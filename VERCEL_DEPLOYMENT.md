# 🚀 Deploying to Vercel

## Quick Setup Guide

Vercel is a serverless platform. Your Flask app has been configured for Vercel deployment.

## ✅ Pre-Deployment Checklist

### Files Already Created:
- ✅ [vercel.json](vercel.json) - Vercel configuration
- ✅ [requirements.txt](requirements.txt) - Python dependencies
- ✅ [app.py](app.py) - Main Flask application (auto-initializes database)

## 📋 Deployment Steps

### Option 1: Deploy via Vercel CLI (Recommended)

1. **Install Vercel CLI**
   ```powershell
   npm install -g vercel
   ```

2. **Login to Vercel**
   ```powershell
   vercel login
   ```

3. **Deploy**
   ```powershell
   vercel
   ```
   
   Follow the prompts:
   - Set up and deploy? **Y**
   - Which scope? (Select your account)
   - Link to existing project? **N** (first time)
   - Project name? (Press enter for default or type a name)
   - In which directory is your code located? **./`** (current directory)

4. **Set Environment Variables**
   ```powershell
   vercel env add SECRET_KEY
   ```
   When prompted, paste your secret key (generate one below)

5. **Deploy to Production**
   ```powershell
   vercel --prod
   ```

### Option 2: Deploy via Vercel Dashboard

1. **Go to [vercel.com](https://vercel.com)**
   - Sign in with GitHub/GitLab/Bitbucket

2. **Import Your Repository**
   - Click "Add New" → "Project"
   - Import your Git repository
   - Or drag and drop your project folder

3. **Configure Project**
   - Framework Preset: **Other**
   - Root Directory: **./`** (leave as is)
   - Build Command: (leave empty)
   - Output Directory: (leave empty)

4. **Set Environment Variables**
   Click "Environment Variables" and add:
   ```
   SECRET_KEY = your-generated-secret-key
   FLASK_ENV = production
   ```

5. **Deploy**
   - Click "Deploy"
   - Wait for deployment to complete
   - You'll get a URL like: `your-app.vercel.app`

## 🔑 Generate Secret Key

Run this command to generate a secure secret key:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and use it as your `SECRET_KEY` environment variable.

## ⚙️ Environment Variables

Set these in the Vercel dashboard or via CLI:

| Variable | Value | Required |
|----------|-------|----------|
| `SECRET_KEY` | (generated secret) | ✅ Yes |
| `FLASK_ENV` | `production` | ✅ Yes |
| `MINIMUM_WITHDRAWAL` | `2200` | Optional |
| `WITHDRAWAL_FEE_PERCENTAGE` | `11` | Optional |

### Setting via CLI:
```powershell
vercel env add SECRET_KEY production
vercel env add FLASK_ENV production
```

### Setting via Dashboard:
1. Go to your project settings
2. Click "Environment Variables"
3. Add each variable
4. Redeploy: `vercel --prod`

## 🗄️ Database on Vercel

### Important Notes:

1. **SQLite Limitations on Vercel:**
   - Vercel is serverless - each request may run on a different server
   - SQLite files are NOT persistent between deployments
   - For production, use a cloud database (see below)

2. **For Testing (SQLite):**
   - Works for testing purposes
   - Data will be lost on redeploy
   - OK for demo/development

3. **For Production (Recommended):**
   Use a cloud database service:

