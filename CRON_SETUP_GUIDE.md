# Income Payout Cron Job Setup Guide

## ⚠️ CRITICAL: Why You Need This

The income payout system requires a **cron job** to work in production. The background thread in `app.py` **only works locally** when running `python app.py` directly. 

Production servers (Gunicorn, uWSGI, Vercel, etc.) **do not execute** the `if __name__ == '__main__'` block, so the background thread never starts.

---

## 🔧 Setup Steps (All Platforms)

### Step 1: Set CRON_SECRET Environment Variable

Generate a secure random token and add it to your hosting platform's environment variables:

```bash
# Generate a secure token (run locally)
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Add this as `CRON_SECRET` in your hosting platform's environment variables.

### Step 2: Set Up the Cron Job

Your cron job should call this endpoint:
```
https://yourdomain.com/cron/process-income-payouts?token=YOUR_CRON_SECRET
```

**Recommended Frequency:** Every 30-60 minutes

---

## 🌐 Platform-Specific Instructions

### PXXL.app (Recommended for Your Setup) ⭐

PXXL.app has **built-in cron job support** - the easiest setup!

**Quick Setup:**

1. **Set CRON_SECRET in PXXL.app:**
   - Go to your app dashboard → Environment Variables
   - Add: `CRON_SECRET` = (your generated token)
   - Restart your app

2. **Create Cron Job in PXXL Dashboard:**
   - Go to your app → **Cron Jobs** or **Scheduled Tasks**
   - Click **"Add New Cron Job"**
   - **Name:** `Income Payout Processor`
   - **Command/URL:** `/cron/process-income-payouts?token=$CRON_SECRET`
     - Use `$CRON_SECRET` - PXXL auto-injects environment variables
   - **Schedule:** `0 * * * *` (every hour) or "Every hour"
   - **Enabled:** ✓ Yes
   - Save

3. **Benefits of PXXL's Built-in Cron:**
   - ✅ No external service needed
   - ✅ Automatic environment variable injection
   - ✅ Built-in logs and monitoring
   - ✅ More reliable (same infrastructure)

4. **Test:**
```bash
curl "https://your-app.pxxl.app/cron/process-income-payouts?token=YOUR_CRON_SECRET"
```

**See [PXXL_INCOME_SETUP.md](PXXL_INCOME_SETUP.md) for detailed step-by-step guide.**

---

### Vercel

**Option 1: Vercel Cron Jobs (Recommended)**

1. Create or update `vercel.json`:

```json
{
  "crons": [{
    "path": "/cron/process-income-payouts?token=$CRON_SECRET",
    "schedule": "0 * * * *"
  }]
}
```

2. Deploy: `vercel --prod`

**Note:** Vercel crons use the environment variable directly in the schedule.

---

**Option 2: Use External Cron Service**

Use a free service like:
- [cron-job.org](https://cron-job.org)
- [EasyCron](https://www.easycron.com)
- [Uptime Robot](https://uptimerobot.com) (set as HTTP monitor)

Create a job that calls:
```
https://yourdomain.vercel.app/cron/process-income-payouts?token=YOUR_CRON_SECRET
```

---

### Heroku

**Option 1: Heroku Scheduler (Recommended)**

1. Add Heroku Scheduler addon:
```bash
heroku addons:create scheduler:standard
```

2. Open scheduler dashboard:
```bash
heroku addons:open scheduler
```

3. Add new job with command:
```bash
curl "https://yourdomain.herokuapp.com/cron/process-income-payouts?token=$CRON_SECRET"
```

4. Set frequency: Every hour or every 10 minutes

---

**Option 2: Custom Dyno (More Reliable)**

1. Create `clock.py`:
```python
from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import os

scheduler = BlockingScheduler()

@scheduler.scheduled_job('interval', minutes=30)
def process_income():
    token = os.environ.get('CRON_SECRET')
    url = f"https://yourdomain.herokuapp.com/cron/process-income-payouts?token={token}"
    response = requests.get(url)
    print(f"Processed income: {response.json()}")

