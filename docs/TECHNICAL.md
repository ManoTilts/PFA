# Personal Finance Assistant - Technical Overview

## Architecture

### Application Structure
```
PFA/
├── main.py                  # Main application and menu system
├── data_manager.py          # MongoDB data layer
├── income.py                # Income tracking module
├── expenses.py              # Expense tracking module
├── investments.py           # Investment portfolio module
├── dashboard.py             # Financial dashboard and analytics
├── requirements.txt         # Python dependencies
├── README.md                # Main documentation
├── QUICKSTART.md            # Quick start guide
├── .env.example             # Environment configuration example
├── .gitignore               # Git ignore rules
├── setup.bat                # Windows setup script
└── run.bat                  # Windows run script
```

## Technology Stack

### Core Technologies
- **Python 3.8+**: Main programming language
- **MongoDB**: NoSQL database for data persistence
- **PyMongo**: Official MongoDB Python driver

### Why MongoDB?

1. **Security**
   - Built-in authentication and authorization
   - Role-based access control
   - SSL/TLS encryption support
   - Field-level encryption available

2. **Scalability**
   - Handles millions of documents efficiently
   - Horizontal scaling with sharding
   - Can grow with your data needs

3. **Flexibility**
   - Schema-less design for easy feature additions
   - Dynamic field addition without migrations
   - Support for complex nested data

4. **Reliability**
   - Automatic replication
   - Point-in-time backups
   - High availability with replica sets

5. **Cloud-Ready**
   - MongoDB Atlas for managed cloud hosting
   - Free tier available
   - Automatic backups and monitoring

## Database Schema

### Collections

#### income
```javascript
{
  amount: Number,
  source: String,
  date: String (YYYY-MM-DD),
  description: String,
  timestamp: ISODate
}
```

#### expenses
```javascript
{
  amount: Number,
  category: String,
  date: String (YYYY-MM-DD),
  description: String,
  timestamp: ISODate
}
```

#### recurring_expenses
```javascript
{
  amount: Number,
  category: String,
  description: String,
  frequency: String (monthly/weekly/yearly),
  created_date: ISODate,
  last_processed: String (YYYY-MM-DD) or null
}
```

#### investments
```javascript
{
  name: String,
  amount: Number (initial),
  type: String,
  purpose: String,
  date: String (YYYY-MM-DD),
  current_value: Number,
  timestamp: ISODate
}
```

#### settings
```javascript
{
  savings_goal_percentage: Number,
  currency: String
}
```

## Data Manager API

### Income Methods
- `add_income(amount, source, date, description)` - Add income entry
- `get_all_income()` - Retrieve all income entries
- `get_income_by_date_range(start_date, end_date)` - Get filtered income

### Expense Methods
- `add_expense(amount, category, date, description)` - Add expense entry
- `get_all_expenses()` - Retrieve all expense entries
- `get_expenses_by_category(category)` - Filter by category
- `get_expenses_by_date_range(start_date, end_date)` - Get filtered expenses

### Recurring Expense Methods
- `add_recurring_expense(amount, category, description, frequency)` - Add template
- `get_recurring_expenses()` - Get all recurring expenses
- `update_recurring_expense_processed(index, date)` - Mark as processed

### Investment Methods
- `add_investment(name, amount, type, purpose, date)` - Add investment
- `get_all_investments()` - Retrieve all investments
- `get_investments_by_purpose(purpose)` - Filter by purpose
- `update_investment_value(index, new_value)` - Update current value

### Settings Methods
- `set_savings_goal(percentage)` - Set savings goal
- `get_savings_goal()` - Get current goal
- `get_currency()` - Get currency symbol

## Security Best Practices

### 1. Connection String Security
- Never hardcode connection strings
- Use environment variables
- Keep `.env` file out of version control
- Use different credentials for dev/prod

### 2. MongoDB Authentication
```javascript
// Create admin user
use admin
db.createUser({
  user: "pfa_admin",
  pwd: "strong_password_here",
  roles: ["readWrite", "dbAdmin"]
})

// Connection string with auth
mongodb://pfa_admin:strong_password_here@localhost:27017/
```

### 3. Network Security
- Enable firewall rules
- Bind MongoDB to localhost in development
- Use VPN or IP whitelist in production
- Enable SSL/TLS for connections

