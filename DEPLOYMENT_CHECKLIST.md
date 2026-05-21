# 🚀 Production Deployment Checklist

After experiencing database connection issues in production, use this checklist to ensure proper deployment.

## Pre-Deployment

### 1. Code Updates
- [x] Worker process separated into `worker.py`
- [x] Database connection pooling configured
- [x] Deprecated datetime usage fixed
- [x] Health check endpoints added (`/health`, `/worker-status`)
- [x] Error handling and retry logic implemented

### 2. Local Testing
```bash
# Test database connection
python check_db_connection.py

# Test worker functionality
python test_worker.py

# Start full system
start_local.bat  # Windows
./start_local.sh # Linux/Mac
```

**Expected Results:**
- ✅ Database connection test passes
- ✅ Worker processes test payouts
- ✅ Both web and worker run without errors

## Deployment Steps

### 3. Push to Repository
```bash
git add .
git commit -m "Fix: Database connection pooling and worker stability"
git push origin main
```

### 4. Deploy to Hosting Platform

Platform will auto-deploy if configured. Wait for deployment to complete.

### 5. 🔥 CRITICAL: Enable Worker Process

#### Heroku
```bash
# Enable worker
heroku ps:scale worker=1

# Verify it's running
heroku ps

# Expected output:
# === web (Eco): gunicorn app:app --timeout 120 --workers 2 (1)
# web.1: up 2026/02/11 10:30:00
#
# === worker (Eco): python worker.py (1)
# worker.1: up 2026/02/11 10:30:05

# Check worker logs
heroku logs --tail --dyno=worker
```

#### Render.com
1. Go to Dashboard
2. Click "New" → "Background Worker"
3. Select your repository
4. Set start command: `python worker.py`
5. Click "Create Background Worker"

#### Railway
1. Go to your project
2. Click "+ New Service"
3. Select "Add Service" → "From Repo"
4. Choose same repository
5. Set start command: `python worker.py`
6. Deploy

### 6. Configure Environment Variables

Ensure these are set in production:

```
DATABASE_URL=postgresql://user:pass@host:port/db
SECRET_KEY=<random-secure-key>
GTR_API_KEY=<your-gtr-api-key>
GTR_SECRET_KEY=<your-gtr-secret>
FLASK_ENV=production
```

### 7. Verify Database Connection

Use health endpoint:
```bash
curl https://your-app.herokuapp.com/health

# Expected response:
# {
#   "status": "ok",
#   "database": "healthy",
#   "active_packages": 19,
#   "timestamp": "2026-02-11T10:30:00"
# }
```

### 8. Check Worker Status

```bash
curl https://your-app.herokuapp.com/worker-status

# Expected response:
# {
#   "status": "ok",
#   "recent_payouts_1h": 0,
#   "packages_due": 0,
#   "total_active_packages": 19,
#   "worker_expected": "running separately",
#   "check_interval": "30 seconds",
#   "payout_interval": "24 hours"
# }
```

### 9. Monitor Worker Logs

```bash
# Heroku
heroku logs --tail --dyno=worker

# Look for:
# ========================================
# 🚀 INCOME DISTRIBUTION WORKER STARTED
# ========================================
# ⏰ Income drops every: 24.0 hours
# 🔄 Checking every: 30 seconds
# 🌐 Environment: production
# 🔌 Database: Connected
# ========================================
```

## Post-Deployment Verification

### 10. Wait for First Payout Cycle

1. Note the time of deployment
2. Add 24 hours for packages that haven't received first payout
3. Check user dashboard for income transactions

### 11. Check Database Records

```sql
-- Check recent income transactions
SELECT * FROM transactions 
WHERE type = 'package_income' 
ORDER BY created_at DESC 
LIMIT 10;

-- Check package payout status
SELECT 
    u.username,
    p.name as package_name,
    up.start_date,
    up.last_payout,
    up.daily_return,
    up.total_earned,
    up.is_active
FROM user_packages up
JOIN users u ON up.user_id = u.id
JOIN packages p ON up.package_id = p.id
WHERE up.is_active = true
ORDER BY up.last_payout DESC NULLS FIRST;
```

### 12. Test With Real User

1. Create test account
2. Purchase smallest package
3. Wait 24 hours
4. Check if income was credited
5. Verify transaction history

## Monitoring

### Continuous Monitoring Setup

1. **Worker Heartbeat** - Check logs every hour for:
   ```
   💓 Worker heartbeat - Still running (120 checks completed, 0 errors)
   ```

