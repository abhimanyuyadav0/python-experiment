# PostgreSQL and pgAdmin Setup Guide

This guide will help you set up PostgreSQL and pgAdmin for the Multi-Tenant Application.

## Installing PostgreSQL

### Windows

1. **Download PostgreSQL**
   - Go to https://www.postgresql.org/download/windows/
   - Download the latest version for Windows
   - Run the installer

2. **Installation Steps**
   - Choose installation directory
   - Set password for `postgres` user (remember this!)
   - Keep default port (5432)
   - Install pgAdmin (included in installer)
   - Complete installation

3. **Verify Installation**
   - Open Command Prompt
   - Run: `psql --version`

### macOS

1. **Using Homebrew**
   ```bash
   brew install postgresql
   brew services start postgresql
   ```

2. **Using Postgres.app**
   - Download from https://postgresapp.com/
   - Drag to Applications folder
   - Double-click to start

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## Installing pgAdmin

### Windows
- Included with PostgreSQL installer
- Or download separately from https://www.pgadmin.org/download/

### macOS
```bash
brew install --cask pgadmin4
```

### Linux
```bash
sudo apt install pgadmin4
```

## Setting Up the Database

### Method 1: Using pgAdmin (GUI)

1. **Open pgAdmin**
   - Launch pgAdmin from Start Menu/Applications
   - Set master password when prompted

2. **Connect to PostgreSQL**
   - Right-click on "Servers" → "Register" → "Server"
   - General tab: Name = "Local PostgreSQL"
   - Connection tab:
     - Host: `localhost`
     - Port: `5432`
     - Username: `postgres`
     - Password: (your postgres password)

3. **Create Database**
   - Right-click on "Databases" → "Create" → "Database"
   - Database name: `multitenant_app`
   - Click "Save"

### Method 2: Using psql (Command Line)

1. **Connect to PostgreSQL**
   ```bash
   psql -U postgres -h localhost
   ```

2. **Create Database**
   ```sql
   CREATE DATABASE multitenant_app;
   \q
   ```

## Configure Environment Variables

1. **Copy environment template**
   ```bash
   cp env.example .env
   ```

2. **Edit .env file**
   ```env
   # Update these values with your PostgreSQL settings
   DATABASE_URL=postgresql://postgres:your_password@localhost:5432/multitenant_app
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=multitenant_app
   DB_USER=postgres
   DB_PASSWORD=your_password
   SECRET_KEY=your-super-secret-key-change-this-in-production
   ```

## Initialize the Application

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize database**
   ```bash
   python init_db.py
   ```

3. **Start the application**
   ```bash
   python -m uvicorn app.main:app --reload --port 5001
   ```

## Testing the Setup

1. **Check API health**
   ```bash
   curl http://localhost:5001/health
   ```

2. **Test login with default admin**
   ```bash
   curl -X POST http://localhost:5001/api/v1/users/authenticate \
     -H "Content-Type: application/json" \
     -d '{"email":"admin@example.com","password":"admin123"}'
   ```

3. **View API documentation**
   - Open http://localhost:5001/docs in your browser

## Troubleshooting

### Connection Issues

**Error: "connection refused"**
- Ensure PostgreSQL is running
- Check if port 5432 is correct
- Verify firewall settings

**Error: "authentication failed"**
- Check username/password in .env
- Verify postgres user password

**Error: "database does not exist"**
- Create the database using pgAdmin or psql
- Check database name in .env

### Common Commands

**Start PostgreSQL service**
- Windows: Services app → PostgreSQL → Start
- macOS: `brew services start postgresql`
- Linux: `sudo systemctl start postgresql`

**Check PostgreSQL status**
- Windows: Services app
- macOS: `brew services list | grep postgresql`
- Linux: `sudo systemctl status postgresql`

**Connect to database**
```bash
psql -U postgres -d multitenant_app -h localhost
```

**List databases**
```sql
\l
```

**List tables**
```sql
\dt
```

## Security Notes

1. **Change default passwords** in production
2. **Use strong secret keys** for JWT
3. **Restrict database access** to application only
4. **Enable SSL** for production databases
5. **Regular backups** of your database

## Next Steps

After setup is complete:

1. Test the API endpoints
2. Explore the database structure in pgAdmin
3. Create additional users for testing
4. Configure your frontend to connect to the API
