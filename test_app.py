import unittest
from unittest.mock import patch
from app import app

class PortalTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
    def test_admin_requires_credentials(self):
        with patch.dict('os.environ', {'OMS_ADMIN_KEY':'test-only'}):
            self.assertEqual(self.client.post('/api/orders').status_code,401)
    def test_tracking_requires_both_credentials(self):
        self.assertEqual(self.client.post('/api/track',json={'tracking':'SFPS-TEST'}).status_code,400)
    def test_tracking_rejects_non_string(self):
        self.assertEqual(self.client.post('/api/track',json={'tracking':1,'access_token':'x'}).status_code,400)
    def test_no_cache(self):
        self.assertEqual(self.client.get('/').headers['Cache-Control'],'no-store')

if __name__ == '__main__':
    unittest.main()
