# SafeBite Deployment Guide

This guide covers deploying SafeBite from development to production environments.

## 🏗️ Architecture Overview

```
Frontend (React/Vite) → Backend (FastAPI) → Database (SQLite/PostgreSQL)
```

## 🔧 Environment Setup

### Development Environment
Already configured and ready to use:
- SQLite database with seeded data
- FastAPI backend with auto-reload
- Vite frontend with hot module replacement

### Production Considerations

#### Environment Variables
Create `.env` file in backend directory:

```env
# Security
SECRET_KEY=your-super-secure-secret-key-minimum-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Database
DATABASE_URL=postgresql://username:password@host:port/database_name

# CORS (Update for your domain)
CORS_ORIGINS=["https://yourdomain.com", "https://www.yourdomain.com"]

# Optional: Email configuration for future features
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your-email@example.com
SMTP_PASSWORD=your-email-password
```

## 🗄️ Database Migration

### From SQLite to PostgreSQL

1. **Install PostgreSQL dependencies:**
```bash
pip install psycopg2-binary
```

2. **Update database configuration:**
```python
# backend/app/core/config.py
DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:pass@localhost/safebite")
```

3. **Create PostgreSQL database:**
```sql
CREATE DATABASE safebite;
CREATE USER safebite_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE safebite TO safebite_user;
```

4. **Migrate data:**
```bash
# Run database creation
python -c "from app.core.database import engine, Base; Base.metadata.create_all(bind=engine)"

# Seed with data
cd database
python seed.py
```

## 🚀 Backend Deployment

### Option 1: Docker Deployment

1. **Create Dockerfile:**
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. **Create docker-compose.yml:**
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://safebite_user:password@db:5432/safebite
      - SECRET_KEY=your-secret-key
    depends_on:
      - db
    volumes:
      - ./backend:/app
    
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=safebite
      - POSTGRES_USER=safebite_user
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  postgres_data:
```

3. **Deploy:**
```bash
docker-compose up -d
```

### Option 2: Manual Server Deployment

1. **Install Python and dependencies:**
```bash
# On Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx

# Create virtual environment
python3 -m venv safebite_env
source safebite_env/bin/activate
pip install -r requirements.txt
```

2. **Install production ASGI server:**
```bash
pip install gunicorn
```

3. **Create systemd service:**
```ini
# /etc/systemd/system/safebite.service
[Unit]
Description=SafeBite FastAPI application
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/var/www/safebite/backend
Environment="PATH=/var/www/safebite/safebite_env/bin"
ExecStart=/var/www/safebite/safebite_env/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
ExecReload=/bin/kill -s HUP $MAINPID
Restart=always

[Install]
WantedBy=multi-user.target
```

4. **Start service:**
```bash
sudo systemctl enable safebite
sudo systemctl start safebite
```

## 🌐 Frontend Deployment

### Build for Production

1. **Install dependencies and build:**
```bash
cd frontend
npm install
npm run build
```

2. **Serve static files:**

**Option A: Nginx**
```nginx
# /etc/nginx/sites-available/safebite
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Frontend
    location / {
        root /var/www/safebite/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend docs
    location /docs {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Option B: Vercel/Netlify**
```json
{
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "https://your-backend-domain.com/api/$1"
    }
  ]
}
```

### Update API Base URL

Update frontend configuration:
```javascript
// src/services/api.js
export const api = axios.create({
  baseURL: process.env.NODE_ENV === 'production' 
    ? 'https://your-backend-domain.com/api'
    : '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})
```

## 🔒 Security Configuration

### SSL/HTTPS Setup

1. **Install Certbot:**
```bash
sudo apt install certbot python3-certbot-nginx
```

2. **Obtain SSL certificate:**
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

3. **Auto-renewal:**
```bash
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

### Security Headers

Update Nginx configuration:
```nginx
# Security headers
add_header X-Content-Type-Options nosniff;
add_header X-Frame-Options DENY;
add_header X-XSS-Protection "1; mode=block";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header Referrer-Policy "strict-origin-when-cross-origin";
add_header Content-Security-Policy "default-src 'self'; img-src 'self' https://images.unsplash.com https://*.unsplash.com; font-src 'self' https://fonts.gstatic.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;";
```

### Environment Security

1. **Secure environment variables:**
```bash
# Set proper permissions
chmod 600 .env

# Use secrets management in production
# AWS Secrets Manager, Azure Key Vault, etc.
```

2. **Database security:**
```python
# Use connection pooling
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=0
)
```

## 📊 Monitoring & Logging

### Application Monitoring

1. **Add logging configuration:**
```python
# backend/app/core/logging.py
import logging
from logging.handlers import RotatingFileHandler

logging.basicConfig(
    handlers=[
        RotatingFileHandler('/var/log/safebite/app.log', maxBytes=10000000, backupCount=3),
        logging.StreamHandler()
    ],
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s %(message)s'
)
```

2. **Health check endpoint:**
```python
# Already implemented at GET /
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "1.0.0"
    }
