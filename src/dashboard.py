"""
Dashboard - Financial overview and goal tracking
"""

from datetime import datetime


class Dashboard:
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def show_dashboard(self):
        """Display comprehensive financial dashboard"""
        print("\n" + "="*60)
        print("FINANCIAL DASHBOARD".center(60))
        print("="*60)
        
        currency = self.data_manager.get_currency()
        current_month = datetime.now().strftime("%Y-%m")
        current_month_name = datetime.now().strftime("%B %Y")
        
        # Get all data
        all_income = self.data_manager.get_all_income()
        all_expenses = self.data_manager.get_all_expenses()
        all_investments = self.data_manager.get_all_investments()
        savings_goal = self.data_manager.get_savings_goal()
        
        # Current month data
        month_income = sum(
            entry['amount'] for entry in all_income
            if entry['date'].startswith(current_month)
        )
        # Separate regular expenses from investment deposits
        month_expenses = sum(
            entry['amount'] for entry in all_expenses
            if entry['date'].startswith(current_month) and entry['category'].lower() != 'investment'
        )
        month_investments = sum(
            entry['amount'] for entry in all_expenses
            if entry['date'].startswith(current_month) and entry['category'].lower() == 'investment'
        )
        
        # Total data
        total_income = sum(entry['amount'] for entry in all_income)
        total_expenses = sum(
            entry['amount'] for entry in all_expenses
            if entry['category'].lower() != 'investment'
        )
        total_investments = sum(
            entry['amount'] for entry in all_expenses
            if entry['category'].lower() == 'investment'
        )
        total_invested = sum(inv['amount'] for inv in all_investments)
        total_investment_value = sum(
            inv.get('current_value', inv['amount']) for inv in all_investments
        )
        
        # Calculations - Investments count as savings!
        month_net_cash = month_income - month_expenses - month_investments  # Cash left after expenses AND investments
        month_total_saved = month_net_cash + month_investments  # Total saved = cash kept + money invested
        month_savings_rate = (month_total_saved / month_income * 100) if month_income > 0 else 0
        
        total_net_cash = total_income - total_expenses - total_investments
        total_saved = total_net_cash + total_investments
        
        # Display Current Month Summary
        print(f"\n{current_month_name}")
        print("-" * 60)
        print(f"Income:              {currency}{month_income:>15,.2f}")
        print(f"Expenses:            {currency}{month_expenses:>15,.2f}")
        print("-" * 60)
        print(f"Total Saved:         {currency}{month_total_saved:>15,.2f}")
        print(f"  • Invested:        {currency}{month_investments:>15,.2f}")
        print(f"  • Cash Remaining:  {currency}{month_net_cash:>15,.2f}")
        print(f"Savings Rate:        {month_savings_rate:>15.1f}%")
        
        # Savings Goal Check
        print("\n" + "-" * 60)
        print("SAVINGS GOAL CHECK".center(60))
        print("-" * 60)
        print(f"Target Savings Rate: {savings_goal}%")
        print(f"Current Savings Rate: {month_savings_rate:.1f}%")
        
        if month_income > 0:
            target_savings = month_income * (savings_goal / 100)
            actual_savings = month_total_saved  # Includes investments!
            difference = actual_savings - target_savings
            
            print(f"Target Savings: {currency}{target_savings:,.2f}")
            print(f"Actual Savings: {currency}{actual_savings:,.2f}")
            
            if month_savings_rate >= savings_goal:
                print(f"✓ GOAL MET! You're saving {currency}{difference:,.2f} more than your goal!")
            else:
                print(f"✗ Below target by {currency}{abs(difference):,.2f}")
                percentage_to_goal = (month_savings_rate / savings_goal * 100) if savings_goal > 0 else 0
                print(f"   You're at {percentage_to_goal:.1f}% of your savings goal")
        else:
            print("No income recorded this month")
        
        # All-Time Summary
        print("\n" + "-" * 60)
        print("ALL-TIME SUMMARY".center(60))
        print("-" * 60)
        print(f"Total Income:    {currency}{total_income:>15,.2f}")
        print(f"Total Expenses:  {currency}{total_expenses:>15,.2f}")
        print(f"Total Invested:  {currency}{total_investments:>15,.2f}")
        print(f"Total Saved:     {currency}{total_saved:>15,.2f}")
        print(f"Cash Remaining:  {currency}{total_net_cash:>15,.2f}")
        
        # Investment Summary
        if all_investments:
            investment_gain = total_investment_value - total_invested
            investment_gain_pct = (investment_gain / total_invested * 100) if total_invested > 0 else 0
            
            print("\n" + "-" * 60)
            print("INVESTMENT SUMMARY".center(60))
            print("-" * 60)
            print(f"Invested:        {currency}{total_invested:>15,.2f}")
            print(f"Current Value:   {currency}{total_investment_value:>15,.2f}")
            if investment_gain >= 0:
                print(f"Gain:            {currency}{investment_gain:>15,.2f} (+{investment_gain_pct:.1f}%)")
            else:
                print(f"Loss:            {currency}{investment_gain:>15,.2f} ({investment_gain_pct:.1f}%)")
        
        # Expense Breakdown (Current Month)
        month_expenses_list = [
            entry for entry in all_expenses
            if entry['date'].startswith(current_month)
        ]
        
        if month_expenses_list:
            print("\n" + "-" * 60)
            print(f"EXPENSE BREAKDOWN - {current_month_name}".center(60))
            print("-" * 60)
            
            # Group by category
            by_category = {}
            for entry in month_expenses_list:
                category = entry['category']
                if category not in by_category:
                    by_category[category] = 0
                by_category[category] += entry['amount']
            
            # Sort by amount and display top categories
            sorted_categories = sorted(by_category.items(), key=lambda x: x[1], reverse=True)
            for category, amount in sorted_categories[:5]:  # Top 5
                percentage = (amount / month_expenses * 100) if month_expenses > 0 else 0
                print(f"{category:.<30} {currency}{amount:>10,.2f} ({percentage:>5.1f}%)")
            
            if len(sorted_categories) > 5:
                other_total = sum(amount for _, amount in sorted_categories[5:])
                other_pct = (other_total / month_expenses * 100) if month_expenses > 0 else 0
                print(f"{'Other':.<30} {currency}{other_total:>10,.2f} ({other_pct:>5.1f}%)")
        
        # Financial Health Indicators
        print("\n" + "-" * 60)
        print("FINANCIAL HEALTH".center(60))
        print("-" * 60)
        
        # Calculate metrics
        if month_income > 0:
            expense_to_income_ratio = (month_expenses / month_income) * 100
            print(f"Expense-to-Income Ratio: {expense_to_income_ratio:.1f}%")
            
            if expense_to_income_ratio < 50:
                print("Excellent! You're spending less than half your income.")
            elif expense_to_income_ratio < 70:
                print("Good! You're maintaining healthy spending habits.")
            elif expense_to_income_ratio < 90:
                print("Caution: You're spending most of your income.")
            else:
                print("Alert: You're spending at or above your income!")
        
        if all_investments:
            investment_ratio = (total_investment_value / total_income * 100) if total_income > 0 else 0
            print(f"Investment-to-Income Ratio: {investment_ratio:.1f}%")
        
        # Emergency Fund Check (assuming Emergency Fund is an investment purpose)
        emergency_funds = [
            inv for inv in all_investments
            if 'emergency' in inv.get('purpose', '').lower()
        ]
        if emergency_funds:
            emergency_total = sum(inv.get('current_value', inv['amount']) for inv in emergency_funds)
            print(f"\nEmergency Fund: {currency}{emergency_total:,.2f}")
            
            # Typically 3-6 months of expenses is recommended
            avg_monthly_expenses = month_expenses if month_expenses > 0 else (total_expenses / 6)
            months_covered = (emergency_total / avg_monthly_expenses) if avg_monthly_expenses > 0 else 0
            print(f"   Covers approximately {months_covered:.1f} months of expenses")
            
            if months_covered >= 6:
                print("   Excellent emergency fund!")
            elif months_covered >= 3:
                print("   Good emergency fund coverage")
            else:
                print("   Consider building your emergency fund")
        
        print("\n" + "="*60)
        
        # Quick Actions
        print("\nQuick Tips:")
        if month_income > 0 and month_savings_rate < savings_goal:
            shortfall = month_income * (savings_goal / 100) - month_total_saved
            print(f"   • To meet your savings goal, save an additional {currency}{shortfall:,.2f}")
            print(f"     (reduce expenses or increase income/investments)")
        
        if month_income > 0 and month_savings_rate > savings_goal:
            print(f"   • Great job! You're exceeding your savings goal by {month_savings_rate - savings_goal:.1f}%")
        
        if not all_investments:
            print(f"   • Start building your investment portfolio for long-term growth")
        
        if not emergency_funds and all_investments:
            print(f"   • Consider allocating some investments to an emergency fund")
        
        print("="*60)
    
    def show_previous_months(self):
        """Display overview of previous months"""
        from datetime import datetime
        
        print("\n" + "="*60)
        print("PREVIOUS MONTHS OVERVIEW".center(60))
        print("="*60)
        
        # Get data
        all_income = self.data_manager.get_all_income()
        all_expenses = self.data_manager.get_all_expenses()
        currency = self.data_manager.get_currency()
        savings_goal = self.data_manager.get_savings_goal()
        
        # Get unique months from the data
        months = set()
        for entry in all_income:
            months.add(entry['date'][:7])  # YYYY-MM format
        for entry in all_expenses:
            months.add(entry['date'][:7])
        
        if not months:
            print("\nNo data available yet.")
            return
        
        # Sort months in descending order (most recent first)
        sorted_months = sorted(months, reverse=True)
        
        # Current month
        current_month = datetime.now().strftime("%Y-%m")
        
        # Remove current month from list
        previous_months = [m for m in sorted_months if m != current_month]
        
        if not previous_months:
            print("\nNo previous month data available yet.")
            print("Current month data can be viewed in the main dashboard.")
            return
        
        # Display menu to select a month
        print("\nSelect a month to view:")
        print("-" * 60)
        for i, month in enumerate(previous_months, 1):
            month_obj = datetime.strptime(month, "%Y-%m")
            month_name = month_obj.strftime("%B %Y")
            print(f"[{i}] {month_name}")
        print("[0] Back to Main Menu")
        print("-" * 60)
        
        try:
            choice = input("\nSelect a month: ").strip()
            if choice == "0":
                return
            
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(previous_months):
                selected_month = previous_months[choice_idx]
                self._show_month_detail(selected_month)
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    def _show_month_detail(self, month):
        """Display detailed overview for a specific month"""
        from datetime import datetime
        
        month_obj = datetime.strptime(month, "%Y-%m")
        month_name = month_obj.strftime("%B %Y")
        
        currency = self.data_manager.get_currency()
        savings_goal = self.data_manager.get_savings_goal()
        
        # Get all data
        all_income = self.data_manager.get_all_income()
        all_expenses = self.data_manager.get_all_expenses()
        
        # Filter data for the selected month
        month_income = sum(
            entry['amount'] for entry in all_income
            if entry['date'].startswith(month)
        )
        month_expenses = sum(
            entry['amount'] for entry in all_expenses
            if entry['date'].startswith(month) and entry['category'].lower() != 'investment'
        )
        month_investments = sum(
            entry['amount'] for entry in all_expenses
            if entry['date'].startswith(month) and entry['category'].lower() == 'investment'
        )
        
        # Calculations
        month_net_cash = month_income - month_expenses - month_investments
        month_total_saved = month_net_cash + month_investments
        month_savings_rate = (month_total_saved / month_income * 100) if month_income > 0 else 0
        
        # Display Month Summary
        print("\n" + "="*60)
        print(month_name.center(60))
        print("="*60)
        print(f"Income:              {currency}{month_income:>15,.2f}")
        print(f"Expenses:            {currency}{month_expenses:>15,.2f}")
        print("-" * 60)
        print(f"Total Saved:         {currency}{month_total_saved:>15,.2f}")
        print(f"  • Invested:        {currency}{month_investments:>15,.2f}")
        print(f"  • Cash Remaining:  {currency}{month_net_cash:>15,.2f}")
        print(f"Savings Rate:        {month_savings_rate:>15.1f}%")
        
        # Savings Goal Check
        print("\n" + "-" * 60)
        print("SAVINGS GOAL CHECK".center(60))
        print("-" * 60)
        print(f"Target Savings Rate: {savings_goal}%")
        print(f"Actual Savings Rate: {month_savings_rate:.1f}%")
        
        if month_income > 0:
            target_savings = month_income * (savings_goal / 100)
            actual_savings = month_total_saved
            difference = actual_savings - target_savings
            
            print(f"Target Savings: {currency}{target_savings:,.2f}")
            print(f"Actual Savings: {currency}{actual_savings:,.2f}")
            
            if month_savings_rate >= savings_goal:
                print(f"✓ GOAL MET! Saved {currency}{difference:,.2f} more than target!")
            else:
                print(f"✗ Below target by {currency}{abs(difference):,.2f}")
                percentage_to_goal = (month_savings_rate / savings_goal * 100) if savings_goal > 0 else 0
                print(f"   Achieved {percentage_to_goal:.1f}% of savings goal")
        else:
            print("No income recorded for this month")
        
        # Expense Breakdown
        month_expenses_list = [
            entry for entry in all_expenses
            if entry['date'].startswith(month)
        ]
        
        if month_expenses_list:
            print("\n" + "-" * 60)
            print(f"EXPENSE BREAKDOWN".center(60))
            print("-" * 60)
            
            # Group by category
            by_category = {}
            for entry in month_expenses_list:
                category = entry['category']
                if category not in by_category:
                    by_category[category] = 0
                by_category[category] += entry['amount']
            
            # Sort by amount
            total_expenses = sum(by_category.values())
            sorted_categories = sorted(by_category.items(), key=lambda x: x[1], reverse=True)
            
            for category, amount in sorted_categories:
                percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
                print(f"{category:.<30} {currency}{amount:>10,.2f} ({percentage:>5.1f}%)")
        
        # Financial Health
        print("\n" + "-" * 60)
        print("FINANCIAL HEALTH".center(60))
        print("-" * 60)
        
        if month_income > 0:
            expense_to_income_ratio = (month_expenses / month_income) * 100
            print(f"Expense-to-Income Ratio: {expense_to_income_ratio:.1f}%")
            
            if expense_to_income_ratio < 50:
                print("Excellent! Spending less than half of income.")
            elif expense_to_income_ratio < 70:
                print("Good! Maintaining healthy spending habits.")
            elif expense_to_income_ratio < 90:
                print("Caution: Spending most of income.")
            else:
                print("Alert: Spending at or above income!")
        
        print("\n" + "="*60)
        input("\nPress Enter to continue...")
    
    def show_previous_months(self):
        """Display overview of previous months"""
        from datetime import datetime
        
        print("\n" + "="*60)
        print("PREVIOUS MONTHS OVERVIEW".center(60))
        print("="*60)
        
        # Get data
        all_income = self.data_manager.get_all_income()
        all_expenses = self.data_manager.get_all_expenses()
        currency = self.data_manager.get_currency()
        savings_goal = self.data_manager.get_savings_goal()
        
        # Get unique months from the data
        months = set()
        for entry in all_income:
            months.add(entry['date'][:7])  # YYYY-MM format
        for entry in all_expenses:
            months.add(entry['date'][:7])
        
        if not months:
            print("\nNo data available yet.")
            return
        
        # Sort months in descending order (most recent first)
        sorted_months = sorted(months, reverse=True)
        
        # Current month
        current_month = datetime.now().strftime("%Y-%m")
        
        # Remove current month from list
        previous_months = [m for m in sorted_months if m != current_month]
        
        if not previous_months:
            print("\nNo previous month data available yet.")
            print("Current month data can be viewed in the main dashboard.")
            return
        
        # Display menu to select a month
        print("\nSelect a month to view:")
        print("-" * 60)
        for i, month in enumerate(previous_months, 1):
            month_obj = datetime.strptime(month, "%Y-%m")
            month_name = month_obj.strftime("%B %Y")
            print(f"[{i}] {month_name}")
        print("[0] Back to Main Menu")
        print("-" * 60)
        
        try:
            choice = input("\nSelect a month: ").strip()
            if choice == "0":
                return
            
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(previous_months):
                selected_month = previous_months[choice_idx]
                self._show_month_detail(selected_month)
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    def _show_month_detail(self, month):
        """Display detailed overview for a specific month"""
        from datetime import datetime
        
        month_obj = datetime.strptime(month, "%Y-%m")
        month_name = month_obj.strftime("%B %Y")
        
        currency = self.data_manager.get_currency()
        savings_goal = self.data_manager.get_savings_goal()
        
        # Get all data
        all_income = self.data_manager.get_all_income()
        all_expenses = self.data_manager.get_all_expenses()
        
        # Filter data for the selected month
        month_income = sum(
            entry['amount'] for entry in all_income
            if entry['date'].startswith(month)
        )
        month_expenses = sum(
            entry['amount'] for entry in all_expenses
            if entry['date'].startswith(month) and entry['category'].lower() != 'investment'
        )
        month_investments = sum(
            entry['amount'] for entry in all_expenses
            if entry['date'].startswith(month) and entry['category'].lower() == 'investment'
        )
        
        # Calculations
        month_net_cash = month_income - month_expenses - month_investments
        month_total_saved = month_net_cash + month_investments
        month_savings_rate = (month_total_saved / month_income * 100) if month_income > 0 else 0
        
        # Display Month Summary
        print("\n" + "="*60)
        print(month_name.center(60))
        print("="*60)
        print(f"Income:              {currency}{month_income:>15,.2f}")
        print(f"Expenses:            {currency}{month_expenses:>15,.2f}")
        print("-" * 60)
        print(f"Total Saved:         {currency}{month_total_saved:>15,.2f}")
        print(f"  • Invested:        {currency}{month_investments:>15,.2f}")
        print(f"  • Cash Remaining:  {currency}{month_net_cash:>15,.2f}")
        print(f"Savings Rate:        {month_savings_rate:>15.1f}%")
        
        # Savings Goal Check
        print("\n" + "-" * 60)
        print("SAVINGS GOAL CHECK".center(60))
        print("-" * 60)
        print(f"Target Savings Rate: {savings_goal}%")
        print(f"Actual Savings Rate: {month_savings_rate:.1f}%")
        
        if month_income > 0:
            target_savings = month_income * (savings_goal / 100)
            actual_savings = month_total_saved
            difference = actual_savings - target_savings
            
            print(f"Target Savings: {currency}{target_savings:,.2f}")
            print(f"Actual Savings: {currency}{actual_savings:,.2f}")
            
            if month_savings_rate >= savings_goal:
                print(f"✓ GOAL MET! Saved {currency}{difference:,.2f} more than target!")
            else:
                print(f"✗ Below target by {currency}{abs(difference):,.2f}")
                percentage_to_goal = (month_savings_rate / savings_goal * 100) if savings_goal > 0 else 0
                print(f"   Achieved {percentage_to_goal:.1f}% of savings goal")
        else:
            print("No income recorded for this month")
        
        # Expense Breakdown
        month_expenses_list = [
            entry for entry in all_expenses
            if entry['date'].startswith(month)
        ]
        
        if month_expenses_list:
            print("\n" + "-" * 60)
            print(f"EXPENSE BREAKDOWN".center(60))
            print("-" * 60)
            
            # Group by category
            by_category = {}
            for entry in month_expenses_list:
                category = entry['category']
                if category not in by_category:
                    by_category[category] = 0
                by_category[category] += entry['amount']
            
            # Sort by amount
            total_expenses = sum(by_category.values())
            sorted_categories = sorted(by_category.items(), key=lambda x: x[1], reverse=True)
            
            for category, amount in sorted_categories:
                percentage = (amount / total_expenses * 100) if total_expenses > 0 else 0
                print(f"{category:.<30} {currency}{amount:>10,.2f} ({percentage:>5.1f}%)")
        
        # Financial Health
        print("\n" + "-" * 60)
        print("FINANCIAL HEALTH".center(60))
        print("-" * 60)
        
        if month_income > 0:
            expense_to_income_ratio = (month_expenses / month_income) * 100
            print(f"Expense-to-Income Ratio: {expense_to_income_ratio:.1f}%")
            
            if expense_to_income_ratio < 50:
                print("Excellent! Spending less than half of income.")
            elif expense_to_income_ratio < 70:
                print("Good! Maintaining healthy spending habits.")
            elif expense_to_income_ratio < 90:
                print("Caution: Spending most of income.")
            else:
                print("Alert: Spending at or above income!")
        
        print("\n" + "="*60)
        input("\nPress Enter to continue...")
