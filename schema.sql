CREATE TABLE IF NOT EXISTS companies (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), name text NOT NULL, created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS members (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), company_id uuid NOT NULL REFERENCES companies(id),
 email text NOT NULL UNIQUE, password_hash text NOT NULL, role text NOT NULL CHECK(role IN ('administrator','procurement','finance','engineer','logistics')), active boolean NOT NULL DEFAULT true
);
CREATE TABLE IF NOT EXISTS procurement_requests (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), company_id uuid NOT NULL REFERENCES companies(id),
 created_by uuid NOT NULL REFERENCES members(id), kind text NOT NULL CHECK(kind IN ('rfq','delivery','support','rma','credit','framework')),
 subject text NOT NULL, description text NOT NULL, status text NOT NULL DEFAULT 'submitted', created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS audit_events (
 id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY, company_id uuid REFERENCES companies(id), actor_id uuid REFERENCES members(id), action text NOT NULL, created_at timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE orders ADD COLUMN IF NOT EXISTS company_id uuid REFERENCES companies(id);
ALTER TABLE orders ADD COLUMN IF NOT EXISTS po_reference text;