```

### Database Monitoring

```sql
-- PostgreSQL monitoring queries
SELECT * FROM pg_stat_activity WHERE state = 'active';
SELECT schemaname, tablename, n_tup_ins, n_tup_upd, n_tup_del 
FROM pg_stat_user_tables;
```

## 🔄 Backup & Recovery

### Database Backup

```bash
#!/bin/bash
# backup_script.sh
BACKUP_DIR="/var/backups/safebite"
DATE=$(date +%Y%m%d_%H%M%S)

# PostgreSQL backup
pg_dump -U safebite_user -h localhost safebite | gzip > $BACKUP_DIR/safebite_$DATE.sql.gz

# Cleanup old backups (keep last 7 days)
find $BACKUP_DIR -name "safebite_*.sql.gz" -mtime +7 -delete
```

### Application Backup

```bash
#!/bin/bash
# Backup application code and configuration
tar -czf /var/backups/safebite/app_backup_$(date +%Y%m%d).tar.gz \
  /var/www/safebite \
  --exclude=/var/www/safebite/node_modules \
  --exclude=/var/www/safebite/frontend/dist
```

## 📈 Performance Optimization

### Backend Optimization

1. **Database indexing:**
```sql
-- Add indexes for common queries
CREATE INDEX idx_restaurants_city ON restaurants(city);
CREATE INDEX idx_restaurants_cuisine ON restaurants(cuisine);
CREATE INDEX idx_restaurants_approval_status ON restaurants(approval_status);
CREATE INDEX idx_restaurants_safety_score ON restaurants(safety_score DESC);
```

2. **Caching:**
```python
# Install redis
pip install redis

# Add caching
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="safebite-cache")
```

### Frontend Optimization

1. **Code splitting:**
```javascript
// Implement lazy loading
const AdminDashboard = lazy(() => import('./pages/AdminDashboard'));
const OwnerDashboard = lazy(() => import('./pages/OwnerDashboard'));
```

2. **Image optimization:**
```javascript
// Use next-gen image formats
const optimizedImageUrl = (url) => {
  return url.replace('?auto=format&fit=crop', '?auto=format&fit=crop&fm=webp');
};
```

## 🚨 Troubleshooting

### Common Issues

1. **CORS errors:**
```python
# Update CORS origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. **Database connection issues:**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check connection
psql -U safebite_user -h localhost -d safebite
```

3. **File permission errors:**
```bash
# Fix permissions
sudo chown -R www-data:www-data /var/www/safebite
sudo chmod -R 755 /var/www/safebite
```

### Monitoring Commands

```bash
# Check application logs
sudo journalctl -u safebite -f

# Monitor system resources
htop
df -h
free -m

# Check network connections
netstat -tulpn | grep :8000
```

## 📋 Deployment Checklist

### Pre-deployment
- [ ] Environment variables configured
- [ ] Database migrated and seeded
- [ ] SSL certificates installed
- [ ] Security headers configured
- [ ] Backup system in place

### Post-deployment
- [ ] Health checks passing
- [ ] All API endpoints functional
- [ ] Frontend loads correctly
- [ ] Authentication working
- [ ] Admin functions accessible
- [ ] Performance monitoring active

### Regular Maintenance
- [ ] Database backups automated
- [ ] SSL certificate renewal scheduled
- [ ] Security updates applied
- [ ] Performance metrics monitored
- [ ] Logs reviewed regularly

## 🎯 Scaling Considerations

### Horizontal Scaling
- Load balancer (Nginx/HAProxy)
- Multiple application instances
- Database read replicas
- CDN for static assets

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Implement caching layers
- Use async processing for heavy tasks

This deployment guide ensures a secure, scalable, and maintainable production environment for SafeBite.