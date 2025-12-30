# Personal Finance Assistant (PFA)

A comprehensive command-line tool to manage your personal finances, track income and expenses, manage investments, and monitor your savings goals. Uses MongoDB for secure and scalable data storage.

## Features

### Income Management
- Add income entries with source, amount, date, and description
- View all income entries
- View income summary with statistics
- Track income by source

### Expense Management
- Add one-time expenses with categories
- Create recurring expenses (monthly, weekly, yearly)
- View expenses by category
- Process recurring expenses automatically
- 12 predefined expense categories

### Investment Management
- Track multiple investments with types and purposes
- Monitor investment performance (gains/losses)
- Categorize investments by purpose (retirement, emergency fund, etc.)
- Update investment values
- View portfolio summary

### Financial Dashboard
- View current month summary
- Track savings rate vs. your goal
- All-time financial overview
- Expense breakdown by category
- Financial health indicators
- Emergency fund check
- Personalized tips and recommendations

### Settings & Goals
- Set savings goal as percentage of income
- Track progress toward savings goals
- Automatic goal achievement tracking

## Project Structure

```
PFA/
├── src/               # Source code
│   ├── main.py        # Main application
│   ├── data_manager.py    # MongoDB interface
│   ├── income.py      # Income tracking
│   ├── expenses.py    # Expense tracking
│   ├── investments.py # Investment management
│   └── dashboard.py   # Financial dashboard
├── docs/              # Documentation
│   ├── QUICKSTART.md  # Getting started guide
│   └── TECHNICAL.md   # Technical documentation
├── config/            # Configuration
│   └── .env.example   # Environment template
├── README.md          # This file
├── requirements.txt   # Python dependencies
└── .gitignore        # Git ignore rules
```

## Installation

### Prerequisites
- Python 3.8 or higher
- MongoDB (local installation or MongoDB Atlas cloud service)

### Setup

1. **Install MongoDB**:
   - **Local**: Download from [mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)
   - **Cloud**: Create free account at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)

2. **Clone this repository**

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure MongoDB** (optional):
   - Default connects to: `mongodb://localhost:27017/`
   - For custom connection, set environment variable:
     ```bash
     # Windows PowerShell
     $env:MONGODB_URI="mongodb://your-connection-string"
     
     # Windows CMD
     set MONGODB_URI=mongodb://your-connection-string
     
     # Linux/Mac
     export MONGODB_URI=mongodb://your-connection-string
     ```

## Usage

```bash
# Run from project root
python src/main.py
```

### Quick Start Guide

1. **Set Your Savings Goal**: Go to Settings & Goals and set your target (e.g., 20%)

2. **Add Your Income**: Add your monthly salary or other income sources

3. **Add Expenses**: 
   - One-time expenses: groceries, shopping, etc.
   - Recurring expenses: rent, subscriptions, utilities

4. **Track Investments**: Add your investment accounts with their purposes

5. **View Dashboard**: Check your financial overview and see if you're meeting goals

For detailed walkthrough, see [docs/QUICKSTART.md](docs/QUICKSTART.md)

## Data Storage

This application uses **MongoDB** for secure, scalable data storage with the following benefits:

- **Security**: Better access control and authentication options
- **Scalability**: Easily handle large amounts of financial data
- **Flexibility**: Schema-less design allows for easy feature additions
- **Reliability**: Built-in replication and backup capabilities
- **Cloud-ready**: Easily migrate to MongoDB Atlas for cloud storage

### Database Structure
- Database: `personal_finance`
- Collections:
  - `income` - Income entries
  - `expenses` - Expense entries
  - `recurring_expenses` - Recurring expense templates
  - `investments` - Investment portfolio
  - `settings` - Application settings and goals

### Data Security Tips
1. Use MongoDB authentication in production
2. Set up regular backups
3. Use MongoDB Atlas for encrypted cloud storage
4. Never share your connection string publicly
5. Use environment variables for connection strings

## File Structure

- `src/` - All Python source code
  - `main.py` - Main application and menu system
  - `data_manager.py` - MongoDB data layer
  - `income.py` - Income tracking module
  - `expenses.py` - Expense tracking module
  - `investments.py` - Investment portfolio module
  - `dashboard.py` - Financial dashboard
- `docs/` - Documentation files
  - `QUICKSTART.md` - Detailed beginner's guide
  - `TECHNICAL.md` - Technical details
- `config/` - Configuration templates
  - `.env.example` - MongoDB connection template
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore rules

## Expense Categories

- Housing
- Food
- Transportation
- Utilities
- Healthcare
- Entertainment
- Shopping
- Education
- Insurance
- Debt
- Savings
- Other

## Investment Types

- Stocks
- Bonds
- ETF
- Mutual Fund
- Real Estate
- Cryptocurrency
- Savings Account
- CD (Certificate of Deposit)
- Retirement Account
- Other

## Investment Purposes

- Retirement
- Emergency Fund
- House Down Payment
- Education
- Vacation
- Short-term Savings
- Long-term Growth
- Passive Income
- Other

## Tips

- **Process recurring expenses monthly**: Use the "Process Recurring Expenses" option at the start of each month
- **Update investment values regularly**: Keep your portfolio current for accurate tracking
- **Review the dashboard frequently**: Stay on top of your financial health and savings goals
- **Set realistic savings goals**: Start with 10-20% and adjust as needed
- **Build an emergency fund**: Aim for 3-6 months of expenses in emergency savings

## Contributions

Suggestions and improvements are welcome! Financial programs can get quite complex, and a new point of view on calculations, features, or workflows is invaluable to improve the program as a whole. Feel free to open an issue or submit a pull request with your ideas.

## License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0). For more details and information, check the LICENSE file.

## Developers

- **Mano Tilts** - Creator and Lead Developer

## Motivation

Created for personal finance management and tracking.
