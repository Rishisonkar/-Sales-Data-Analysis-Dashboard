-- Run in Supabase Dashboard -> SQL Editor (optional; setup_supabase.py also creates this)

CREATE TABLE IF NOT EXISTS sales_orders (
    order_id VARCHAR(50) PRIMARY KEY,
    order_date TIMESTAMP,
    customer_id VARCHAR(50),
    segment VARCHAR(50),
    region VARCHAR(50),
    state VARCHAR(50),
    category VARCHAR(50),
    sub_category VARCHAR(50),
    sales DOUBLE PRECISION,
    quantity INTEGER,
    discount DOUBLE PRECISION,
    profit DOUBLE PRECISION,
    profit_margin DOUBLE PRECISION,
    calculated_cost_basis DOUBLE PRECISION
);

-- Allow read access for authenticated/anon if using Supabase API later
ALTER TABLE sales_orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access"
ON sales_orders FOR SELECT
USING (true);
