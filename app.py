import os
import secrets
import hmac
from flask import Flask, request, jsonify
import psycopg

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

def connect():
    return psycopg.connect(os.environ['DATABASE_URL'])

def init_db():
    with connect() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS orders (
            tracking text PRIMARY KEY, access_token text NOT NULL,
            status text NOT NULL, eta date, created_at timestamptz DEFAULT now()
        )""")

@app.after_request
def headers(response):
    response.headers['Cache-Control'] = 'no-store'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'no-referrer'
    return response

@app.get('/')
def home():
    return jsonify(service='SFPS Order Management', state='integration testing', customer_launch=False)

@app.get('/healthz')
def health():
    try:
        with connect() as db:
            db.execute('SELECT 1 FROM orders LIMIT 1')
        return jsonify(status='ok')
    except Exception:
        return jsonify(status='database unavailable'), 503

@app.post('/api/orders')
def create_order():
    key = os.environ.get('OMS_ADMIN_KEY')
    if not key or not hmac.compare_digest(request.headers.get('Authorization',''), 'Bearer '+key):
        return jsonify(error='unauthorized'), 401
    tracking = 'SFPS-' + secrets.token_hex(10).upper()
    token = secrets.token_urlsafe(32)
    import hashlib
    with connect() as db:
        db.execute('INSERT INTO orders (tracking, access_token, status) VALUES (%s,%s,%s)', (tracking, hashlib.sha256(token.encode()).hexdigest(), 'Received'))
    return jsonify(tracking=tracking, access_token=token), 201

@app.post('/api/track')
def track():
    import hashlib
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or not all(isinstance(data.get(k),str) for k in ('tracking','access_token')):
        return jsonify(error='invalid request'), 400
    with connect() as db:
        row = db.execute('SELECT status, eta FROM orders WHERE tracking=%s AND access_token=%s', (data['tracking'],hashlib.sha256(data['access_token'].encode()).hexdigest())).fetchone()
    if not row:
        return jsonify(error='order not found'), 404
    return jsonify(status=row[0], eta=row[1].isoformat() if row[1] else None)

if __name__ == '__main__':
    init_db()
