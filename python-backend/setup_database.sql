-- FastAPI User API Database Setup
-- Run this script in your Supabase SQL editor

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL CHECK (length(name) >= 1 AND length(name) <= 100),
    email VARCHAR(255) UNIQUE NOT NULL CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    password VARCHAR(255) NOT NULL CHECK (length(password) >= 8),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_is_active ON users(is_active);
CREATE INDEX IF NOT EXISTS idx_users_created_at ON users(created_at);

-- Create function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger to automatically update updated_at
DROP TRIGGER IF EXISTS update_users_updated_at ON users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (RLS) for better security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all operations (you can customize this based on your needs)
CREATE POLICY "Allow all operations for authenticated users" ON users
    FOR ALL USING (true);

-- Insert some sample data (optional)
INSERT INTO users (name, email, password, is_active) VALUES
    ('Admin User', 'admin@example.com', 'sha256_hash_of_password', true),
    ('Test User', 'test@example.com', 'sha256_hash_of_password', true)
ON CONFLICT (email) DO NOTHING;

-- Grant necessary permissions (adjust based on your Supabase setup)
-- GRANT ALL ON users TO authenticated;
-- GRANT USAGE, SELECT ON SEQUENCE users_id_seq TO authenticated; 