### 4. Data Protection
- Regular backups (automated with MongoDB Atlas)
- Test restore procedures
- Consider encryption at rest
- Implement audit logging

## Performance Optimization

### Indexes
Create indexes for frequently queried fields:
```javascript
// Create indexes
db.income.createIndex({ date: -1 })
db.expenses.createIndex({ date: -1 })
db.expenses.createIndex({ category: 1 })
db.investments.createIndex({ purpose: 1 })
```

### Query Optimization
- Use projection to limit returned fields
- Implement pagination for large datasets
- Cache frequently accessed data

## Deployment Options

### Local Development
```bash
# Install MongoDB locally
# Default: mongodb://localhost:27017/
python main.py
```

### MongoDB Atlas (Cloud)
```bash
# Set connection string
set MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/

# Run application
python main.py
```

### Docker Deployment
```dockerfile
# Example Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

## Extending the Application

### Adding New Features

1. **New Data Type**
   - Add collection in `data_manager.py`
   - Create methods for CRUD operations
   - Create UI module (e.g., `goals.py`)
   - Add menu in `main.py`

2. **New Analytics**
   - Add methods in respective module
   - Update `dashboard.py` to display
   - Consider caching for performance

3. **Export/Import**
   - JSON export: Use `pymongo` cursors
   - CSV export: Use Python's `csv` module
   - PDF reports: Use `reportlab` library

### Example: Adding a Budget Feature

```python
# In data_manager.py
def add_budget(self, category, monthly_limit):
    entry = {
        "category": category,
        "monthly_limit": monthly_limit,
        "created_date": datetime.now().isoformat()
    }
    self.budgets_collection.insert_one(entry)
    return entry
```

## Testing

### Manual Testing Checklist
- [ ] Add income entry
- [ ] Add one-time expense
- [ ] Add recurring expense
- [ ] Process recurring expenses
- [ ] Add investment
- [ ] Update investment value
- [ ] View dashboard
- [ ] Set savings goal
- [ ] Check all calculations
- [ ] Test date ranges

### Automated Testing (Future Enhancement)
```python
# Example unit test
import unittest
from data_manager import DataManager

class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.dm = DataManager("mongodb://localhost:27017/test_db")
    
    def test_add_income(self):
        entry = self.dm.add_income(1000, "Salary", "2025-01-01", "Test")
        self.assertEqual(entry['amount'], 1000)
```

## Troubleshooting

### Common Issues

**Problem**: Cannot connect to MongoDB
**Solution**: 
- Check if MongoDB is running: `mongod --version`
- Verify connection string
- Check firewall settings

**Problem**: pymongo module not found
**Solution**: 
```bash
pip install pymongo
```

**Problem**: Data not persisting
**Solution**:
- Check MongoDB is running
- Verify write permissions
- Check disk space

**Problem**: Slow queries
**Solution**:
- Create appropriate indexes
- Reduce data volume
- Use aggregation pipelines

## Migration from JSON

If you have data in the old JSON format:

```python
# migration_script.py
import json
from data_manager import DataManager

# Load old JSON data
with open('finance_data.json', 'r') as f:
    old_data = json.load(f)

# Initialize MongoDB
dm = DataManager()

# Migrate income
for entry in old_data['income']:
    dm.add_income(**entry)

# Migrate expenses
for entry in old_data['expenses']:
    dm.add_expense(**entry)

# And so on...
```

## Future Enhancements

### Planned Features
1. Multi-currency support
2. Budget tracking and alerts
3. Bill payment reminders
4. Financial goal tracking
5. Data export (CSV, PDF)
6. Visualizations and charts
7. Mobile app integration
8. Bank account integration (API)
9. Tax calculation assistance
10. Multi-user support with authentication

### Technical Improvements
1. Async MongoDB operations
2. Caching layer (Redis)
3. RESTful API backend
4. Web interface (Flask/FastAPI)
5. GraphQL API
6. Real-time updates (WebSockets)
7. Unit and integration tests
8. CI/CD pipeline
9. Docker containerization
10. Kubernetes deployment

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## License

See LICENSE file for details.

## Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check the documentation
- Review the code comments