2. **Health Endpoint** - Set up monitoring tool (UptimeRobot, etc):
   - URL: `https://your-app.com/health`
   - Check every 5 minutes
   - Alert if status != "ok"

3. **Worker Status** - Monitor for payouts:
   - URL: `https://your-app.com/worker-status`
   - Check `packages_due` count
   - Alert if it remains > 0 for extended period

4. **Database Alerts**:
   - Monitor connection pool usage
   - Alert on connection errors
   - Track query performance

### Log Analysis

Set up log aggregation to track:
- ✅ Income distributions (look for "Processed X payouts")
- ❌ Database connection errors
- ⚠️ Worker restarts
- 🔄 Connection pool recycling

## Troubleshooting

### Worker Not Starting

```bash
# Check if worker dyno is enabled
heroku ps

# Scale up if needed
heroku ps:scale worker=1

# Check for startup errors
heroku logs --tail --dyno=worker
```

### Database Connection Errors

```bash
# Check connection pooling config
# In app.py, verify SQLALCHEMY_ENGINE_OPTIONS

# Test connection locally
python check_db_connection.py

# Check PostgreSQL server status
heroku pg:info  # for Heroku
```

### Income Not Distributing

1. **Verify worker is running**:
   ```bash
   curl https://your-app.com/worker-status
   ```

2. **Check package status**:
   - Must be active
   - 24 hours must have passed
   - Package not expired

3. **Force test payout**:
   ```bash
   heroku run python test_worker.py
   ```

4. **Check worker logs** for errors:
   ```bash
   heroku logs --tail --dyno=worker | grep ERROR
   ```

### Too Many Database Connections

If you see "too many connections" errors:

1. **Reduce connection pool**:
   ```python
   'pool_size': 5,  # Reduce from 10
   'max_overflow': 10,  # Reduce from 20
   ```

2. **Check for connection leaks**:
   ```bash
   # Monitor pool status
   curl https://your-app.com/health
   ```

3. **Restart worker and web**:
   ```bash
   heroku restart
   ```

## Success Indicators

✅ **Working Correctly When:**

1. Worker logs show regular heartbeats
2. `/health` endpoint returns status "ok"
3. `/worker-status` shows `packages_due: 0` after payout time
4. User balances increase every 24 hours
5. Transaction history shows package_income entries
6. No connection errors in logs
7. Worker stays running without restarts

## Rollback Plan

If deployment fails:

1. **Revert code**:
   ```bash
   git revert HEAD
   git push origin main
   ```

2. **Or rollback on platform**:
   ```bash
   # Heroku
   heroku rollback
   
   # Railway - use dashboard
   # Render - redeploy previous version
   ```

3. **Scale down worker** if causing issues:
   ```bash
   heroku ps:scale worker=0
   ```

4. **Check error logs** before re-attempting

## Cost Management

### Dyno/Worker Costs

- **Heroku Eco**: $5/month for 1000 dyno hours (shared)
  - 1 web + 1 worker = 2 dynos
  - 2 dynos × 730 hours = 1460 hours needed
  - Need ~2 Eco plans or upgrade to Basic

- **Heroku Basic**: $7/dyno/month
  - Separate billing for web and worker
  - Total: $14/month

- **Render**: Free tier includes background workers

- **Railway**: $5/month free credit, then pay-as-you-go

### Optimization Tips

1. **Single worker** is sufficient for most loads
2. **Web workers**: 2 is usually enough
3. Monitor resource usage and scale as needed
4. Use free tier services for testing

## Support Resources

- **Deployment Guide**: [HOSTING_SETUP.md](HOSTING_SETUP.md)
- **Income Fix Guide**: [INCOME_FIX_README.md](INCOME_FIX_README.md)
- **Database Check**: `python check_db_connection.py`
- **Worker Test**: `python test_worker.py`
- **Health Check**: `https://your-app.com/health`
- **Worker Status**: `https://your-app.com/worker-status`

## Final Checklist

Before considering deployment complete:

- [ ] Code deployed successfully
- [ ] Worker process enabled and running
- [ ] Health endpoint returns "ok"
- [ ] Worker logs show startup message
- [ ] Database connection test passes
- [ ] No errors in last 15 minutes of logs
- [ ] Environment variables verified
- [ ] Monitoring/alerting configured
- [ ] Test user created and package purchased
- [ ] Documentation updated with app URL
- [ ] Team notified of deployment

---

**Remember**: The worker MUST be running separately for income distribution to work in production!
