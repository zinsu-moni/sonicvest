# 🚀 Hosting Setup Guide - Income Distribution Fix

## Problem
Income distribution works locally but not when hosted because the background worker thread doesn't start with Gunicorn.

## Solution
We've separated the income distribution worker into its own process.

---

## 📋 Setup Instructions

### For Heroku

1. **Scale the worker dyno** (IMPORTANT - this is why income wasn't distributing):
   ```bash
   heroku ps:scale worker=1
   ```

2. **Check worker status**:
   ```bash
   heroku ps
   ```
   
   You should see:
   ```
   === web (Free): gunicorn app:app --timeout 120 --workers 2 (1)
   web.1: up
   
   === worker (Free): python worker.py (1)
   worker.1: up
   ```

3. **View worker logs**:
   ```bash
   heroku logs --tail --dyno=worker
   ```

4. **View all logs**:
   ```bash
   heroku logs --tail
   ```

### For Render.com

1. **Add a new Background Worker**:
   - Go to your service dashboard
   - Click "New" → "Background Worker"
   - Set command: `python worker.py`
   - Deploy

2. **Check logs**:
   - View the worker service logs in the dashboard

### For Railway.app

1. **Add worker in railway.json** (create if doesn't exist):
   ```json
   {
     "build": {
       "builder": "nixpacks"
     },
     "deploy": {
       "startCommand": "gunicorn app:app",
       "restartPolicyType": "always"
     }
   }
   ```

2. **Add a new service**:
   - Same repository
   - Set start command: `python worker.py`

### For Other Platforms

1. **Docker/Container Setup**:
   ```dockerfile
   # In your Dockerfile, you need to run both web and worker processes
   # Use a process manager like supervisord
   ```

2. **VPS/Server Setup**:
   ```bash
   # Run web server
   gunicorn app:app --bind 0.0.0.0:8000 --daemon
   
   # Run worker
   python worker.py &
   ```

---

## 🔍 Verification

### Check if worker is running:

1. **View recent logs** for this pattern:
   ```
   ✅ [2026-02-11 10:30:00] Processed 5 income payouts
   ```

2. **Check transaction history** in the app:
   - Look for "package_income" transactions
   - Should appear every 24 hours for active packages

3. **Manual test** (if you have database access):
   ```python
   from worker import distribute_income
   from app import app
   
   with app.app_context():
       count = distribute_income()
       print(f"Processed {count} payouts")
   ```

---

## ⚙️ Configuration

The worker checks for payouts every **30 seconds** but only processes them after the configured interval (default: 24 hours).

You can modify in `app.py`:
```python
SYSTEM_SETTINGS = {
    'INCOME_DROP_HOURS': 24.0,  # Change this value
    # ...
}
```

---

## 🐛 Troubleshooting

### Worker not running?
```bash
# Heroku
heroku ps:scale worker=1
heroku restart worker

# Check logs
heroku logs --tail --dyno=worker
```

### Income still not distributing?

1. **Check package status**:
   - User must have an active package
   - Package must have passed the first 24-hour period
   - Check `last_payout` field in database

2. **Force a payout** (database access needed):
   ```sql
   -- Set last_payout to null or old date to force next payout
   UPDATE user_packages 
   SET last_payout = NOW() - INTERVAL '25 hours'
   WHERE is_active = true;
   ```

3. **Check worker logs** for errors:
   - Database connection issues
   - Permission problems
   - Query execution errors

---

## 💰 Cost Considerations

- **Heroku Free Tier**: No longer available, hobby dynos cost ~$7/month per dyno
- **Heroku Eco**: $5/month for 1000 dyno hours (shared between web + worker)
- **Render**: Free tier available with limitations
- **Railway**: $5/month credit free tier

Most platforms charge separately for worker processes!

---

## 📊 Monitoring

Set up monitoring for:
- Worker uptime
- Income distribution success rate
- Error logs
- Database query performance

---

## 🔄 Restart Commands

```bash
# Heroku
heroku restart worker
heroku restart

# Railway
railway restart

# Render
# Use the restart button in dashboard
```

---

## ✅ Checklist

- [ ] Worker dyno/process is enabled
- [ ] Worker is showing as "up" in platform dashboard
- [ ] Worker logs show successful startup
- [ ] Test user has active package
- [ ] 24 hours have passed since package purchase
- [ ] Database connection is working
- [ ] Transactions are being created in database
- [ ] User balances are increasing

---

## 📞 Support

If income still isn't distributing after following this guide:

1. Check all logs for error messages
2. Verify database connectivity
3. Ensure environment variables are set correctly
4. Check if the worker process has database write permissions
5. Verify the system time/timezone settings

The worker should log every action, so check the logs first!
