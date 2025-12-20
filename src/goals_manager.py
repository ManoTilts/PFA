"""
Goals Manager - Track savings goals for future expenses
"""

from datetime import datetime


class GoalsManager:
    def __init__(self, data_manager):
        self.data_manager = data_manager
    
    def create_goal(self):
        """Create a new savings goal"""
        print("\n" + "="*60)
        print("CREATE SAVINGS GOAL".center(60))
        print("="*60)
        
        name = input("Enter goal name (e.g., 'PC Upgrade', 'Vacation'): ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        
        try:
            target_amount = float(input("Enter target amount: ").strip())
            if target_amount <= 0:
                print("Target amount must be positive.")
                return
            
            monthly_target = float(input("Enter monthly savings target (optional, press Enter to skip): ").strip() or "0")
            if monthly_target < 0:
                print("Monthly target cannot be negative.")
                return
            
            deadline_input = input("Target completion date (YYYY-MM) or press Enter to skip: ").strip()
            deadline = None
            if deadline_input:
                try:
                    datetime.strptime(deadline_input, "%Y-%m")
                    deadline = deadline_input
                except ValueError:
                    print("Invalid date format. Skipping deadline.")
            
            description = input("Enter description (optional): ").strip()
            
            date = datetime.now().strftime("%Y-%m-%d")
            entry = self.data_manager.add_goal(name, target_amount, monthly_target, deadline, description, date)
            
            currency = self.data_manager.get_currency()
            print(f"\nGoal created successfully!")
            print(f"   Name: {name}")
            print(f"   Target: {currency}{target_amount:,.2f}")
            if monthly_target > 0:
                print(f"   Monthly target: {currency}{monthly_target:,.2f}")
            if deadline:
                print(f"   Deadline: {deadline}")
            
        except ValueError:
            print("Invalid amount. Please enter a number.")
    
    def add_contribution(self):
        """Add money towards a goal"""
        goals = self.data_manager.get_active_goals()
        
        if not goals:
            print("\nNo active goals found. Create a goal first.")
            return
        
        currency = self.data_manager.get_currency()
        print("\n" + "="*60)
        print("CONTRIBUTE TO GOAL".center(60))
        print("="*60)
        
        print("\nActive Goals:")
        for i, goal in enumerate(goals, 1):
            saved = goal.get('saved', 0)
            remaining = goal['target_amount'] - saved
            progress = (saved / goal['target_amount']) * 100
            print(f"[{i}] {goal['name']}")
            print(f"    Target: {currency}{goal['target_amount']:,.2f}")
            print(f"    Saved: {currency}{saved:,.2f} ({progress:.1f}%)")
            print(f"    Remaining: {currency}{remaining:,.2f}")
        
        try:
            choice = int(input("\nSelect goal number: ").strip())
            if not (1 <= choice <= len(goals)):
                print("Invalid selection.")
                return
            
            goal = goals[choice - 1]
            saved = goal.get('saved', 0)
            remaining = goal['target_amount'] - saved
            
            print(f"\nContributing to: {goal['name']}")
            print(f"Remaining to reach goal: {currency}{remaining:,.2f}")
            
            amount = float(input("Enter contribution amount: ").strip())
            if amount <= 0:
                print("Amount must be positive.")
                return
            
            date = datetime.now().strftime("%Y-%m-%d")
            self.data_manager.add_goal_contribution(goal['_id'], amount, date)
            
            new_saved = saved + amount
            new_remaining = goal['target_amount'] - new_saved
            progress = (new_saved / goal['target_amount']) * 100
            
            print(f"\nContribution recorded!")
            print(f"   Amount: {currency}{amount:,.2f}")
            print(f"   Total saved: {currency}{new_saved:,.2f} ({progress:.1f}%)")
            
            if new_remaining <= 0:
                print(f"\n🎉 Goal achieved! You've reached your target!")
            else:
                print(f"   Remaining: {currency}{new_remaining:,.2f}")
            
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
    
    def view_all_goals(self):
        """View all savings goals"""
        all_goals = self.data_manager.get_all_goals()
        
        if not all_goals:
            print("\nNo savings goals found.")
            return
        
        currency = self.data_manager.get_currency()
        current_month = datetime.now().strftime("%Y-%m")
        
        print("\n" + "="*60)
        print("SAVINGS GOALS".center(60))
        print("="*60)
        
        active_goals = [g for g in all_goals if g['target_amount'] > g.get('saved', 0)]
        completed_goals = [g for g in all_goals if g['target_amount'] <= g.get('saved', 0)]
        
        total_target = sum(g['target_amount'] for g in active_goals)
        total_saved = sum(g.get('saved', 0) for g in active_goals)
        total_remaining = total_target - total_saved
        
        # Current month contributions
        month_contributions = 0
        for goal in all_goals:
            for contribution in goal.get('contributions', []):
                if contribution['date'].startswith(current_month):
                    month_contributions += contribution['amount']
        
        # Total monthly targets
        total_monthly_target = sum(g.get('monthly_target', 0) for g in active_goals)
        
        print(f"\nTotal Target Amount: {currency}{total_target:,.2f}")
        print(f"Total Saved: {currency}{total_saved:,.2f}")
        print(f"Total Remaining: {currency}{total_remaining:,.2f}")
        if total_monthly_target > 0:
            print(f"\nCombined Monthly Target: {currency}{total_monthly_target:,.2f}")
        print(f"Contributed This Month: {currency}{month_contributions:,.2f}")
        
        if total_monthly_target > 0:
            month_progress = (month_contributions / total_monthly_target) * 100
            print(f"Monthly Progress: {month_progress:.1f}%")
        
        if active_goals:
            print("\n" + "-"*60)
            print("ACTIVE GOALS".center(60))
            print("-"*60)
            
            for i, goal in enumerate(active_goals, 1):
                saved = goal.get('saved', 0)
                remaining = goal['target_amount'] - saved
                progress = (saved / goal['target_amount']) * 100
                
                print(f"\n[{i}] {goal['name']}")
                if goal.get('description'):
                    print(f"    {goal['description']}")
                print(f"    Created: {goal['date']}")
                print(f"    Target: {currency}{goal['target_amount']:,.2f}")
                print(f"    Saved: {currency}{saved:,.2f} ({progress:.1f}%)")
                print(f"    Remaining: {currency}{remaining:,.2f}")
                
                if goal.get('monthly_target', 0) > 0:
                    print(f"    Monthly target: {currency}{goal['monthly_target']:,.2f}")
                    
                    # Calculate months needed at current rate
                    months_needed = remaining / goal['monthly_target']
                    print(f"    Months to goal: {months_needed:.1f}")
                
                if goal.get('deadline'):
                    print(f"    ⏰ Deadline: {goal['deadline']}")
                    
                    # Check if pace is on track
                    if goal.get('monthly_target', 0) > 0:
                        current_date = datetime.now()
                        deadline_date = datetime.strptime(goal['deadline'], "%Y-%m")
                        months_left = (deadline_date.year - current_date.year) * 12 + (deadline_date.month - current_date.month)
                        
                        if months_left > 0:
                            required_monthly = remaining / months_left
                            print(f"    Required monthly: {currency}{required_monthly:.2f}")
                            
                            if required_monthly > goal['monthly_target']:
                                print(f"    ⚠️  Current target too low by {currency}{required_monthly - goal['monthly_target']:.2f}/mo")
                
                if goal.get('contributions'):
                    print(f"    Contributions made: {len(goal['contributions'])}")
        
        if completed_goals:
            print("\n" + "-"*60)
            print("COMPLETED GOALS".center(60))
            print("-"*60)
            
            for goal in completed_goals:
                saved = goal.get('saved', 0)
                print(f"\n✓ {goal['name']}")
                print(f"    Target: {currency}{goal['target_amount']:,.2f}")
                print(f"    Final amount: {currency}{saved:,.2f}")
                print(f"    Created: {goal['date']}")
                if goal.get('contributions'):
                    last_contribution = goal['contributions'][-1]['date']
                    print(f"    Completed: {last_contribution}")
        
        print("\n" + "="*60)
    
    def edit_goal(self):
        """Edit an existing goal"""
        goals = self.data_manager.get_active_goals()
        
        if not goals:
            print("\nNo active goals found.")
            return
        
        currency = self.data_manager.get_currency()
        print("\n" + "="*60)
        print("EDIT GOAL".center(60))
        print("="*60)
        
        for i, goal in enumerate(goals, 1):
            print(f"[{i}] {goal['name']}")
            print(f"    Monthly target: {currency}{goal.get('monthly_target', 0):,.2f}")
        
        try:
            choice = int(input("\nSelect goal to edit: ").strip())
            if not (1 <= choice <= len(goals)):
                print("Invalid selection.")
                return
            
            goal = goals[choice - 1]
            
            print(f"\nEditing: {goal['name']}")
            print(f"Current monthly target: {currency}{goal.get('monthly_target', 0):,.2f}")
            
            new_target = input("Enter new monthly target (or press Enter to keep current): ").strip()
            if new_target:
                try:
                    new_target_amount = float(new_target)
                    if new_target_amount < 0:
                        print("Monthly target cannot be negative.")
                        return
                    
                    self.data_manager.update_goal_monthly_target(goal['_id'], new_target_amount)
                    print(f"\nMonthly target updated to {currency}{new_target_amount:,.2f}")
                except ValueError:
                    print("Invalid amount.")
            else:
                print("\nNo changes made.")
            
        except ValueError:
            print("Invalid input.")
    
    def view_contribution_history(self):
        """View contribution history across all goals"""
        all_goals = self.data_manager.get_all_goals()
        
        if not all_goals:
            print("\nNo goals found.")
            return
        
        currency = self.data_manager.get_currency()
        print("\n" + "="*60)
        print("CONTRIBUTION HISTORY".center(60))
        print("="*60)
        
        all_contributions = []
        for goal in all_goals:
            for contribution in goal.get('contributions', []):
                all_contributions.append({
                    'date': contribution['date'],
                    'amount': contribution['amount'],
                    'goal': goal['name']
                })
        
        if not all_contributions:
            print("\nNo contributions recorded yet.")
            return
        
        # Sort by date
        all_contributions.sort(key=lambda x: x['date'], reverse=True)
        
        total_contributed = sum(c['amount'] for c in all_contributions)
        
        print(f"\nTotal Contributed: {currency}{total_contributed:,.2f}")
        print(f"Total Contributions: {len(all_contributions)}")
        
        print("\n" + "-"*60)
        print("RECENT CONTRIBUTIONS".center(60))
        print("-"*60)
        
        for contribution in all_contributions[:15]:  # Show last 15
            print(f"\n{contribution['date']}: {currency}{contribution['amount']:,.2f}")
            print(f"   → {contribution['goal']}")
        
        if len(all_contributions) > 15:
            print(f"\n... and {len(all_contributions) - 15} more contribution(s)")
        
        print("="*60)
