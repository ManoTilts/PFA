"""
Debt & Overexpense Manager - Track overspending and repayment goals
"""

from datetime import datetime


class DebtManager:
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def add_debt(self):
        """Record a debt or overexpense"""
        print("\n" + "="*60)
        print("RECORD OVEREXPENSE/DEBT".center(60))
        print("="*60)
        
        try:
            amount = float(input("Enter overexpense amount (positive number): ").strip())
            if amount <= 0:
                print("Amount must be positive.")
                return
            
            description = input("Enter description (e.g., 'November overspending'): ").strip()
            if not description:
                print("Description cannot be empty.")
                return
            
            # Ask for month limit
            month_limit_input = input("\nSet repayment deadline (months from now, or press Enter to skip): ").strip()
            month_limit = None
            target_date = None
            
            if month_limit_input:
                try:
                    month_limit = int(month_limit_input)
                    if month_limit <= 0:
                        print("Using no deadline.")
                        month_limit = None
                    else:
                        # Calculate target date
                        from datetime import datetime
                        from dateutil.relativedelta import relativedelta
                        target_date = (datetime.now() + relativedelta(months=month_limit)).strftime("%Y-%m")
                        print(f"Target payoff date: {target_date}")
                except ValueError:
                    print("Invalid number, skipping deadline.")
                except ImportError:
                    # If dateutil not available, calculate roughly
                    print("Note: Install python-dateutil for precise date calculations")
                    month_limit = None
            
            date = datetime.now().strftime("%Y-%m-%d")
            
            entry = self.data_manager.add_debt(amount, description, date, month_limit, target_date)
            currency = self.data_manager.get_currency()
            print(f"\nOverexpense recorded!")
            print(f"   Amount: {currency}{amount:,.2f}")
            print(f"   Description: {description}")
            print(f"   Date: {date}")
            if month_limit:
                print(f"   Deadline: {month_limit} months (target: {target_date})")
            
        except ValueError:
            print("Invalid amount. Please enter a number.")
    
    def add_repayment(self):
        """Record a repayment towards debt"""
        debts = self.data_manager.get_active_debts()
        
        if not debts:
            print("\nNo active debts found.")
            return
        
        currency = self.data_manager.get_currency()
        print("\n" + "="*60)
        print("RECORD REPAYMENT".center(60))
        print("="*60)
        
        print("\nActive Debts:")
        for i, debt in enumerate(debts, 1):
            remaining = debt['amount'] - debt.get('paid', 0)
            print(f"[{i}] {debt['description']}")
            print(f"    Total: {currency}{debt['amount']:,.2f}")
            print(f"    Paid: {currency}{debt.get('paid', 0):,.2f}")
            print(f"    Remaining: {currency}{remaining:,.2f}")
        
        try:
            choice = int(input("\nSelect debt number: ").strip())
            if not (1 <= choice <= len(debts)):
                print("Invalid selection.")
                return
            
            debt = debts[choice - 1]
            remaining = debt['amount'] - debt.get('paid', 0)
            
            print(f"\nRepaying: {debt['description']}")
            print(f"Remaining balance: {currency}{remaining:,.2f}")
            
            amount = float(input("Enter repayment amount: ").strip())
            if amount <= 0:
                print("Amount must be positive.")
                return
            
            if amount > remaining:
                print(f"Warning: Payment exceeds remaining balance!")
                confirm = input(f"Pay full remaining {currency}{remaining:,.2f} instead? (y/n): ").strip().lower()
                if confirm == 'y':
                    amount = remaining
                else:
                    return
            
            date = datetime.now().strftime("%Y-%m-%d")
            self.data_manager.add_debt_payment(debt['_id'], amount, date)
            
            new_paid = debt.get('paid', 0) + amount
            new_remaining = debt['amount'] - new_paid
            
            print(f"\nRepayment recorded!")
            print(f"   Amount paid: {currency}{amount:,.2f}")
            print(f"   Total paid: {currency}{new_paid:,.2f}")
            print(f"   Remaining: {currency}{new_remaining:,.2f}")
            
            if new_remaining <= 0:
                print(f"\n🎉 Debt fully paid off!")
            
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
    
    def set_monthly_goal(self):
        """Set monthly repayment goal"""
        print("\n" + "="*60)
        print("SET MONTHLY REPAYMENT GOAL".center(60))
        print("="*60)
        
        current_goal = self.data_manager.get_debt_repayment_goal()
        currency = self.data_manager.get_currency()
        
        if current_goal > 0:
            print(f"\nCurrent monthly goal: {currency}{current_goal:,.2f}")
        else:
            print("\nNo monthly goal set yet.")
        
        try:
            amount = float(input("Enter new monthly repayment goal (or 0 to remove): ").strip())
            if amount < 0:
                print("Amount cannot be negative.")
                return
            
            self.data_manager.set_debt_repayment_goal(amount)
            
            if amount == 0:
                print("\nMonthly repayment goal removed.")
            else:
                print(f"\nMonthly repayment goal updated to {currency}{amount:,.2f}")
            print("Note: This is separate from your regular savings goal.")
            
        except ValueError:
            print("Invalid amount. Please enter a number.")
    
    def view_debt_status(self):
        """View all debts and repayment status"""
        all_debts = self.data_manager.get_all_debts()
        
        if not all_debts:
            print("\nNo debts recorded. Great job!")
            return
        
        currency = self.data_manager.get_currency()
        current_month = datetime.now().strftime("%Y-%m")
        repayment_goal = self.data_manager.get_debt_repayment_goal()
        
        print("\n" + "="*60)
        print("DEBT & OVEREXPENSE STATUS".center(60))
        print("="*60)
        
        active_debts = [d for d in all_debts if d['amount'] > d.get('paid', 0)]
        paid_debts = [d for d in all_debts if d['amount'] <= d.get('paid', 0)]
        
        total_debt = sum(d['amount'] for d in active_debts)
        total_paid_on_active = sum(d.get('paid', 0) for d in active_debts)
        total_remaining = total_debt - total_paid_on_active
        
        # Current month payments
        month_payments = 0
        for debt in all_debts:
            for payment in debt.get('payments', []):
                if payment['date'].startswith(current_month):
                    month_payments += payment['amount']
        
        print(f"\nTotal Outstanding Debt: {currency}{total_remaining:,.2f}")
        print(f"Monthly Repayment Goal: {currency}{repayment_goal:,.2f}")
        print(f"Paid This Month: {currency}{month_payments:,.2f}")
        
        if repayment_goal > 0:
            progress = (month_payments / repayment_goal) * 100
            print(f"Monthly Progress: {progress:.1f}%")
            
            if month_payments >= repayment_goal:
                print("✓ Monthly goal achieved!")
            else:
                remaining_goal = repayment_goal - month_payments
                print(f"   Remaining to meet goal: {currency}{remaining_goal:,.2f}")
        
        # Check if any debt has deadline that won't be met
        if repayment_goal > 0 and total_remaining > 0:
            months_to_payoff = total_remaining / repayment_goal
            print(f"\nAt current goal, payoff in: {months_to_payoff:.1f} months")
        
        if active_debts:
            print("\n" + "-"*60)
            print("ACTIVE DEBTS".center(60))
            print("-"*60)
            
            for i, debt in enumerate(active_debts, 1):
                remaining = debt['amount'] - debt.get('paid', 0)
                progress_pct = (debt.get('paid', 0) / debt['amount']) * 100
                
                print(f"\n[{i}] {debt['description']}")
                print(f"    Date: {debt['date']}")
                print(f"    Total: {currency}{debt['amount']:,.2f}")
                print(f"    Paid: {currency}{debt.get('paid', 0):,.2f} ({progress_pct:.1f}%)")
                print(f"    Remaining: {currency}{remaining:,.2f}")
                
                if debt.get('payments'):
                    print(f"    Payments made: {len(debt['payments'])}")
                
                # Show deadline info
                if debt.get('month_limit') and debt.get('target_date'):
                    target_date = debt['target_date']
                    print(f"    ⏰ Deadline: {target_date} ({debt['month_limit']} months)")
                    
                    # Calculate required monthly payment
                    if repayment_goal > 0:
                        required_monthly = remaining / debt['month_limit']
                        print(f"    Required monthly: {currency}{required_monthly:,.2f}")
                        
                        if required_monthly > repayment_goal:
                            print(f"    ⚠️  Current goal ({currency}{repayment_goal:,.2f}/mo) is too low!")
                            print(f"        Need to increase by {currency}{required_monthly - repayment_goal:,.2f}/mo")
        
        if paid_debts:
            print("\n" + "-"*60)
            print("PAID OFF DEBTS".center(60))
            print("-"*60)
            
            for debt in paid_debts:
                print(f"\n✓ {debt['description']}")
                print(f"    Amount: {currency}{debt['amount']:,.2f}")
                print(f"    Date created: {debt['date']}")
                if debt.get('payments'):
                    last_payment = debt['payments'][-1]['date']
                    print(f"    Paid off: {last_payment}")
        
        print("\n" + "="*60)
    
    def view_repayment_history(self):
        """View detailed repayment history"""
        all_debts = self.data_manager.get_all_debts()
        
        if not all_debts:
            print("\nNo debt history found.")
            return
        
        currency = self.data_manager.get_currency()
        print("\n" + "="*60)
        print("REPAYMENT HISTORY".center(60))
        print("="*60)
        
        all_payments = []
        for debt in all_debts:
            for payment in debt.get('payments', []):
                all_payments.append({
                    'date': payment['date'],
                    'amount': payment['amount'],
                    'debt': debt['description']
                })
        
        if not all_payments:
            print("\nNo repayments recorded yet.")
            return
        
        # Sort by date
        all_payments.sort(key=lambda x: x['date'], reverse=True)
        
        total_repaid = sum(p['amount'] for p in all_payments)
        
        print(f"\nTotal Amount Repaid: {currency}{total_repaid:,.2f}")
        print(f"Total Payments: {len(all_payments)}")
        
        print("\n" + "-"*60)
        print("RECENT PAYMENTS".center(60))
        print("-"*60)
        
        for payment in all_payments[:10]:  # Show last 10 payments
            print(f"\n{payment['date']}: {currency}{payment['amount']:,.2f}")
            print(f"   → {payment['debt']}")
        
        if len(all_payments) > 10:
            print(f"\n... and {len(all_payments) - 10} more payment(s)")
        
        print("="*60)
