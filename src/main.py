"""
Personal Finance Assistant - Main Program
A comprehensive tool to manage your income, expenses, investments, and financial goals.
"""

from datetime import datetime
from data_manager import DataManager
from income import IncomeManager
from expenses import ExpenseManager
from investments import InvestmentManager
from dashboard import Dashboard
from debt_manager import DebtManager
from goals_manager import GoalsManager


class PersonalFinanceApp:
    def __init__(self):
        self.data_manager = DataManager()
        self.income_manager = IncomeManager(self.data_manager)
        self.expense_manager = ExpenseManager(self.data_manager)
        self.investment_manager = InvestmentManager(self.data_manager)
        self.dashboard = Dashboard(self.data_manager)
        self.debt_manager = DebtManager(self.data_manager)
        self.goals_manager = GoalsManager(self.data_manager)
    
    def display_main_menu(self):
        print("\n" + "="*60)
        print("PERSONAL FINANCE ASSISTANT".center(60))
        print("="*60)
        print("\n[1] Income Management")
        print("[2] Expense Management")
        print("[3] Investment Management")
        print("[4] Debt & Overexpense Management")
        print("[5] Savings Goals")
        print("[6] Financial Dashboard")
        print("[7] Settings & Goals")
        print("[0] Exit")
        print("\n" + "-"*60)
    
    def income_menu(self):
        while True:
            print("\n" + "="*60)
            print("INCOME MANAGEMENT".center(60))
            print("="*60)
            print("\n[1] Add Income Entry")
            print("[2] View All Income")
            print("[3] View Income Summary")
            print("[4] Investment Withdrawal")
            print("[0] Back to Main Menu")
            print("\n" + "-"*60)
            
            choice = input("Select an option: ").strip()
            
            if choice == "1":
                self.income_manager.add_income()
            elif choice == "2":
                self.income_manager.view_all_income()
            elif choice == "3":
                self.income_manager.view_summary()
            elif choice == "4":
                self.income_manager.investment_withdrawal()
            elif choice == "0":
                break
            else:
                print("Invalid option. Please try again.")
    
    def expense_menu(self):
        while True:
            print("\n" + "="*60)
            print("EXPENSE MANAGEMENT".center(60))
            print("="*60)
            print("\n[1] Add Expense")
            print("[2] Add Recurring Expense")
            print("[3] View All Expenses")
            print("[4] View Expenses by Category")
            print("[5] View Recurring Expenses")
            print("[6] Process Recurring Expenses (Apply for this month)")
            print("[7] Investment Deposit")
            print("[8] Simulate Expense")
            print("[0] Back to Main Menu")
            print("\n" + "-"*60)
            
            choice = input("Select an option: ").strip()
            
            if choice == "1":
                self.expense_manager.add_expense()
            elif choice == "2":
                self.expense_manager.add_recurring_expense()
            elif choice == "3":
                self.expense_manager.view_all_expenses()
            elif choice == "4":
                self.expense_manager.view_by_category()
            elif choice == "5":
                self.expense_manager.view_recurring_expenses()
            elif choice == "6":
                self.expense_manager.process_recurring_expenses()
            elif choice == "7":
                self.expense_manager.investment_deposit()
            elif choice == "8":
                self.expense_manager.simulate_expense()
            elif choice == "0":
                break
            else:
                print("Invalid option. Please try again.")
    
    def investment_menu(self):
        while True:
            print("\n" + "="*60)
            print("INVESTMENT MANAGEMENT".center(60))
            print("="*60)
            print("\nℹ️  Use Expense Menu → Investment Deposit to add money")
            print("ℹ️  Use Income Menu → Investment Withdrawal to take money out")
            print("\n[1] View All Investments")
            print("[2] View Investments by Purpose")
            print("[3] View Investment Summary")
            print("[4] Update Investment Value (for gains/losses)")
            print("[0] Back to Main Menu")
            print("\n" + "-"*60)
            
            choice = input("Select an option: ").strip()
            
            if choice == "1":
                self.investment_manager.view_all_investments()
            elif choice == "2":
                self.investment_manager.view_by_purpose()
            elif choice == "3":
                self.investment_manager.view_summary()
            elif choice == "4":
                self.investment_manager.update_investment_value()
            elif choice == "0":
                break
            else:
                print("Invalid option. Please try again.")
    
    def debt_menu(self):
        while True:
            print("\n" + "="*60)
            print("DEBT & OVEREXPENSE MANAGEMENT".center(60))
            print("="*60)
            print("\n[1] Record Overexpense/Debt")
            print("[2] Record Repayment")
            print("[3] Set Monthly Repayment Goal")
            print("[4] View Debt Status")
            print("[5] View Repayment History")
            print("[0] Back to Main Menu")
            print("\n" + "-"*60)
            
            choice = input("Select an option: ").strip()
            
            if choice == "1":
                self.debt_manager.add_debt()
            elif choice == "2":
                self.debt_manager.add_repayment()
            elif choice == "3":
                self.debt_manager.set_monthly_goal()
            elif choice == "4":
                self.debt_manager.view_debt_status()
            elif choice == "5":
                self.debt_manager.view_repayment_history()
            elif choice == "0":
                break
            else:
                print("Invalid option. Please try again.")
    
    def goals_menu(self):
        while True:
            print("\n" + "="*60)
            print("SAVINGS GOALS".center(60))
            print("="*60)
            print("\n[1] Create New Goal")
            print("[2] Contribute to Goal")
            print("[3] View All Goals")
            print("[4] Edit Goal Monthly Target")
            print("[5] View Contribution History")
            print("[0] Back to Main Menu")
            print("\n" + "-"*60)
            
            choice = input("Select an option: ").strip()
            
            if choice == "1":
                self.goals_manager.create_goal()
            elif choice == "2":
                self.goals_manager.add_contribution()
            elif choice == "3":
                self.goals_manager.view_all_goals()
            elif choice == "4":
                self.goals_manager.edit_goal()
            elif choice == "5":
                self.goals_manager.view_contribution_history()
            elif choice == "0":
                break
            else:
                print("Invalid option. Please try again.")
    
    def settings_menu(self):
        while True:
            print("\n" + "="*60)
            print("SETTINGS & GOALS".center(60))
            print("="*60)
            print("\n[1] Set Savings Goal (%)")
            print("[2] View Current Savings Goal")
            print("[0] Back to Main Menu")
            print("\n" + "-"*60)
            
            choice = input("Select an option: ").strip()
            
            if choice == "1":
                try:
                    goal = float(input("Enter your savings goal (% of income): ").strip())
                    if 0 <= goal <= 100:
                        self.data_manager.set_savings_goal(goal)
                        print(f"Savings goal set to {goal}%")
                    else:
                        print("Please enter a percentage between 0 and 100.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            elif choice == "2":
                goal = self.data_manager.get_savings_goal()
                print(f"\nCurrent savings goal: {goal}%")
            elif choice == "0":
                break
            else:
                print("Invalid option. Please try again.")
    
    def run(self):
        print("\nWelcome to your Personal Finance Assistant!")
        
        while True:
            self.display_main_menu()
            choice = input("Select an option: ").strip()
            
            if choice == "1":
                self.income_menu()
            elif choice == "2":
                self.expense_menu()
            elif choice == "3":
                self.investment_menu()
            elif choice == "4":
                self.debt_menu()
            elif choice == "5":
                self.goals_menu()
            elif choice == "6":
                self.dashboard.show_dashboard()
            elif choice == "7":
                self.settings_menu()
            elif choice == "0":
                print("\nThank you for using Personal Finance Assistant!")
                print("All data has been saved automatically.")
                break
            else:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    app = PersonalFinanceApp()
    app.run()
