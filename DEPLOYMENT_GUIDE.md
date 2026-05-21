# Fintech Finance Application - Deployment Guide

## Quick Start

Your application is now configured for production deployment.

### Key Files Created
- **Procfile**: Specifies how to run your app on hosting platforms
- **runtime.txt**: Python version specification
- **.env.example**: Template for environment variables
- **requirements.txt**: All dependencies with gunicorn included

---

## Deployment Steps

### 1. **Update Environment Variables**

Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

Edit `.env` with your production values:
```
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=<generate-a-long-random-string>
PORT=5000
```

### 2. **Test Locally**

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py
```

Your app should be accessible at `http://localhost:5000`

---

## Hosting Platform Instructions

### **Heroku**

```bash
# Install Heroku CLI
# Create account at heroku.com

# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secure-key

# Deploy
git push heroku main

# View logs
heroku logs --tail
```

### **Render.com**

1. Push code to GitHub
2. Visit [render.com](https://render.com)
3. Create new **Web Service**
4. Connect GitHub repository
5. Set **Build Command**:
   ```
   pip install -r requirements.txt
   ```
6. Set **Start Command**:
   ```
   gunicorn app:app
   ```
7. Add environment variables in dashboard
8. Deploy

### **Railway.app**

1. Push code to GitHub
2. Visit [railway.app](https://railway.app)
3. Create new project from GitHub
4. Add environment variables
5. Railway auto-detects Flask app
6. Deploy

### **PythonAnywhere**

1. Upload your code
2. Go to Web tab
3. Add new web app
4. Choose Python 3.11
5. Point to your project directory
6. Set WSGI configuration:
   ```python
   import sys
   path = '/home/username/mysite'
   sys.path.insert(0, path)
   from app import app as application
   ```
7. Reload

### **AWS Elastic Beanstalk**

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 fintech-app

# Create environment
eb create fintech-env

# Deploy
eb deploy

# Open in browser
eb open
```

---

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| FLASK_ENV | Environment mode | `production` |
| FLASK_DEBUG | Enable debug mode | `0` (production) |
| SECRET_KEY | Session encryption key | Generate with `python -c "import secrets; print(secrets.token_hex(32))"` |
| PORT | Server port | `5000` |
| DATABASE_URL | Database connection | `sqlite:///fintech.db` (local) |
| GTR_MERCHANT_ID | GTR Pay merchant ID | Your merchant ID |
| GTR_SECRET_KEY | GTR Pay secret key | Your secret key |

---

## Troubleshooting

### Error: "Address already in use"
```bash
# Kill process on port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Error: "ModuleNotFoundError"
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt
```

### Error: "Database locked"
```bash
# Remove old database and restart
rm fintech.db
python app.py
```

### 500 Error on Deployment
1. Check platform logs for detailed error
2. Verify all environment variables are set
3. Check database file path is correct
4. Ensure PORT from environment is being used

---

## Security Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Set `FLASK_DEBUG=0`
- [ ] Generate secure `SECRET_KEY`
- [ ] Use HTTPS in production
- [ ] Set database permissions correctly
- [ ] Enable CORS only for trusted origins
- [ ] Use environment variables for sensitive data
- [ ] Keep dependencies updated: `pip install --upgrade -r requirements.txt`

---

## Performance Tips

1. Use gunicorn with multiple workers:
   ```bash
   gunicorn -w 4 app:app
   ```

2. Enable gzip compression in Flask

3. Use SQLite optimizations or switch to PostgreSQL for production

4. Cache static files with CDN

5. Monitor error logs:
   ```bash
   tail -f app.log
   ```

---

## Support

For issues with specific platforms:
- **Heroku**: https://devcenter.heroku.com/
- **Render**: https://render.com/docs
- **Railway**: https://docs.railway.app/
- **PythonAnywhere**: https://www.pythonanywhere.com/help/
