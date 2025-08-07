-- Add role column to users table
ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user' NOT NULL;

-- Add constraint to ensure valid roles
ALTER TABLE users ADD CONSTRAINT check_role CHECK (role IN ('admin', 'tenant', 'user'));

-- Create index for role-based queries
CREATE INDEX idx_users_role ON users(role);

-- Update existing users to have appropriate roles (optional)
-- You can modify these based on your existing data
-- UPDATE users SET role = 'admin' WHERE email = 'admin@example.com';
-- UPDATE users SET role = 'tenant' WHERE email LIKE '%tenant%';

-- Add some sample data with different roles
INSERT INTO users (name, email, password, is_active, role, created_at, updated_at) VALUES
('Admin User', 'admin@gmail.com', '1234567890', true, 'admin', NOW(), NOW()),
('Tenant Manager', 'tenant@gmail.com', '1234567890', true, 'tenant', NOW(), NOW()),
('Regular User', 'user@gmail.com', '1234567890', true, 'user', NOW(), NOW())
ON CONFLICT (email) DO NOTHING; 