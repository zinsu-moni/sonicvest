# ✅ Income Payout Fix - Quick Start Checklist

## What's Wrong?
Your income payout system doesn't work on PXXL.app because production servers don't run background threads. You need a cron job.

## 🚀 Fix It Now (5 Minutes)

### Step 1: Generate Secret Token
Run this command locally:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```
Copy the output (example: `xK9mP2nQ8vR5tY7uE1wA3sD6fG4hJ0lZ`)

---

### Step 2: Add to PXXL.app Environment Variables
1. Go to PXXL.app dashboard
2. Click on your app → Settings → Environment Variables
3. Add new variable:
   - **Name:** `CRON_SECRET`
   - **Value:** (paste the token you generated)
4. **Restart your app** (important!)

---

### Step 3: Set Up Cron Job in PXXL.app Dashboard

#### PXXL.app Built-in Cron (Recommended - Easiest!) ⭐
1. Go to your PXXL.app dashboard
2. Select your app → Navigate to **"Cron Jobs"** or **"Scheduled Tasks"**
3. Click **"Add New Cron Job"** or **"Create Cron"**
4. Fill in:
   - **Name:** `Income Payout Processor`
   - **Command/URL:** `/cron/process-income-payouts?token=$CRON_SECRET`
     - **Important:** Use `$CRON_SECRET` exactly - PXXL will replace it automatically
   - **Schedule:** `0 * * * *` (every hour) or select "Every hour" from dropdown
   - **Method:** GET (if asked)
   - **Enabled:** ✓ Check this box
5. Click **"Save"** or **"Create"**
6. Done! The cron job will run automatically

**Why use PXXL's built-in cron?**
- ✅ No external service needed
- ✅ Environment variables work automatically
- ✅ Built-in monitoring and logs
- ✅ More reliable
- ✅ Completely free

#### Alternative: External Service (If needed)
If you can't find the Cron Jobs section in PXXL dashboard:

**Option: cron-job.org (FREE)**
1. Go to: https://cron-job.org/en/signup
2. Sign up and create cronjob
3. Use URL: `https://your-app.pxxl.app/cron/process-income-payouts?token=YOUR_CRON_SECRET`
   - Replace `YOUR_CRON_SECRET` with actual token from Step 1
4. Schedule: Every hour

---

### Step 4: Test It
Open this URL in your browser (replace with your values):
```
https://your-app.pxxl.app/cron/process-income-payouts?token=YOUR_CRON_SECRET
```

**✅ Success looks like:**
```json
{
  "success": true,
  "processed": 3,
  "timestamp": "2026-02-12T10:30:00",
  "total_active_packages": 5
}
```

**❌ If you see this, your token is wrong:**
```json
{
  "success": false,
  "error": "Unauthorized - Invalid or missing token"
}
```

---

## ✅ Done! Now What?

### Monitor It:
- Check PXXL.app dashboard → **Cron Jobs** section for execution history
- Look for successful runs (green status or HTTP 200)
- Check Application Logs for "Cron job processed" messages
- Enable email notifications in PXXL if available

### Verify It's Working:
1. Log into your app as a user
2. Check if balance increases after 24 hours
3. Look at transaction history for "Daily income" entries

### When Does Income Drop?
- Every 24 hours after package purchase
- Cron job checks every 30-60 minutes
- If 24+ hours have passed, income is paid out

---

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Unauthorized" error | Double-check `CRON_SECRET` in PXXL.app matches URL token |
| Cron runs but no payouts | Verify users have active packages and 24 hours have passed |
| Can't access endpoint | Make sure your app is deployed and running on PXXL.app |
| Database errors | Check `DATABASE_URL` is set correctly in PXXL.app |

---

## 📚 Need More Details?
- **Full Setup Guide:** [PXXL_INCOME_SETUP.md](PXXL_INCOME_SETUP.md)
- **All Platforms Guide:** [CRON_SETUP_GUIDE.md](CRON_SETUP_GUIDE.md)

---

## 🎯 Checklist
- [ ] Generated CRON_SECRET token
- [ ] Added CRON_SECRET to PXXL.app environment variables
- [ ] Restarted app on PXXL.app
- [ ] Created cron job in PXXL dashboard (or external service)
- [ ] Cron job is enabled and scheduled
- [ ] Tested endpoint and got success response
- [ ] Can see cron job in PXXL Cron Jobs section
- [ ] Waiting 24 hours to verify first payout

**That's it! Your income payouts will now work automatically! 🎉**
