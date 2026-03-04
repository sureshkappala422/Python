from storage import load_expenses, save_expenses
from tracker import add_expense, list_expenses, show_total, show_category_summary


def show_menu() -> None:
    print("\n==============================")
    print(" Personal Expense Tracker")
    print("==============================")
    print("1) Add Expense")
    print("2) View All Expenses")
    print("3) Total Spending")
    print("4) Category Summary")
    print("5) Save & Exit")
    print("==============================")


def main() -> None:
    expenses = load_expenses()

    while True:
        show_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            add_expense(expenses)

        elif choice == "2":
            list_expenses(expenses)

        elif choice == "3":
            show_total(expenses)

        elif choice == "4":
            show_category_summary(expenses)

        elif choice == "5":
            save_expenses(expenses)
            print("✅ Saved. Bye!")
            break

        else:
            print("❌ Invalid choice. Please select 1-5.")


if __name__ == "__main__":
    main()