### Option A: Supabase (Free PostgreSQL)
```powershell
# Add to environment variables
DATABASE_URL=postgresql://user:password@host:5432/database
```
[Setup Guide](https://supabase.com/)

### Option B: PlanetScale (Free MySQL)
```powershell
DATABASE_URL=mysql://user:password@host/database
```
[Setup Guide](https://planetscale.com/)

### Option C: Railway (PostgreSQL)
```powershell
DATABASE_URL=postgresql://user:password@host:5432/database
```
[Setup Guide](https://railway.app/)

### Option D: Neon (Serverless PostgreSQL)
```powershell
DATABASE_URL=postgresql://user:password@host/database
```
[Setup Guide](https://neon.tech/)

## 📝 Update Your App for PostgreSQL (If Using)

If you choose a PostgreSQL database, add `psycopg2-binary` to requirements:

```powershell
echo psycopg2-binary==2.9.9 >> requirements.txt
```

The app will automatically detect `DATABASE_URL` and use PostgreSQL!

## ✅ Verify Deployment

After deployment:

1. **Test Homepage**
   - Visit your Vercel URL
   - Should see the landing page

2. **Test Registration**
   - Go to `/register`
   - Create a test account
   - Should see success message

3. **Test Login**
   - Login with test account
   - Should see dashboard

4. **Check Logs**
   ```powershell
   vercel logs
   ```

## 🔍 Troubleshooting

### Issue: "Internal Server Error"

**Check Logs:**
```powershell
vercel logs --follow
```

**Common Causes:**
1. Missing `SECRET_KEY` environment variable
2. Database not initialized (should auto-initialize on first request)
3. Missing dependencies in `requirements.txt`

### Issue: "Module Not Found"

**Solution:** Make sure all dependencies are in `requirements.txt`
```powershell
pip freeze > requirements.txt
vercel --prod
```

### Issue: "Database Locked" or "No Such Table"

**Solution:** This happens with SQLite on serverless. Use a cloud database:
1. Sign up for Supabase (free)
2. Get PostgreSQL connection string
3. Add to Vercel environment variables as `DATABASE_URL`
4. Redeploy: `vercel --prod`

### Issue: Static Files Not Loading

**Solution:** Vercel should serve them automatically. If not:
1. Check [vercel.json](vercel.json) routes configuration
2. Make sure files are in `/static` folder
3. Redeploy

### Issue: "Secret Key Not Set"

**Solution:**
```powershell
# Generate key
python -c "import secrets; print(secrets.token_hex(32))"

# Add to Vercel
vercel env add SECRET_KEY production
# Paste the generated key when prompted

# Redeploy
vercel --prod
```

## 🎯 Recommended Setup for Production

For the best production experience on Vercel:

1. **Use GitHub Integration**
   - Push code to GitHub
   - Connect repository to Vercel
   - Auto-deploy on every push

2. **Use Cloud Database**
   - Supabase (PostgreSQL) - Recommended
   - Free tier: 500MB storage, 2GB bandwidth
   - Persistent and reliable

3. **Set Up Domains**
   - Add custom domain in Vercel dashboard
   - SSL certificate automatically provided

4. **Enable Analytics**
   - Go to project settings
   - Enable Vercel Analytics
   - Monitor performance

## 📊 Deployment Workflow

### Initial Setup:
```powershell
# 1. Install Vercel CLI
npm install -g vercel

# 2. Login
vercel login

# 3. Deploy
vercel

# 4. Set environment variables
python -c "import secrets; print(secrets.token_hex(32))"
vercel env add SECRET_KEY production
# Paste the secret key

# 5. Deploy to production
vercel --prod
```

### Subsequent Updates:
```powershell
# Make your changes
# Then deploy
vercel --prod
```

Or with Git:
```powershell
git add .
git commit -m "Update message"
git push
# Vercel auto-deploys if connected to Git
```

## 🚀 Quick Commands

```powershell
# Deploy to preview
vercel

# Deploy to production
vercel --prod

# View logs
vercel logs

# View logs (live)
vercel logs --follow

# List deployments
vercel ls

# Open project in browser
vercel open

# Remove deployment
vercel remove [deployment-url]
```

## 🔐 Security Checklist

Before going live:

- [ ] Set `SECRET_KEY` environment variable (not default)
- [ ] Set `FLASK_ENV=production`
- [ ] Use cloud database (not SQLite)
- [ ] Enable HTTPS (Vercel does this automatically)
- [ ] Review admin credentials
- [ ] Test all features (register, login, deposit, withdrawal)

## 📈 Performance Tips

1. **Use PostgreSQL** instead of SQLite for better concurrent access
2. **Enable Caching** for static assets (Vercel does this automatically)
3. **Monitor** with Vercel Analytics
4. **Optimize** database queries if response is slow

## 🆘 Getting Help

- **Vercel Docs:** https://vercel.com/docs
- **Check logs:** `vercel logs --follow`
- **Support:** https://vercel.com/support

## 🎉 You're Ready!

Your app is now configured for Vercel. Just run:

```powershell
vercel --prod
```

And you're live! 🚀

---

**Next Steps:**
1. Deploy: `vercel --prod`
2. Set SECRET_KEY environment variable
3. (Optional) Set up cloud database for production
4. Test registration and login
5. Share your Vercel URL!
