"""
Data Manager - Handles all data persistence using MongoDB
"""

from pymongo import MongoClient
from datetime import datetime
import os


class DataManager:
    def __init__(self, connection_string=None):
        # Use environment variable or default to local MongoDB
        if connection_string is None:
            connection_string = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
        
        self.client = MongoClient(connection_string)
        self.db = self.client['personal_finance']
        self.income_collection = self.db['income']
        self.expenses_collection = self.db['expenses']
        self.recurring_expenses_collection = self.db['recurring_expenses']
        self.investments_collection = self.db['investments']
        self.settings_collection = self.db['settings']
        self.debts_collection = self.db['debts']
        self.goals_collection = self.db['goals']
        
        # Initialize settings if not exists
        self._initialize_settings()
    
        # Initialize settings if not exists
        self._initialize_settings()
    
    def _initialize_settings(self):
        """Initialize default settings if not exists"""
        if self.settings_collection.count_documents({}) == 0:
            default_settings = {
                "savings_goal_percentage": 20.0,
                "currency": "$"
            }
            self.settings_collection.insert_one(default_settings)
    
    def close(self):
        """Close MongoDB connection"""
        self.client.close()
    
    # Income methods
    def add_income(self, amount, source, date, description=""):
        """Add an income entry"""
        entry = {
            "amount": amount,
            "source": source,
            "date": date,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        self.income_collection.insert_one(entry)
        return entry
    
    def get_all_income(self):
        """Get all income entries"""
        return list(self.income_collection.find({}, {'_id': 0}))
    
    def get_income_by_date_range(self, start_date, end_date):
        """Get income within a date range"""
        return list(self.income_collection.find({
            "date": {"$gte": start_date, "$lte": end_date}
        }, {'_id': 0}))
    
    # Expense methods
    def add_expense(self, amount, category, date, description=""):
        """Add an expense entry"""
        entry = {
            "amount": amount,
            "category": category,
            "date": date,
            "description": description,
            "timestamp": datetime.now().isoformat()
        }
        self.expenses_collection.insert_one(entry)
        return entry
    
    def get_all_expenses(self):
        """Get all expense entries"""
        return list(self.expenses_collection.find({}, {'_id': 0}))
    
    def get_expenses_by_category(self, category):
        """Get expenses by category"""
        return list(self.expenses_collection.find({
            "category": {"$regex": f"^{category}$", "$options": "i"}
        }, {'_id': 0}))
    
    def get_expenses_by_date_range(self, start_date, end_date):
        """Get expenses within a date range"""
        return list(self.expenses_collection.find({
            "date": {"$gte": start_date, "$lte": end_date}
        }, {'_id': 0}))
    
    # Recurring expense methods
    def add_recurring_expense(self, amount, category, description, frequency):
        """Add a recurring expense"""
        entry = {
            "amount": amount,
            "category": category,
            "description": description,
            "frequency": frequency,
            "created_date": datetime.now().isoformat(),
            "last_processed": None
        }
        self.recurring_expenses_collection.insert_one(entry)
        return entry
    
    def get_recurring_expenses(self):
        """Get all recurring expenses"""
        return list(self.recurring_expenses_collection.find({}, {'_id': 0}))
    
    def update_recurring_expense_processed(self, index, date):
        """Update the last processed date for a recurring expense"""
        recurring = list(self.recurring_expenses_collection.find({}))
        if 0 <= index < len(recurring):
            self.recurring_expenses_collection.update_one(
                {'_id': recurring[index]['_id']},
                {'$set': {'last_processed': date}}
            )
    
    # Investment methods
    def add_investment(self, name, amount, type_name, purpose, date):
        """Add an investment entry"""
        entry = {
            "name": name,
            "amount": amount,
            "type": type_name,
            "purpose": purpose,
            "date": date,
            "current_value": amount,
            "timestamp": datetime.now().isoformat()
        }
        self.investments_collection.insert_one(entry)
        return entry
    
    def get_all_investments(self):
        """Get all investment entries"""
        return list(self.investments_collection.find({}, {'_id': 0}))
    
    def get_investments_by_purpose(self, purpose):
        """Get investments by purpose"""
        return list(self.investments_collection.find({
            "purpose": {"$regex": f"^{purpose}$", "$options": "i"}
        }, {'_id': 0}))
    
    def update_investment_value(self, index, new_value):
        """Update the current value of an investment"""
        investments = list(self.investments_collection.find({}))
        if 0 <= index < len(investments):
            self.investments_collection.update_one(
                {'_id': investments[index]['_id']},
                {'$set': {'current_value': new_value}}
            )
            return True
        return False
    
    # Settings methods
    def set_savings_goal(self, percentage):
        """Set the savings goal percentage"""
        self.settings_collection.update_one(
            {},
            {'$set': {'savings_goal_percentage': percentage}},
            upsert=True
        )
    
    def get_savings_goal(self):
        """Get the savings goal percentage"""
        settings = self.settings_collection.find_one({})
        return settings.get('savings_goal_percentage', 20.0) if settings else 20.0
    
    def get_currency(self):
        """Get the currency symbol"""
        settings = self.settings_collection.find_one({})
        return settings.get('currency', '$') if settings else '$'
    
    # Debt methods
    def add_debt(self, amount, description, date, month_limit=None, target_date=None):
        """Add a debt/overexpense entry"""
        entry = {
            "amount": amount,
            "description": description,
            "date": date,
            "paid": 0,
            "payments": [],
            "month_limit": month_limit,
            "target_date": target_date,
            "timestamp": datetime.now().isoformat()
        }
        self.debts_collection.insert_one(entry)
        return entry
    
    def get_all_debts(self):
        """Get all debt entries"""
        return list(self.debts_collection.find({}))
    
    def get_active_debts(self):
        """Get debts that are not fully paid"""
        all_debts = list(self.debts_collection.find({}))
        return [d for d in all_debts if d['amount'] > d.get('paid', 0)]
    
    def add_debt_payment(self, debt_id, amount, date):
        """Record a payment towards a debt"""
        debt = self.debts_collection.find_one({'_id': debt_id})
        if debt:
            new_paid = debt.get('paid', 0) + amount
            payment = {"amount": amount, "date": date}
            
            self.debts_collection.update_one(
                {'_id': debt_id},
                {
                    '$set': {'paid': new_paid},
                    '$push': {'payments': payment}
                }
            )
            return True
        return False
    
    def set_debt_repayment_goal(self, amount):
        """Set monthly debt repayment goal"""
        self.settings_collection.update_one(
            {},
            {'$set': {'debt_repayment_goal': amount}},
            upsert=True
        )
    
    def get_debt_repayment_goal(self):
        """Get monthly debt repayment goal"""
        settings = self.settings_collection.find_one({})
        return settings.get('debt_repayment_goal', 0) if settings else 0
    
    # Goals methods
    def add_goal(self, name, target_amount, monthly_target, deadline, description, date):
        """Add a savings goal"""
        entry = {
            "name": name,
            "target_amount": target_amount,
            "monthly_target": monthly_target,
            "deadline": deadline,
            "description": description,
            "date": date,
            "saved": 0,
            "contributions": [],
            "timestamp": datetime.now().isoformat()
        }
        self.goals_collection.insert_one(entry)
        return entry
    
    def get_all_goals(self):
        """Get all savings goals"""
        return list(self.goals_collection.find({}))
    
    def get_active_goals(self):
        """Get goals that are not fully funded"""
        all_goals = list(self.goals_collection.find({}))
        return [g for g in all_goals if g['target_amount'] > g.get('saved', 0)]
    
    def add_goal_contribution(self, goal_id, amount, date):
        """Record a contribution towards a goal"""
        goal = self.goals_collection.find_one({'_id': goal_id})
        if goal:
            new_saved = goal.get('saved', 0) + amount
            contribution = {"amount": amount, "date": date}
            
            self.goals_collection.update_one(
                {'_id': goal_id},
                {
                    '$set': {'saved': new_saved},
                    '$push': {'contributions': contribution}
                }
            )
            return True
        return False
    
    def update_goal_monthly_target(self, goal_id, new_target):
        """Update the monthly target for a goal"""
        self.goals_collection.update_one(
            {'_id': goal_id},
            {'$set': {'monthly_target': new_target}}
        )
        return True
