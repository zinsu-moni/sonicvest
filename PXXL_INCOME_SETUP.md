# 🚀 Income Payout Setup for PXXL.app

## ⚠️ CRITICAL: Income Payouts Won't Work Without This Setup

Your income payout system is currently **not working** in production because PXXL.app (like all production hosts) doesn't run the background thread. You **must** set up an external cron job.

---

## 🔧 Quick Setup (3 Steps)

### Step 1: Set CRON_SECRET Environment Variable

1. Generate a secure token:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

2. Copy the generated token

3. Go to your PXXL.app dashboard → Environment Variables

4. Add new variable:
   - **Name:** `CRON_SECRET`
   - **Value:** (paste the generated token)

5. Restart your app

---

### Step 2: Set Up Cron Job in PXXL.app Dashboard

PXXL.app has **built-in cron job support**! This is the easiest and most reliable method.

#### **Using PXXL.app's Built-in Cron (Recommended):**

1. Go to your PXXL.app dashboard

2. Select your application

3. Navigate to **"Cron Jobs"** or **"Scheduled Tasks"** section

4. Click **"Add New Cron Job"** or **"Create Cron"**

5. Fill in the details:
   - **Name/Title:** `Income Payout Processor`
   - **Command/URL:** `/cron/process-income-payouts?token=$CRON_SECRET`
     - **Note:** Use `$CRON_SECRET` - PXXL will automatically inject the environment variable
   - **Schedule/Frequency:** 
     - **Cron Expression:** `0 * * * *` (every hour) 
     - **OR Simple Schedule:** "Every hour" or "Every 30 minutes"
   - **Method:** GET (if asked)
   - **Enabled:** ✓ Yes

6. **Save** the cron job

7. The cron will automatically start running on schedule!

**Benefits of using PXXL's built-in cron:**
- ✅ No external service needed
- ✅ Uses environment variables automatically
- ✅ More reliable (same infrastructure)
- ✅ Better performance (no external network calls)
- ✅ Built-in monitoring and logs

---

#### **Alternative: External Cron Service (If PXXL cron is unavailable)**

If for some reason you can't access PXXL's cron feature:

**Option: cron-job.org (Free)**
1. Go to [https://cron-job.org](https://cron-job.org)
2. Sign up and create job
3. URL: `https://your-app.pxxl.app/cron/process-income-payouts?token=YOUR_CRON_SECRET`
4. Schedule: Every hour

---

### Step 3: Test Your Setup

Test the endpoint manually:

```bash
# Replace YOUR_APP and YOUR_TOKEN with actual values
curl "https://your-app.pxxl.app/cron/process-income-payouts?token=YOUR_CRON_SECRET"
```

**Expected success response:**
```json
{
  "success": true,
  "processed": 5,
  "timestamp": "2026-02-12T10:30:00",
  "total_active_packages": 10
}
```

**If token is wrong, you'll get:**
```json
{
  "success": false,
  "error": "Unauthorized - Invalid or missing token"
}
```

---

## 🔍 Monitoring

### Check if it's working:

1. **Via PXXL.app Cron Logs:**
   - Go to your app dashboard → **Cron Jobs** section
   - View execution history for your cron job
   - Check for successful runs (HTTP 200 status)
   - Look for any error messages

2. **Via PXXL.app Application Logs:**
   - Go to your app dashboard
   - Open "Logs" or "Console" tab
   - Look for: `✅ Cron job processed X income payouts`
   - Filter by date/time to find recent executions

3. **Via Your Application:**
   - Log in as user with active package
   - Check if balance increases every 24 hours
   - Check transaction history for "Daily income" entries

4. **Manual Test:**
   - Visit the endpoint in browser to test immediately
   - Should return JSON with execution details

---

## 📊 Recommended Cron Frequency

Your system drops income every **24 hours** (`INCOME_DROP_HOURS = 24.0`).

**Best practice:**
- **Every 1 hour:** `0 * * * *` ✅ Recommended
- **Every 30 minutes:** `*/30 * * * *` (more frequent checks)
- **Every 2 hours:** `0 */2 * * *` (lighter load)

Don't run it too frequently (every 5 minutes) as it wastes resources.

---

## ❓ Troubleshooting

### Issue: "Unauthorized - Invalid token"

**Solution:**
- Verify `CRON_SECRET` is set in PXXL.app environment variables
- Ensure token in URL exactly matches the environment variable
- No extra spaces or quotes in either place
- Restart app after setting environment variable

### Issue: Database connection errors

**Solution:**
- PXXL.app free tier may have connection limits
- Verify `DATABASE_URL` is correct in environment variables
- Check database isn't sleeping (connect to it via psql first)

### Issue: Cron runs but no payouts happen

**Solution:**
- Check if users have active packages (query database)
- Verify 24 hours have passed since last payout
- Check package `end_date` hasn't expired
- Look at `last_payout` field in `user_package` table

### Issue: Can't see logs in PXXL.app

**Solution:**
- Check **Cron Jobs** section for execution history
- View **Application Logs** tab in dashboard
- Look at cron job status (success/failure indicators)
- If still no logs, test endpoint manually in browser

---

## 🔒 Security Checklist

- [x] `CRON_SECRET` environment variable is set
- [x] Token is long and random (32+ characters)
- [x] Using HTTPS URL (not HTTP)
- [ ] Only cron service knows the token
- [ ] Rotate token every 3-6 months

---

## 🎯 Quick Verification

After setup, verify everything works:

1. ✅ Cron job created in PXXL dashboard and enabled
2. ✅ Cron job shows in "Scheduled Tasks" or "Cron Jobs" section
3. ✅ Test endpoint returns success (JSON with "success": true)
4. ✅ PXXL cron execution history shows successful runs
5. ✅ Application logs show "Cron job processed X income payouts"
6. ✅ User balances increase after 24 hours
7. ✅ Transaction records are created with type "package_income"

---

## 📞 Still Having Issues?

### Debug Steps:

1. **Test endpoint directly in browser:**
   ```
   https://your-app.pxxl.app/cron/process-income-payouts?token=YOUR_TOKEN
   ```
   Should return JSON response

2. **Check database has active packages:**
   ```sql
   SELECT * FROM user_package WHERE is_active = true AND end_date > NOW();
   ```

3. **Check last payout times:**
   ```sql
   SELECT id, user_id, last_payout, created_at 
   FROM user_package 
   WHERE is_active = true;
   ```

4. **Verify users have packages:**
   - Log in to admin panel: `https://your-app.pxxl.app/admin/login`
   - Check user packages section

---

## 💡 Why This Is Necessary

PXXL.app uses **Gunicorn** or similar WSGI servers in production. These servers:
- Don't execute the `if __name__ == '__main__':` block in your Python code
- Don't support long-running background threads
- Restart workers periodically, killing any background threads

**The solution:** Use **scheduled cron jobs** (either PXXL's built-in cron or external services) to trigger the income payout endpoint at regular intervals. This is the standard approach for all production Python web applications.

---

## ✅ You're All Set!

Once configured:
- Income payouts will process automatically every hour
- Users will receive daily income on schedule
- System runs reliably without manual intervention
- You can monitor via cron service dashboard

**Remember:** Always keep your `CRON_SECRET` secure and never commit it to version control!