scheduler.start()
```

2. Add to `requirements.txt`:
```
APScheduler==3.10.4
```

3. Update `Procfile`:
```
web: gunicorn app:app
clock: python clock.py
```

4. Scale up the clock dyno:
```bash
heroku ps:scale clock=1
```

---

### Render

1. Go to your Render dashboard
2. Select your Web Service
3. Go to "Cron Jobs" tab
4. Click "Add Cron Job"
5. Enter:
   - **Name:** Process Income Payouts
   - **Command:** 
     ```bash
     curl "https://yourdomain.onrender.com/cron/process-income-payouts?token=$CRON_SECRET"
     ```
   - **Schedule:** `0 * * * *` (every hour) or `*/30 * * * *` (every 30 minutes)

---

### Railway

1. Install Railway CLI:
```bash
npm i -g @railway/cli
```

2. Add cron job via Railway dashboard or use external service

**Recommended:** Use external cron service (cron-job.org) since Railway doesn't have built-in cron:

```
https://yourdomain.railway.app/cron/process-income-payouts?token=YOUR_CRON_SECRET
```

---

### Traditional VPS (Linux with Crontab)

1. SSH into your server

2. Edit crontab:
```bash
crontab -e
```

3. Add this line (runs every 30 minutes):
```bash
*/30 * * * * curl "https://yourdomain.com/cron/process-income-payouts?token=YOUR_CRON_SECRET" > /dev/null 2>&1
```

Or if your app is on same server:
```bash
*/30 * * * * curl "http://localhost:5000/cron/process-income-payouts?token=YOUR_CRON_SECRET" > /dev/null 2>&1
```

4. Save and exit. Verify with:
```bash
crontab -l
```

---

### DigitalOcean App Platform

1. Go to your app in DigitalOcean dashboard
2. Navigate to "Jobs" section
3. Create a new Job:
   - **Name:** income-payout-processor
   - **Command:** 
     ```bash
     curl "https://yourdomain.ondigitalocean.app/cron/process-income-payouts?token=$CRON_SECRET"
     ```
   - **Job Type:** Pre-Deploy Job (runs before deployment) or Cron Job
   - **Schedule:** `0 * * * *`

---

## 🧪 Testing Your Cron Job

### Test Endpoint Manually

```bash
# Replace with your actual URL and token
curl "https://yourdomain.com/cron/process-income-payouts?token=YOUR_CRON_SECRET"
```

**Expected Response:**
```json
{
  "success": true,
  "processed": 5,
  "timestamp": "2026-02-12T10:30:00",
  "total_active_packages": 10
}
```

### Test Without Token (Should Fail)

```bash
curl "https://yourdomain.com/cron/process-income-payouts"
```

**Expected Response:**
```json
{
  "success": false,
  "error": "Unauthorized - Invalid or missing token"
}
```

---

## 🔍 Monitoring

### Check Logs

After setting up, monitor your application logs to see if payouts are processing:

**Heroku:**
```bash
heroku logs --tail
```

**Vercel:**
Check Function Logs in dashboard

**Render:**
Check Logs tab in dashboard

**Look for:**
```
✅ Cron job processed 5 income payouts at 2026-02-12 10:30:00
```

### Create Monitoring Endpoint

Add this to monitor cron job status (already included in the endpoint response):

```bash
# Check last execution
curl "https://yourdomain.com/cron/process-income-payouts?token=YOUR_CRON_SECRET"
```

---

## 📊 Recommended Cron Frequencies

- **Every 30 minutes:** `*/30 * * * *` (Good balance)
- **Every hour:** `0 * * * *` (Recommended)
- **Every 2 hours:** `0 */2 * * *` (Light load)

Since income drops every 24 hours (`INCOME_DROP_HOURS = 24.0`), running every 30-60 minutes ensures timely processing without overwhelming your server.

---

## 🔒 Security Tips

1. **Always set CRON_SECRET** in production
2. **Use HTTPS** only for cron endpoint
3. **Rotate CRON_SECRET** periodically (every 3-6 months)
4. **Monitor failed requests** in your logs
5. **Use long, random tokens** (32+ characters)

---

## ❓ Troubleshooting

### Cron job returns 401 Unauthorized

- Check CRON_SECRET is set correctly in environment variables
- Ensure token in URL matches CRON_SECRET exactly
- No extra spaces or quotes in environment variable

### Cron job returns 500 Error

- Check application logs for detailed error
- Verify database connection is working
- Test endpoint manually first

### No payouts despite cron running

- Check if users have active packages: query `UserPackage` table
- Verify `last_payout` timestamps are updating
- Check `INCOME_DROP_HOURS` setting (24 hours by default)
- Ensure packages have `end_date` > current time

### Database connection timeout

- Increase `pool_size` in `SQLALCHEMY_ENGINE_OPTIONS`
- Check database hosting plan limits
- Ensure database is not sleeping (common on free tiers)

---

## 🎯 Quick Start Checklist

- [ ] Generate secure CRON_SECRET token
- [ ] Add CRON_SECRET to hosting environment variables
- [ ] Set up cron job on your hosting platform
- [ ] Test endpoint manually with curl
- [ ] Monitor logs for first successful execution
- [ ] Verify user balances are updating
- [ ] Check transactions table for income records

---

## 📞 Need Help?

If you're still having issues:

1. Check application logs for error messages
2. Test the endpoint manually with curl
3. Verify database has active packages: `SELECT * FROM user_package WHERE is_active = true;`
4. Ensure income interval (24 hours) has passed since last payout

---

**Remember:** The cron job is **essential** for production. Without it, income payouts will **not work** on hosted platforms.
