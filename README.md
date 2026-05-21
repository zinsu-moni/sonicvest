# Fintech Finance User Panel

> **🚀 PRODUCTION READY**: Registration server error fix applied! The app now auto-initializes the database on first request. See [QUICK_FIX_GUIDE.md](QUICK_FIX_GUIDE.md) for deployment instructions.

A responsive, blue-themed web platform where users can register, log in, buy packages, earn daily income, withdraw funds, and get referral commissions.

## Features

- **User Registration & Login**
  - Register with name, email, phone, password, referral code (optional)
  - Login/logout system with session handling
  - Password hashing (bcrypt)

- **Dashboard**
  - Show active packages
  - Countdown to next daily income drop (22 hours)
  - Total earnings
  - Withdrawable balance
  - Welcome bonus for new users

- **Investment Packages**
  - List all packages (price, daily income, total income, duration)
  - Purchase packages through manual or automatic payment options

- **Daily Check-in Bonus**
  - Claim ₦200 bonus once every 24 hours

- **Automated Earnings**
  - Background job runs every 22 hours
  - Credits daily income to user balance
  - Marks packages as expired after 35 days

- **Multi-Level Referrals**
  - 3-level referral commissions:
    - Level 1: 24%
    - Level 2: 4%
    - Level 3: 2%
  - Referral link and tree visualization

- **Withdrawals**
  - Minimum withdrawal ₦1,000
  - Bank withdrawal request form
  - Status tracking for withdrawal requests

- **Transaction History**
  - Track deposits, withdrawals, commissions, and bonuses
  - Filter and sort capabilities

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript (vanilla)
- **Backend**: Python with Flask
- **Database**: PostgreSQL (SQLite for local development)
- **Task Processing**: Background worker thread

## Installation and Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/fintech-finance.git
   cd fintech-finance
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

5. Run the application:
   ```
   flask run
   ```

6. **IMPORTANT**: Start the income distribution worker (in a separate terminal):
   ```
   python worker.py
   ```
   
   This runs the background process that distributes daily income to users.

7. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Welcome Email Configuration

To send a welcome email after user registration, add these variables to your `.env` file:

```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@example.com
MAIL_PASSWORD=your-app-password
MAIL_SENDER_NAME=Max Wealth
APP_BASE_URL=https://maxwealth.pxxl.click
```

Notes:
- Use an app password for Gmail (not your normal account password).
- If these values are not configured, registration still works but email delivery may fail.

### Testing the Worker

To verify the income distribution is working:
```
python test_worker.py
```

This will show all active packages and test the payout system.

## Production Deployment

### ⚠️ CRITICAL: Worker Process Setup

The income distribution **requires a separate worker process** to run in production. Without this, users won't receive their daily income!

**Quick Setup:**

1. **Deploy your code** to your hosting platform (Heroku, Render, Railway, etc.)

2. **Enable the worker dyno/process**:
   
   For Heroku:
   ```bash
   heroku ps:scale worker=1
   ```
   
   For other platforms: Add a worker/background service that runs `python worker.py`

3. **Verify it's running**:
   ```bash
   heroku logs --tail --dyno=worker
   ```
   
   You should see: `🚀 INCOME DISTRIBUTION WORKER STARTED`

📖 **Full deployment guide**: See [HOSTING_SETUP.md](HOSTING_SETUP.md) for detailed instructions for all platforms.

### Environment Variables

Make sure these are set in production:
- `DATABASE_URL` - PostgreSQL connection string
- `SECRET_KEY` - Flask secret key
- `GTR_API_KEY` - Payment gateway API key
- `GTR_SECRET_KEY` - Payment gateway secret

## Troubleshooting

### Income not distributing?
- Check if worker process is running (see [HOSTING_SETUP.md](HOSTING_SETUP.md))
- Verify 24 hours have passed since package purchase
- Check worker logs for errors
- Run `python test_worker.py` locally to test

### Database errors?
- Ensure PostgreSQL is properly configured
- Check DATABASE_URL environment variable
- Run `python init_production_db.py` to initialize tables

## Project Structure

```
fintech/
├── app.py                  # Main application file
├── models/                 # Database models
│   ├── user.py
│   ├── package.py
│   ├── transaction.py
│   └── payment.py
├── controllers/            # Route controllers
│   ├── auth_controller.py
│   ├── dashboard_controller.py
│   ├── package_controller.py
│   ├── referral_controller.py
│   ├── transaction_controller.py
│   └── withdrawal_controller.py
├── static/                 # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── templates/              # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── auth/
│   ├── dashboard/
│   ├── package/
│   ├── referral/
│   └── withdrawal/
└── requirements.txt        # Project dependencies
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributors

- Your Name - Initial work

## Acknowledgments

- Hat tip to anyone whose code was used
- Inspiration
- etc.
