# Quick Start Guide - Personal Finance Assistant

## First Time Setup

### Step 1: Install MongoDB

**Option A: Local Installation (Recommended for beginners)**
1. Download MongoDB Community Server: https://www.mongodb.com/try/download/community
2. Install with default settings
3. MongoDB will run on `mongodb://localhost:27017/`

**Option B: MongoDB Atlas (Cloud - Free tier available)**
1. Create account at https://www.mongodb.com/cloud/atlas
2. Create a free cluster
3. Get your connection string
4. Set environment variable: `set MONGODB_URI=your-connection-string`

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python main.py
```

## First Use Walkthrough

### 1. Set Your Savings Goal
- Go to: **[5] Settings & Goals**
- Select: **[1] Set Savings Goal**
- Enter a percentage (e.g., 20 for 20%)

### 2. Add Your Income
- Go to: **[1] Income Management**
- Select: **[1] Add Income Entry**
- Enter your monthly salary or other income

### 3. Add Expenses
- Go to: **[2] Expense Management**
- Select: **[1] Add Expense** for one-time expenses
- Select: **[2] Add Recurring Expense** for monthly bills

### 4. Set Up Recurring Expenses
Add your regular monthly expenses:
- Rent/Mortgage
- Utilities
- Subscriptions (Netflix, Spotify, etc.)
- Insurance payments
- Loan payments

### 5. Track Your Investments
- Go to: **[3] Investment Management**
- Select: **[1] Add Investment**
- Add each investment with its purpose:
  - Emergency Fund
  - Retirement
  - House Down Payment
  - etc.

### 6. View Your Financial Dashboard
- Go to: **[4] Financial Dashboard**
- See your complete financial overview
- Check if you're meeting your savings goal
- Get personalized financial tips

## Monthly Routine

### Beginning of Month:
1. Process recurring expenses: **[2] → [6]**
2. Add your monthly income: **[1] → [1]**

### Throughout the Month:
- Add expenses as they occur: **[2] → [1]**
- Update investment values: **[3] → [5]**

### End of Month:
- Check your dashboard: **[4]**
- Review if you met your savings goal
- Adjust budget if needed

## Tips for Success

1. **Be Consistent**: Enter expenses daily or weekly
2. **Categorize Accurately**: Use consistent categories
3. **Review Regularly**: Check dashboard weekly
4. **Update Investments**: Monthly or quarterly updates
5. **Set Realistic Goals**: Start with 10-15% savings rate
6. **Build Emergency Fund**: Aim for 3-6 months of expenses

## Common Categories

### Expense Categories:
- Housing (rent, mortgage, property tax)
- Food (groceries, dining out)
- Transportation (car payment, gas, public transit)
- Utilities (electricity, water, internet)
- Healthcare (insurance, medications, doctor visits)
- Entertainment (movies, hobbies, subscriptions)
- Shopping (clothes, electronics, household items)
- Education (courses, books, tuition)
- Insurance (health, car, life, home)
- Debt (credit cards, loans)
- Savings (transfers to savings accounts)

### Investment Types:
- Stocks
- Bonds
- ETF (Exchange Traded Funds)
- Mutual Funds
- Real Estate
- Cryptocurrency
- Savings Account
- CD (Certificate of Deposit)
- Retirement Account (401k, IRA)

### Investment Purposes:
- Retirement (long-term growth)
- Emergency Fund (3-6 months expenses)
- House Down Payment
- Education Fund
- Vacation Fund
- Short-term Savings (<1 year)
- Long-term Growth (>5 years)
- Passive Income (dividends, rental income)

## Troubleshooting

### Can't connect to MongoDB?
- Make sure MongoDB is running: `mongod --version`
- Check connection string in environment variable
- For local: Use `mongodb://localhost:27017/`

### Lost data?
- MongoDB stores data persistently
- Check your database: Use MongoDB Compass or mongo shell
- Database name: `personal_finance`

### Want to migrate from JSON?
- Export your JSON data
- Import into MongoDB using a migration script
- Contact support or check documentation

## Security Recommendations

1. **Use authentication** for MongoDB in production
2. **Backup regularly** - MongoDB Atlas has automatic backups
3. **Don't share** your `.env` file or connection strings
4. **Use strong passwords** for MongoDB users
5. **Enable encryption** for MongoDB Atlas connections

## Need Help?

- Read the full README.md for detailed information
- Check MongoDB documentation: https://docs.mongodb.com/
- Review the code comments for technical details
