"""
Expense Manager - Handles expense tracking including recurring expenses
"""

from datetime import datetime


class ExpenseManager:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.common_categories = [
            "Housing", "Food", "Transportation", "Utilities", 
            "Healthcare", "Entertainment", "Shopping", "Education",
            "Insurance", "Debt", "Savings", "Other"
        ]
    
    def add_expense(self):
        """Add a new expense entry"""
        print("\n" + "="*60)
        print("ADD NEW EXPENSE".center(60))
        print("="*60)
        
        try:
            amount = float(input("Enter amount: ").strip())
            if amount <= 0:
                print("Amount must be positive.")
                return
            
            print("\nCommon categories:")
            for i, cat in enumerate(self.common_categories, 1):
                print(f"  [{i}] {cat}", end="   " if i % 3 != 0 else "\n")
            print()
            
            category = input("\nEnter category (or select number): ").strip()
            
            # Check if user entered a number
            try:
                cat_num = int(category)
                if 1 <= cat_num <= len(self.common_categories):
                    category = self.common_categories[cat_num - 1]
            except ValueError:
                pass
            
            if not category:
                print("Category cannot be empty.")
                return
            
            date_input = input("Enter date (YYYY-MM-DD) or press Enter for today: ").strip()
            if date_input:
                try:
                    datetime.strptime(date_input, "%Y-%m-%d")
                    date = date_input
                except ValueError:
                    print("Invalid date format. Using today's date.")
                    date = datetime.now().strftime("%Y-%m-%d")
            else:
                date = datetime.now().strftime("%Y-%m-%d")
            
            description = input("Enter description (optional): ").strip()
            
            entry = self.data_manager.add_expense(amount, category, date, description)
            currency = self.data_manager.get_currency()
            print(f"\nExpense added successfully!")
            print(f"   Amount: {currency}{amount:,.2f}")
            print(f"   Category: {category}")
            print(f"   Date: {date}")
            
        except ValueError:
            print("Invalid amount. Please enter a number.")
    
    def add_recurring_expense(self):
        """Add a recurring expense"""
        print("\n" + "="*60)
        print("ADD RECURRING EXPENSE".center(60))
        print("="*60)
        
        try:
            amount = float(input("Enter amount: ").strip())
            if amount <= 0:
                print("Amount must be positive.")
                return
            
            print("\nCommon categories:")
            for i, cat in enumerate(self.common_categories, 1):
                print(f"  [{i}] {cat}", end="   " if i % 3 != 0 else "\n")
            print()
            
            category = input("\nEnter category (or select number): ").strip()
            
            # Check if user entered a number
            try:
                cat_num = int(category)
                if 1 <= cat_num <= len(self.common_categories):
                    category = self.common_categories[cat_num - 1]
            except ValueError:
                pass
            
            if not category:
                print("Category cannot be empty.")
                return
            
            description = input("Enter description: ").strip()
            if not description:
                print("Description is required for recurring expenses.")
                return
            
            print("\nFrequency options:")
            print("  [1] Monthly")
            print("  [2] Weekly")
            print("  [3] Yearly")
            
            freq_choice = input("\nSelect frequency (or type custom): ").strip()
            freq_map = {"1": "Monthly", "2": "Weekly", "3": "Yearly"}
            frequency = freq_map.get(freq_choice, freq_choice)
            
            entry = self.data_manager.add_recurring_expense(amount, category, description, frequency)
            currency = self.data_manager.get_currency()
            print(f"\nRecurring expense added successfully!")
            print(f"   Amount: {currency}{amount:,.2f}")
            print(f"   Category: {category}")
            print(f"   Description: {description}")
            print(f"   Frequency: {frequency}")
            
        except ValueError:
            print("Invalid amount. Please enter a number.")
    
    def view_all_expenses(self):
        """Display all expense entries"""
        expense_entries = self.data_manager.get_all_expenses()
        
        if not expense_entries:
            print("\nNo expense entries found.")
            return
        
        currency = self.data_manager.get_currency()
        print("\n" + "="*60)
        print("ALL EXPENSE ENTRIES".center(60))
        print("="*60)
        
        # Sort by date (newest first)
        sorted_expenses = sorted(expense_entries, key=lambda x: x['date'], reverse=True)
        
        total = 0
        total_investments = 0
        for i, entry in enumerate(sorted_expenses, 1):
            print(f"\n[{i}] {currency}{entry['amount']:,.2f}")
            print(f"    Category: {entry['category']}")
            print(f"    Date: {entry['date']}")
            if entry.get('description'):
                print(f"    Description: {entry['description']}")
            
            if entry['category'].lower() == 'investment':
                total_investments += entry['amount']
            else:
                total += entry['amount']
        
        print("\n" + "-"*60)
        print(f"TOTAL EXPENSES: {currency}{total:,.2f}")
        if total_investments > 0:
            print(f"TOTAL INVESTMENTS: {currency}{total_investments:,.2f}")
            print(f"COMBINED TOTAL: {currency}{total + total_investments:,.2f}")
        print("-"*60)
    
    def view_by_category(self):
        """Display expenses grouped by category"""
        expense_entries = self.data_manager.get_all_expenses()
        
        if not expense_entries:
            print("\nNo expense entries found.")
            return
        
        currency = self.data_manager.get_currency()
        
        # Group by category
        by_category = {}
        for entry in expense_entries:
            category = entry['category']
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(entry)
        
        # Separate regular expenses from investments
        total_expenses = sum(
            entry['amount'] for entry in expense_entries
            if entry['category'].lower() != 'investment'
        )
        total_investments = sum(
            entry['amount'] for entry in expense_entries
            if entry['category'].lower() == 'investment'
        )
        
        print("\n" + "="*60)
        print("EXPENSES BY CATEGORY".center(60))
        print("="*60)
        
        for category in sorted(by_category.keys()):
            entries = by_category[category]
            category_total = sum(entry['amount'] for entry in entries)
            
            # Calculate percentage based on appropriate total
            if category.lower() == 'investment':
                base_total = total_investments + total_expenses
                label = "(Savings/Investment)"
            else:
                base_total = total_expenses
                label = ""
            
            percentage = (category_total / base_total) * 100 if base_total > 0 else 0
            
            print(f"\n{category} {label}")
            print(f"   Total: {currency}{category_total:,.2f} ({percentage:.1f}%)")
            print(f"   Entries: {len(entries)}")
        
        print("\n" + "-"*60)
        print(f"CONSUMPTION EXPENSES: {currency}{total_expenses:,.2f}")
        if total_investments > 0:
            print(f"INVESTMENTS (SAVINGS): {currency}{total_investments:,.2f}")
        print(f"TOTAL OUTFLOWS: {currency}{total_expenses + total_investments:,.2f}")
        print("-"*60)
    
    def view_recurring_expenses(self):
        """Display all recurring expenses"""
        recurring = self.data_manager.get_recurring_expenses()
        
        if not recurring:
            print("\nNo recurring expenses found.")
            return
        
        currency = self.data_manager.get_currency()
        print("\n" + "="*60)
        print("RECURRING EXPENSES".center(60))
        print("="*60)
        
        total_monthly = 0
        for i, entry in enumerate(recurring, 1):
            print(f"\n[{i}] {currency}{entry['amount']:,.2f} - {entry['frequency']}")
            print(f"    Category: {entry['category']}")
            print(f"    Description: {entry['description']}")
            if entry.get('last_processed'):
                print(f"    Last processed: {entry['last_processed']}")
            
            # Calculate monthly equivalent
            if entry['frequency'].lower() == 'monthly':
                monthly_amount = entry['amount']
            elif entry['frequency'].lower() == 'weekly':
                monthly_amount = entry['amount'] * 4.33
            elif entry['frequency'].lower() == 'yearly':
                monthly_amount = entry['amount'] / 12
            else:
                monthly_amount = entry['amount']
            
            total_monthly += monthly_amount
        
        print("\n" + "-"*60)
        print(f"ESTIMATED MONTHLY TOTAL: {currency}{total_monthly:,.2f}")
        print("-"*60)
    
    def process_recurring_expenses(self):
        """Process recurring expenses for the current month"""
        recurring = self.data_manager.get_recurring_expenses()
        
        if not recurring:
            print("\nNo recurring expenses found.")
            return
        
        current_month = datetime.now().strftime("%Y-%m")
        today = datetime.now().strftime("%Y-%m-%d")
        processed_count = 0
        
        print("\n" + "="*60)
        print("PROCESSING RECURRING EXPENSES".center(60))
        print("="*60)
        
        for i, entry in enumerate(recurring):
            last_processed = entry.get('last_processed', '')
            
            # Check if already processed this month
            if last_processed and last_processed.startswith(current_month):
                print(f"\nSkipping: {entry['description']} (already processed this month)")
                continue
            
            # Ask user to confirm
            currency = self.data_manager.get_currency()
            print(f"\n{entry['description']}")
            print(f"   Amount: {currency}{entry['amount']:,.2f}")
            print(f"   Category: {entry['category']}")
            
            confirm = input("   Add this expense? (y/n): ").strip().lower()
            
            if confirm == 'y':
                self.data_manager.add_expense(
                    entry['amount'],
                    entry['category'],
                    today,
                    f"{entry['description']} (Recurring)"
                )
                self.data_manager.update_recurring_expense_processed(i, today)
                processed_count += 1
                print("   Added!")
        
        print("\n" + "-"*60)
        print(f"Processed {processed_count} recurring expense(s)")
        print("-"*60)
    
    def investment_deposit(self):
        """Deposit money into an investment (creates expense)"""
        print("\n" + "="*60)
        print("INVESTMENT DEPOSIT".center(60))
        print("="*60)
        
        try:
            amount = float(input("Enter deposit amount: ").strip())
            if amount <= 0:
                print("Amount must be positive.")
                return
            
            # List existing investments
            investments = self.data_manager.get_all_investments()
            
            print("\n[0] Create New Investment")
            if investments:
                currency = self.data_manager.get_currency()
                for i, inv in enumerate(investments, 1):
                    current_value = inv.get('current_value', inv['amount'])
                    print(f"[{i}] {inv['name']} ({inv['type']}) - {currency}{current_value:,.2f}")
            
            choice = input("\nSelect investment (or 0 for new): ").strip()
            
            try:
                choice_num = int(choice)
            except ValueError:
                print("Invalid selection.")
                return
            
            investment_name = ""
            
            if choice_num == 0:
                # Create new investment
                investment_name = input("Enter investment name: ").strip()
                if not investment_name:
                    print("Name cannot be empty.")
                    return
                
                inv_type = input("Enter investment type (e.g., Savings, Stocks, ETF): ").strip()
                if not inv_type:
                    inv_type = "Other"
                
                purpose = input("Enter purpose (e.g., Emergency Fund, Passive Income): ").strip()
                if not purpose:
                    purpose = "General"
                
                date = datetime.now().strftime("%Y-%m-%d")
                self.data_manager.add_investment(investment_name, amount, inv_type, purpose, date)
                print(f"\nNew investment '{investment_name}' created!")
            
            elif 1 <= choice_num <= len(investments):
                # Existing investment
                inv = investments[choice_num - 1]
                investment_name = inv['name']
                current_value = inv.get('current_value', inv['amount'])
                new_value = current_value + amount
                
                self.data_manager.update_investment_value(choice_num - 1, new_value)
                print(f"\nInvestment '{investment_name}' updated!")
                currency = self.data_manager.get_currency()
                print(f"   Previous value: {currency}{current_value:,.2f}")
                print(f"   Deposit: +{currency}{amount:,.2f}")
                print(f"   New value: {currency}{new_value:,.2f}")
            else:
                print("Invalid selection.")
                return
            
            # Create expense entry
            date = datetime.now().strftime("%Y-%m-%d")
            description = f"Investment deposit to {investment_name}"
            self.data_manager.add_expense(amount, "Investment", date, description)
            
            currency = self.data_manager.get_currency()
            print(f"\nExpense recorded: {currency}{amount:,.2f} (Investment)")
            print("Your available balance has been reduced accordingly.")
            
        except ValueError:
            print("Invalid amount. Please enter a number.")
    
    def simulate_expense(self):
        """Simulate adding an expense to see the impact on finances"""
        print("\n" + "="*60)
        print("SIMULATE EXPENSE".center(60))
        print("="*60)
        
        try:
            amount = float(input("Enter amount to simulate: ").strip())
            if amount <= 0:
                print("Amount must be positive.")
                return
            
            print("\nCommon categories:")
            for i, cat in enumerate(self.common_categories, 1):
                print(f"  [{i}] {cat}", end="   " if i % 3 != 0 else "\n")
            print()
            
            category = input("\nEnter category (or select number): ").strip()
            
            # Check if user entered a number
            try:
                cat_num = int(category)
                if 1 <= cat_num <= len(self.common_categories):
                    category = self.common_categories[cat_num - 1]
            except ValueError:
                pass
            
            if not category:
                print("Category cannot be empty.")
                return
            
            description = input("Enter description (optional): ").strip()
            
            # Calculate current financial status
            currency = self.data_manager.get_currency()
            all_income = self.data_manager.get_all_income()
            all_expenses = self.data_manager.get_all_expenses()
            
            total_income = sum(entry['amount'] for entry in all_income)
            # Separate regular expenses from investments
            total_expenses = sum(
                entry['amount'] for entry in all_expenses
                if entry['category'].lower() != 'investment'
            )
            total_investments = sum(
                entry['amount'] for entry in all_expenses
                if entry['category'].lower() == 'investment'
            )
            current_balance = total_income - total_expenses - total_investments
            
            # Calculate after simulation (only affects balance if it's a regular expense)
            if category.lower() == 'investment':
                balance_after = current_balance - amount  # Investment reduces cash
                new_total_investments = total_investments + amount
                new_total_expenses = total_expenses
            else:
                balance_after = current_balance - amount
                new_total_investments = total_investments
                new_total_expenses = total_expenses + amount
            
            # Display simulation results
            print("\n" + "="*60)
            print("SIMULATION RESULTS".center(60))
            print("="*60)
            print(f"\nExpense Details:")
            print(f"   Amount: {currency}{amount:,.2f}")
            print(f"   Category: {category}")
            if description:
                print(f"   Description: {description}")
            
            print(f"\nCurrent Financial Status:")
            print(f"   Total Income: {currency}{total_income:,.2f}")
            print(f"   Total Expenses: {currency}{total_expenses:,.2f}")
            if total_investments > 0:
                print(f"   Total Invested: {currency}{total_investments:,.2f}")
            print(f"   Current Balance: {currency}{current_balance:,.2f}")
            
            print(f"\nAfter This {'Investment' if category.lower() == 'investment' else 'Expense'}:")
            if category.lower() == 'investment':
                print(f"   Total Expenses: {currency}{total_expenses:,.2f} (unchanged)")
                print(f"   New Total Invested: {currency}{new_total_investments:,.2f}")
            else:
                print(f"   New Total Expenses: {currency}{new_total_expenses:,.2f}")
                if total_investments > 0:
                    print(f"   Total Invested: {currency}{total_investments:,.2f} (unchanged)")
            print(f"   New Balance: {currency}{balance_after:,.2f}")
            
            # Calculate percentage impact
            if total_income > 0:
                expense_percentage = (amount / total_income) * 100
                print(f"   This expense is {expense_percentage:.2f}% of total income")
            
            # Show warning if balance would go negative
            if balance_after < 0:
                print(f"\n⚠️  WARNING: This expense would result in a negative balance!")
                print(f"   Shortfall: {currency}{abs(balance_after):,.2f}")
            
            # Category comparison
            category_expenses = self.data_manager.get_expenses_by_category(category)
            category_total = sum(entry['amount'] for entry in category_expenses)
            new_category_total = category_total + amount
            
            print(f"\nCategory Impact ({category}):")
            print(f"   Current Total: {currency}{category_total:,.2f}")
            print(f"   After This Expense: {currency}{new_category_total:,.2f}")
            
            # Calculate percentage of appropriate total
            if category.lower() == 'investment':
                total_for_pct = total_investments
                new_total_for_pct = new_total_investments
                label = "Total Investments"
            else:
                total_for_pct = total_expenses
                new_total_for_pct = new_total_expenses
                label = "Total Expenses"
            
            if total_for_pct > 0 or new_total_for_pct > 0:
                current_category_pct = (category_total / total_for_pct * 100) if total_for_pct > 0 else 0
                new_category_pct = (new_category_total / new_total_for_pct * 100) if new_total_for_pct > 0 else 0
                print(f"   Category % of {label}: {current_category_pct:.1f}% → {new_category_pct:.1f}%")
            
            print("\n" + "-"*60)
            print("This is a SIMULATION only - no data has been saved.")
            print("-"*60)
            
            # Ask if user wants to actually add the expense
            confirm = input("\nDo you want to add this expense for real? (y/n): ").strip().lower()
            if confirm == 'y':
                date = datetime.now().strftime("%Y-%m-%d")
                self.data_manager.add_expense(amount, category, date, description)
                print(f"\nExpense added successfully!")
            else:
                print("\nExpense not added. Simulation discarded.")
            
        except ValueError:
            print("Invalid amount. Please enter a number.")
