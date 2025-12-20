"""
Investment Manager - Handles investment tracking and portfolio management
"""

from datetime import datetime


class InvestmentManager:
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.common_types = [
            "Stocks", "Bonds", "ETF", "Mutual Fund", 
            "Real Estate", "Cryptocurrency", "Savings Account",
            "CD", "Retirement Account", "Other"
        ]
        self.common_purposes = [
            "Retirement", "Emergency Fund", "House Down Payment",
            "Education", "Vacation", "Short-term Savings",
            "Long-term Growth", "Passive Income", "Other"
        ]
    
    def add_investment(self):
        """Add a new investment entry"""
        print("\n" + "="*60)
        print("ADD NEW INVESTMENT".center(60))
        print("="*60)
        
        name = input("Enter investment name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        
        try:
            amount = float(input("Enter initial amount: ").strip())
            if amount <= 0:
                print("Amount must be positive.")
                return
        except ValueError:
            print("Invalid amount. Please enter a number.")
            return
        
        print("\nCommon investment types:")
        for i, t in enumerate(self.common_types, 1):
            print(f"  [{i}] {t}", end="   " if i % 3 != 0 else "\n")
        print()
        
        inv_type = input("\nEnter investment type (or select number): ").strip()
        
        # Check if user entered a number
        try:
            type_num = int(inv_type)
            if 1 <= type_num <= len(self.common_types):
                inv_type = self.common_types[type_num - 1]
        except ValueError:
            pass
        
        if not inv_type:
            print("Investment type cannot be empty.")
            return
        
        print("\nCommon purposes:")
        for i, p in enumerate(self.common_purposes, 1):
            print(f"  [{i}] {p}", end="   " if i % 3 != 0 else "\n")
        print()
        
        purpose = input("\nEnter purpose (or select number): ").strip()
        
        # Check if user entered a number
        try:
            purpose_num = int(purpose)
            if 1 <= purpose_num <= len(self.common_purposes):
                purpose = self.common_purposes[purpose_num - 1]
        except ValueError:
            pass
        
        if not purpose:
            print("Purpose cannot be empty.")
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
        
        entry = self.data_manager.add_investment(name, amount, inv_type, purpose, date)
        currency = self.data_manager.get_currency()
        print(f"\nInvestment added successfully!")
        print(f"   Name: {name}")
        print(f"   Amount: {currency}{amount:,.2f}")
        print(f"   Type: {inv_type}")
        print(f"   Purpose: {purpose}")
        print(f"   Date: {date}")
    
    def view_all_investments(self):
        """Display all investment entries"""
        investments = self.data_manager.get_all_investments()
        
        if not investments:
            print("\nNo investments found.")
            return
        
        currency = self.data_manager.get_currency()
        print("\n" + "="*60)
        print("ALL INVESTMENTS".center(60))
        print("="*60)
        
        total_invested = 0
        total_current = 0
        
        for i, inv in enumerate(investments, 1):
            current_value = inv.get('current_value', inv['amount'])
            gain_loss = current_value - inv['amount']
            gain_loss_pct = (gain_loss / inv['amount']) * 100 if inv['amount'] > 0 else 0
            
            print(f"\n[{i}] {inv['name']}")
            print(f"    Type: {inv['type']}")
            print(f"    Purpose: {inv['purpose']}")
            print(f"    Initial: {currency}{inv['amount']:,.2f}")
            print(f"    Current: {currency}{current_value:,.2f}", end="")
            
            if gain_loss >= 0:
                print(f" (+{currency}{gain_loss:,.2f}, +{gain_loss_pct:.1f}%)")
            else:
                print(f" ({currency}{gain_loss:,.2f}, {gain_loss_pct:.1f}%)")
            
            print(f"    Date: {inv['date']}")
            
            total_invested += inv['amount']
            total_current += current_value
        
        total_gain_loss = total_current - total_invested
        total_gain_loss_pct = (total_gain_loss / total_invested) * 100 if total_invested > 0 else 0
        
        print("\n" + "-"*60)
        print(f"Total Invested: {currency}{total_invested:,.2f}")
        print(f"Current Value: {currency}{total_current:,.2f}")
        if total_gain_loss >= 0:
            print(f"Total Gain: {currency}{total_gain_loss:,.2f} (+{total_gain_loss_pct:.1f}%)")
        else:
            print(f"Total Loss: {currency}{total_gain_loss:,.2f} ({total_gain_loss_pct:.1f}%)")
        print("-"*60)
    
    def view_by_purpose(self):
        """Display investments grouped by purpose"""
        investments = self.data_manager.get_all_investments()
        
        if not investments:
            print("\nNo investments found.")
            return
        
        currency = self.data_manager.get_currency()
        
        # Group by purpose
        by_purpose = {}
        for inv in investments:
            purpose = inv['purpose']
            if purpose not in by_purpose:
                by_purpose[purpose] = []
            by_purpose[purpose].append(inv)
        
        print("\n" + "="*60)
        print("INVESTMENTS BY PURPOSE".center(60))
        print("="*60)
        
        for purpose in sorted(by_purpose.keys()):
            invs = by_purpose[purpose]
            purpose_total_invested = sum(inv['amount'] for inv in invs)
            purpose_total_current = sum(inv.get('current_value', inv['amount']) for inv in invs)
            
            print(f"\n{purpose}")
            print(f"   Initial Investment: {currency}{purpose_total_invested:,.2f}")
            print(f"   Current Value: {currency}{purpose_total_current:,.2f}")
            print(f"   Number of Investments: {len(invs)}")
            print(f"   Investments: {', '.join([inv['name'] for inv in invs])}")
        
        print("="*60)
    
    def view_summary(self):
        """Display investment summary with statistics"""
        investments = self.data_manager.get_all_investments()
        
        if not investments:
            print("\nNo investments found.")
            return
        
        currency = self.data_manager.get_currency()
        
        total_invested = sum(inv['amount'] for inv in investments)
        total_current = sum(inv.get('current_value', inv['amount']) for inv in investments)
        total_gain_loss = total_current - total_invested
        total_gain_loss_pct = (total_gain_loss / total_invested) * 100 if total_invested > 0 else 0
        
        # Group by type
        by_type = {}
        for inv in investments:
            inv_type = inv['type']
            if inv_type not in by_type:
                by_type[inv_type] = {'invested': 0, 'current': 0, 'count': 0}
            by_type[inv_type]['invested'] += inv['amount']
            by_type[inv_type]['current'] += inv.get('current_value', inv['amount'])
            by_type[inv_type]['count'] += 1
        
        # Group by purpose
        by_purpose = {}
        for inv in investments:
            purpose = inv['purpose']
            if purpose not in by_purpose:
                by_purpose[purpose] = 0
            by_purpose[purpose] += inv.get('current_value', inv['amount'])
        
        print("\n" + "="*60)
        print("INVESTMENT SUMMARY".center(60))
        print("="*60)
        
        print(f"\nTotal Invested: {currency}{total_invested:,.2f}")
        print(f"Current Value: {currency}{total_current:,.2f}")
        if total_gain_loss >= 0:
            print(f"Total Gain: {currency}{total_gain_loss:,.2f} (+{total_gain_loss_pct:.1f}%)")
        else:
            print(f"Total Loss: {currency}{total_gain_loss:,.2f} ({total_gain_loss_pct:.1f}%)")
        print(f"Total Investments: {len(investments)}")
        
        print("\n" + "-"*60)
        print("BY INVESTMENT TYPE".center(60))
        print("-"*60)
        
        for inv_type, data in sorted(by_type.items(), key=lambda x: x[1]['current'], reverse=True):
            percentage = (data['current'] / total_current) * 100
            gain_loss = data['current'] - data['invested']
            print(f"{inv_type:.<25} {currency}{data['current']:>12,.2f} ({percentage:>5.1f}%)")
            print(f"{'':.<25} {data['count']} investment(s), ", end="")
            if gain_loss >= 0:
                print(f"+{currency}{gain_loss:,.2f}")
            else:
                print(f"{currency}{gain_loss:,.2f}")
        
        print("\n" + "-"*60)
        print("BY PURPOSE".center(60))
        print("-"*60)
        
        for purpose, amount in sorted(by_purpose.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total_current) * 100
            print(f"{purpose:.<30} {currency}{amount:>12,.2f} ({percentage:>5.1f}%)")
        
        print("="*60)
    
    def update_investment_value(self):
        """Update the current value of an investment"""
        investments = self.data_manager.get_all_investments()
        
        if not investments:
            print("\nNo investments found.")
            return
        
        currency = self.data_manager.get_currency()
        print("\n" + "="*60)
        print("UPDATE INVESTMENT VALUE".center(60))
        print("="*60)
        
        for i, inv in enumerate(investments, 1):
            current_value = inv.get('current_value', inv['amount'])
            print(f"[{i}] {inv['name']} - Current: {currency}{current_value:,.2f}")
        
        try:
            choice = int(input("\nSelect investment number to update: ").strip())
            if 1 <= choice <= len(investments):
                index = choice - 1
                inv = investments[index]
                
                print(f"\nUpdating: {inv['name']}")
                print(f"Current value: {currency}{inv.get('current_value', inv['amount']):,.2f}")
                
                new_value = float(input(f"Enter new value: ").strip())
                if new_value < 0:
                    print("Value cannot be negative.")
                    return
                
                self.data_manager.update_investment_value(index, new_value)
                
                gain_loss = new_value - inv['amount']
                gain_loss_pct = (gain_loss / inv['amount']) * 100 if inv['amount'] > 0 else 0
                
                print(f"\nInvestment value updated!")
                print(f"   New value: {currency}{new_value:,.2f}")
                if gain_loss >= 0:
                    print(f"   Gain: {currency}{gain_loss:,.2f} (+{gain_loss_pct:.1f}%)")
                else:
                    print(f"   Loss: {currency}{gain_loss:,.2f} ({gain_loss_pct:.1f}%)")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input.")
