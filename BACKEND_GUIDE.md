# Fintech Backend - Dual Balance System

## 🏗️ Architecture Overview

The new backend has been built from scratch with a clean, simple Flask application featuring a **dual balance system** as requested.

## 💰 Dual Balance System

### 1. **Recharge Balance** (`recharge_balance`)
- **Purpose**: For deposits and investments
- **Use Cases**:
  - Money deposited by users
  - Used to purchase investment packages
  - Cannot be withdrawn directly

### 2. **Main Balance** (`main_balance`) 
- **Purpose**: For earnings and withdrawals
- **Use Cases**:
  - Daily income from investments
  - Referral commissions
  - Welcome bonuses
  - Available for withdrawal

## 📊 Balance Methods

### Recharge Balance Operations
```python
user.add_recharge_balance(amount, description)     # Add money (deposits)
user.deduct_recharge_balance(amount, description)  # Deduct money (investments)
```

### Main Balance Operations
```python
user.add_main_balance(amount, description)       # Add money (earnings)
user.deduct_main_balance(amount, description)    # Deduct money (withdrawals)
```

## 🔄 Transaction Flow

1. **User Deposits Money** → `recharge_balance` increases
2. **User Invests in Package** → `recharge_balance` decreases, creates `UserPackage`
3. **Daily Income Generated** → `main_balance` increases
4. **User Withdraws Money** → `main_balance` decreases

## 📁 File Structure

```
app.py              # Main Flask application
init_db.py          # Database initialization
requirements.txt    # Dependencies
fintech.db         # SQLite database
templates/         # HTML templates (preserved)
static/           # CSS/JS/Images (preserved)
```

## 🎯 Key Features

### Models
- **User**: Dual balance system, referrals, authentication
- **Package**: Investment packages with daily returns
- **UserPackage**: User's active investments
- **Transaction**: All financial transactions with balance type tracking
- **Withdrawal**: Withdrawal requests

### Routes
- `/auth/login` - User authentication
- `/auth/register` - User registration with welcome bonus
- `/dashboard` - Main dashboard with balance overview
- `/packages` - View available investment packages
- `/packages/buy/<id>` - Purchase investment packages
- `/deposit` - Add money to recharge balance
- `/withdrawal` - Request withdrawals from main balance
- `/referral` - Referral system
- `/transactions` - Transaction history

## 🚀 Getting Started

1. **Dependencies are installed**: Flask, SQLAlchemy, etc.
2. **Database is initialized**: Run `python init_db.py`
3. **Application is running**: `python app.py`

## 👤 Demo Account

- **Email**: demo@fintech.com
- **Password**: password123
- **Recharge Balance**: 10,000.00
- **Main Balance**: 1,500.00

## 💡 Balance System Benefits

1. **Clear Separation**: Investment money vs. withdrawal money
2. **Fraud Prevention**: Users can't withdraw deposited money directly
3. **Investment Tracking**: Clear flow from deposit → investment → earnings
4. **Transaction Transparency**: All movements tracked with balance type

The application is now running at http://localhost:5000 with a clean, working dual balance system!
