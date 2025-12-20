"""
Income Manager - Handles income tracking and reporting
"""

from datetime import datetime


class IncomeManager:
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def add_income(self):
        """Add a new income entry"""
        print("\n" + "="*60)
        print("ADD NEW INCOME".center(60))
        print("="*60)
        
        try:
            amount = float(input("Enter amount: ").strip())
            if amount <= 0:
                print("Amount must be positive.")
                return
            
            print("\nCommon sources: Salary, Freelance, Bonus, Investment Return, Gift, Other")
            source = input("Enter income source: ").strip()
            if not source:
                print("Source cannot be empty.")
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
            
            entry = self.data_manager.add_income(amount, source, date, description)
            currency = self.data_manager.get_currency()
            print(f"\nIncome added successfully!")
            print(f"   Amount: {currency}{amount:,.2f}")
            print(f"   Source: {source}")
            print(f"   Date: {date}")
            
        except ValueError:
            print("Invalid amount. Please enter a number.")
    
    def view_all_income(self):
        """Display all income entries"""
        income_entries = self.data_manager.get_all_income()
        
        if not income_entries:
            print("\nNo income entries found.")
            return
        
        currency = self.data_manager.get_currency()
        print("\n" + "="*60)
        print("ALL INCOME ENTRIES".center(60))
        print("="*60)
        
        total = 0
        for i, entry in enumerate(income_entries, 1):
            print(f"\n[{i}] {currency}{entry['amount']:,.2f}")
            print(f"    Source: {entry['source']}")
            print(f"    Date: {entry['date']}")
            if entry.get('description'):
                print(f"    Description: {entry['description']}")
            total += entry['amount']
        
        print("\n" + "-"*60)
        print(f"TOTAL INCOME: {currency}{total:,.2f}")
        print("-"*60)
    
    def view_summary(self):
        """Display income summary with statistics"""
        income_entries = self.data_manager.get_all_income()
        
        if not income_entries:
            print("\nNo income entries found.")
            return
        
        currency = self.data_manager.get_currency()
        
        # Calculate statistics
        total_income = sum(entry['amount'] for entry in income_entries)
        avg_income = total_income / len(income_entries)
        
        # Group by source
        by_source = {}
        for entry in income_entries:
            source = entry['source']
            if source not in by_source:
                by_source[source] = 0
            by_source[source] += entry['amount']
        
        # Get current month income
        current_month = datetime.now().strftime("%Y-%m")
        month_income = sum(
            entry['amount'] for entry in income_entries
            if entry['date'].startswith(current_month)
        )
        
        print("\n" + "="*60)
        print("INCOME SUMMARY".center(60))
        print("="*60)
        
        print(f"\nTotal Income: {currency}{total_income:,.2f}")
        print(f"Average Income per Entry: {currency}{avg_income:,.2f}")
        print(f"Total Entries: {len(income_entries)}")
        print(f"Current Month Income: {currency}{month_income:,.2f}")
        
        print("\n" + "-"*60)
        print("INCOME BY SOURCE".center(60))
        print("-"*60)
        
        for source, amount in sorted(by_source.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total_income) * 100
            print(f"{source:.<30} {currency}{amount:>12,.2f} ({percentage:>5.1f}%)")
        
        print("="*60)
    
    def investment_withdrawal(self):
        """Withdraw money from an investment (creates income)"""
        print("\n" + "="*60)
        print("INVESTMENT WITHDRAWAL".center(60))
        print("="*60)
        
        investments = self.data_manager.get_all_investments()
        
        if not investments:
            print("\nNo investments found. Create an investment first.")
            return
        
        # Display investments
        currency = self.data_manager.get_currency()
        print("\nSelect investment to withdraw from:")
        for i, inv in enumerate(investments, 1):
            current_value = inv.get('current_value', inv['amount'])
            print(f"[{i}] {inv['name']} ({inv['type']}) - {currency}{current_value:,.2f}")
        
        try:
            choice = int(input("\nSelect investment number: ").strip())
            if not (1 <= choice <= len(investments)):
                print("Invalid selection.")
                return
            
            inv = investments[choice - 1]
            investment_name = inv['name']
            current_value = inv.get('current_value', inv['amount'])
            
            print(f"\nWithdrawing from: {investment_name}")
            print(f"Current value: {currency}{current_value:,.2f}")
            
            amount = float(input("Enter withdrawal amount: ").strip())
            if amount <= 0:
                print("Amount must be positive.")
                return
            
            if amount > current_value:
                print(f"Warning: Withdrawal amount exceeds current investment value!")
                confirm = input(f"Continue anyway? (y/n): ").strip().lower()
                if confirm != 'y':
                    return
            
            # Update investment value
            new_value = current_value - amount
            self.data_manager.update_investment_value(choice - 1, new_value)
            
            # Create income entry
            date = datetime.now().strftime("%Y-%m-%d")
            description = f"Withdrawal from {investment_name}"
            self.data_manager.add_income(amount, "Investment Withdrawal", date, description)
            
            print(f"\nWithdrawal successful!")
            print(f"   Withdrawn: {currency}{amount:,.2f}")
            print(f"   New investment value: {currency}{new_value:,.2f}")
            print(f"\nIncome recorded: {currency}{amount:,.2f} (Investment Withdrawal)")
            print("Your available balance has been increased accordingly.")
            
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
