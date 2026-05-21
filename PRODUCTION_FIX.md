# Production Deployment Checklist

## Issue Fixed: Server Error After Registration

### **Problem**
When the application was hosted, users encountered server errors during registration because:
1. Database tables were not created automatically in production
2. The `if __name__ == '__main__':` initialization code only runs with `python app.py`
3. Gunicorn (used in production) imports the app without running that initialization

### **Solution Implemented**

✅ **1. Added `@app.before_request` Database Initialization**
   - Database tables are now created automatically on first request
   - Runs regardless of how the app is started (gunicorn, flask run, python app.py)
   - Located in [app.py](app.py) lines ~50-90

✅ **2. Created Production Initialization Script**
   - New file: [init_production_db.py](init_production_db.py)
   - Runs during deployment to ensure database is ready
   - Handles migrations for existing databases

✅ **3. Updated Procfile**
   - Added `release:` command to initialize database before web start
   - Increased gunicorn timeout to 120 seconds
   - Set 2 workers for better performance

✅ **4. Added Error Handling to Registration**
   - Registration route now catches and logs all errors
   - Shows user-friendly error messages
   - Prevents database crashes from breaking the app

---

## Pre-Deployment Checklist

### 1. **Environment Variables** (Required)
Set these on your hosting platform:

```bash
# Security (Generate new secret key for production!)
SECRET_KEY=your-production-secret-key-here

# Database (if using PostgreSQL)
DATABASE_URL=postgresql://user:password@host:port/database

# App Settings
FLASK_ENV=production
MINIMUM_WITHDRAWAL=2200
WITHDRAWAL_FEE_PERCENTAGE=11

# GTR Bank Integration (if using)
GTR_BANK_API_KEY=your-gtr-api-key
GTR_BANK_MERCHANT_ID=your-merchant-id
```

### 2. **Generate Secret Key**
Never use the default secret key in production!

```python
import secrets
print(secrets.token_hex(32))
```

### 3. **Update Configuration**
Edit [config.py](config.py) if needed to match your environment.

### 4. **Install Dependencies**
Ensure [requirements.txt](requirements.txt) is up to date:

```bash
pip freeze > requirements.txt
```

---

## Deployment Steps

### **Option A: Heroku**

1. **Install Heroku CLI**
   ```bash
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login and Create App**
   ```bash
   heroku login
   heroku create your-app-name
   ```

3. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
   heroku config:set FLASK_ENV=production
   ```

4. **Deploy**
   ```bash
   git add .
   git commit -m "Fixed registration server error"
   git push heroku main
   ```

5. **Check Logs**
   ```bash
   heroku logs --tail
   ```

### **Option B: Render**

1. **Create New Web Service**
   - Connect your GitHub repository
   - Select branch to deploy

2. **Configure Build & Start Commands**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app --timeout 120 --workers 2`
   - Pre-deploy Command: `python init_production_db.py`

3. **Set Environment Variables**
   - Add `SECRET_KEY` and other variables in dashboard

4. **Deploy**
   - Render auto-deploys on git push

### **Option C: PythonAnywhere**

1. **Upload Files**
   - Use git or file manager to upload your project

2. **Create Virtual Environment**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 myenv
   pip install -r requirements.txt
   ```

3. **Initialize Database**
   ```bash
   python init_production_db.py
   ```

4. **Configure WSGI**
   - Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`
   - Point to your `app.py`

5. **Reload Web App**

### **Option D: DigitalOcean App Platform**

1. **Create New App**
   - Connect GitHub repository

2. **Configure App**
   - Type: Web Service
   - Run Command: `gunicorn app:app --timeout 120 --workers 2`
   - Build Command: `pip install -r requirements.txt`

3. **Add Database Component** (Optional)
   - PostgreSQL recommended for production

4. **Set Environment Variables**

5. **Deploy**

---

## Post-Deployment Verification

### 1. **Test Registration**
   - Go to `/register`
   - Create a test account
   - Should see success message and redirect to login

### 2. **Test Login**
   - Use credentials from registration
   - Should see dashboard

### 3. **Test Admin Panel**
   - Go to `/admin/login`
   - Create admin user if needed:
     ```bash
     python create_admin.py
     ```

### 4. **Check Database**
   - Verify tables were created
   - Check sample packages exist

### 5. **Monitor Logs**
   - Look for any errors or warnings
   - Check that background processor started

---

## Common Deployment Issues & Solutions

### Issue: "Internal Server Error" on Registration
**Solution:** Database not initialized
```bash
python init_production_db.py
# Or restart the application to trigger @app.before_request
```

### Issue: "Application Error" on Start
**Solution:** Check logs for missing dependencies
```bash
heroku logs --tail  # Heroku
# or check hosting platform logs
```

### Issue: Static Files Not Loading
**Solution:** Configure static file serving
```python
# For production, use a proper web server or CDN
# In app.py, ensure static folder is configured
```

### Issue: Database Connection Errors
**Solution:** Check DATABASE_URL environment variable
```bash
# Make sure it's set correctly
echo $DATABASE_URL
```

### Issue: "Secret Key Not Set" Error
**Solution:** Set SECRET_KEY environment variable
```bash
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
```

---

## Database Migration Notes

The app now automatically:
- Creates all required tables on first request
- Adds missing columns to existing databases
- Initializes admin database
- No manual migration needed

If you need to reset the database:
```bash
python reset_database.py
```

---

## Monitoring & Maintenance

### Check Application Health
```bash
# Heroku
heroku ps

# Check logs
heroku logs --tail

# Scale workers
heroku ps:scale web=1 worker=1
```

### Backup Database
```bash
# For SQLite (local backup)
cp fintech.db fintech.db.backup

# For PostgreSQL (Heroku)
heroku pg:backups:capture
heroku pg:backups:download
```

### Update Application
```bash
git add .
git commit -m "Update message"
git push heroku main
```

---

## Security Checklist

- [ ] Changed default SECRET_KEY
- [ ] Set FLASK_ENV=production
- [ ] Disabled debug mode
- [ ] Using HTTPS (most platforms provide this automatically)
- [ ] Set secure session cookies
- [ ] Protected admin routes
- [ ] Validated all user inputs
- [ ] Sanitized database queries (using SQLAlchemy ORM)

---

## Performance Optimization

### Recommended Settings for Different Scales

**Small (< 100 users):**
```
workers=2
timeout=120
```

**Medium (100-1000 users):**
```
workers=4
timeout=120
worker-class=gevent
```

**Large (1000+ users):**
- Use PostgreSQL instead of SQLite
- Add Redis for caching
- Use CDN for static files
- Scale workers: `workers = (2 * CPU_cores) + 1`

---

## Support

If you encounter issues after deployment:
1. Check application logs first
2. Verify environment variables are set
3. Test database connection
4. Review this checklist

For specific errors, the app now shows user-friendly messages and logs detailed errors for debugging.

---

## Files Modified in This Fix

1. [app.py](app.py) - Added `@app.before_request` database initialization
2. [app.py](app.py) - Added error handling to registration route
3. [Procfile](Procfile) - Added release command for database initialization
4. [init_production_db.py](init_production_db.py) - New production initialization script

**All changes are backward compatible** - your app will work both locally and in production.
