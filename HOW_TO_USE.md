# How to Use - Personal Finance Assistant

## First Time Setup

### 1. Install MongoDB

**Option A - Local (Easiest)**
- Download from: https://www.mongodb.com/try/download/community
- Install with default settings
- It will run automatically on `mongodb://localhost:27017/`

**Option B - Cloud (MongoDB Atlas)**
- Sign up at: https://www.mongodb.com/cloud/atlas
- Create a free cluster
- Get your connection string
- Set it as environment variable (see below)

### 2. Install Python Packages

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
python src/main.py
```

## Using a Custom MongoDB Connection

If you're using MongoDB Atlas or a custom MongoDB server:

**Windows PowerShell:**
```powershell
$env:MONGODB_URI="your-connection-string-here"
python src/main.py
```

**Windows CMD:**
```cmd
set MONGODB_URI=your-connection-string-here
python src/main.py
```

**Linux/Mac:**
```bash
export MONGODB_URI=your-connection-string-here
python src/main.py
```

## Basic Workflow

### Initial Setup (First Time)

1. **Set Savings Goal**
   - Menu: `[5] Settings & Goals`
   - Select: `[1] Set Savings Goal`
   - Enter percentage (e.g., 20 means save 20% of income)

### Adding Data

2. **Add Income**
   - Menu: `[1] Income Management`
   - Select: `[1] Add Income Entry`
   - Enter: amount, source (e.g., "Salary"), date, description

3. **Add One-Time Expenses**
   - Menu: `[2] Expense Management`
   - Select: `[1] Add Expense`
   - Enter: amount, category, date, description

4. **Add Recurring Expenses** (rent, subscriptions, etc.)
   - Menu: `[2] Expense Management`
   - Select: `[2] Add Recurring Expense`
   - Enter: amount, category, description, frequency (monthly/weekly/yearly)

5. **Add Investments**
   - Menu: `[3] Investment Management`
   - Select: `[1] Add Investment`
   - Enter: name, amount, type, purpose, date

### Monthly Routine

**Beginning of Month:**
1. Go to `[2] Expense Management` → `[6] Process Recurring Expenses`
   - This applies your recurring expenses for the current month
2. Add your monthly income

**During the Month:**
- Add expenses as they happen
- Update investment values when needed

**End of Month:**
- Check dashboard `[4]` to see how you did
- See if you met your savings goal

### Viewing Your Data

**Dashboard (Most Important)**
- Menu: `[4] Financial Dashboard`
- Shows:
  - Current month income vs expenses
  - Savings rate (actual vs goal)
  - All-time summary
  - Investment performance
  - Expense breakdown
  - Financial health indicators

**Income Reports**
- Menu: `[1] Income Management`
- Options:
  - `[2]` View all income entries
  - `[3]` View income summary with statistics

**Expense Reports**
- Menu: `[2] Expense Management`
- Options:
  - `[3]` View all expenses
  - `[4]` View expenses by category
  - `[5]` View recurring expenses

**Investment Reports**
- Menu: `[3] Investment Management`
- Options:
  - `[2]` View all investments
  - `[3]` View by purpose
  - `[4]` View summary
  - `[5]` Update investment value

## Example Session

```
1. First run - set savings goal to 20%
2. Add income: $3000, "Salary", today
3. Add recurring expenses:
   - $1000, "Housing", "Rent", Monthly
   - $100, "Utilities", "Internet", Monthly
   - $15, "Entertainment", "Netflix", Monthly
4. Add one-time expense: $80, "Food", "Groceries", today
5. Add investment: "Emergency Fund", $5000, "Savings Account", "Emergency Fund", today
6. Check dashboard - see that you're saving well!
```

## Understanding the Dashboard

When you view the dashboard `[4]`, you'll see:

**Current Month Summary**
- Income this month
- Expenses this month
- Net (income - expenses)
- Savings rate (net / income)

**Savings Goal Check**
- Your target: e.g., 20%
- Your actual: e.g., 25%
- Status: "GOAL MET!" or "Below target"

**All-Time Summary**
- Total income ever
- Total expenses ever
- Net savings

**Investment Summary** (if you have investments)
- Total invested
- Current value
- Gains/losses

**Expense Breakdown**
- Top 5 categories this month
- Percentage of total for each

**Financial Health**
- Expense-to-income ratio
- Emergency fund coverage (months)
- Tips for improvement

## Tips for Success

1. **Be Consistent** - Enter data regularly (daily or weekly)
2. **Use Categories** - Always categorize expenses the same way
3. **Set Realistic Goals** - Start with 10-15% savings if 20% is too hard
4. **Build Emergency Fund** - Aim for 3-6 months of expenses
5. **Update Investments** - Check values monthly or quarterly
6. **Review Dashboard** - Check weekly to stay on track

## Common Questions

**Q: What if I forget to add an expense?**
A: You can backdate it - just enter the correct date when adding.

**Q: How do I delete an entry?**
A: Currently not supported in the UI. You can use MongoDB Compass to edit the database directly.

**Q: Can I export my data?**
A: You can use MongoDB Compass or mongodump to export. CSV export feature coming soon.

**Q: What's the difference between recurring and one-time expenses?**
A: 
- Recurring: Templates for bills that repeat (rent, subscriptions)
- One-time: Actual expenses that happened once (groceries, shopping)

**Q: When should I process recurring expenses?**
A: At the start of each month. This creates actual expense entries from your templates.

## Troubleshooting

**Can't connect to MongoDB?**
- Make sure MongoDB is running
- Check connection string
- Default is `mongodb://localhost:27017/`

**No data showing up?**
- Make sure you've added data first
- Check you're connected to the right database

**Error installing pymongo?**
- Make sure pip is updated: `pip install --upgrade pip`
- Try: `pip install pymongo`

## Need More Help?

- Read: `README.md` for overview
- Read: `docs/QUICKSTART.md` for detailed walkthrough
- Read: `docs/TECHNICAL.md` for technical details
