import csv

def get_user_name():
    name = input("Welcome to the Expense Prediction Software!\nPlease input your name: ")
    return name

def input_expenses(categories):
    expenses = {}
    for category in categories:
        print(f"\nCategory: {category}")
        expenses[category] = []
        for i in range(6):
            expense_input = input(f"Please input expenses for month {i + 1} in MVR (comma-separated): ")
            expense_list = [float(amount.strip()) for amount in expense_input.split(',')]
            expenses[category].extend(expense_list)
    return expenses

def predict_next_month_expenses(expenses, categories):
    predictions = {}
    for category in categories:
        expense_data = expenses[category]  # Get data for the last three months
        prediction = sum(expense_data) / len(expense_data)  # Simple moving average
        predictions[category] = prediction
    return predictions

def calculate_savings_recommendations(predictions):
    savings_goal = float(input("Please enter your savings goal for next month in MVR: "))
    recommendations = {}
    potential_savings = 0

    for category, prediction in predictions.items():
        difference = prediction - (savings_goal / len(predictions))
        if difference > 0:
            percentage_reduction = (difference / prediction) * 100
            recommendations[category] = f"Consider reducing your {category} expense by {percentage_reduction:.2f}%"
            potential_savings += difference

    return recommendations, potential_savings

def main():
    name = get_user_name()
    print(f"\nHello, {name}! Let’s predict your expenses for the next month.")
    
    categories = ["Coffees", "Outside Food", "Education", "Utilities", "Groceries", "Phone and Internet", "Subscriptions", "Petrol", "Maintenance and Repairs"]
    expenses = input_expenses(categories)
    
    while True:
        print("\n>> Please select an option:")
        print("1. Enter Expense Data")
        print("2. Predict Next Month’s Expenses")
        print("3. Savings Plan for Next Month")
        print("4. Exit")
        
        choice = input(">> Enter your choice: ")
        
        if choice == '1':
            print("\n>> You’ve selected 'Enter Expense Data'")
            category = input("Description of Expense: ")
            print("Category Options:")
            for i, cat in enumerate(categories, start=1):
                print(f"\t[{i}] {cat}")
            category_choice = int(input("Choose a Category (1/2/3/...): "))
            if 1 <= category_choice <= len(categories):
                category = categories[category_choice - 1]
                amount = float(input("Amount (in MVR): "))
                date = input("Date (dd/mm/yyyy): ")
                expenses.setdefault(category, []).append(amount)
                print("\n>> Expense Saved Successfully!\n")
            else:
                print("Invalid category choice.")
        elif choice == '2':
            print("\n>> You’ve selected 'Predict Next Month’s Expenses'")
            predictions = predict_next_month_expenses(expenses, categories)
            print("\nCalculating predictions based on past months...\n")
            print("Predictions:")
            for category, prediction in predictions.items():
                print(f"\t{category}: MVR {prediction:.2f}")
            show_formula = input("\nDo you want to see the prediction formula used? (Yes/No): ").strip().lower()
            if show_formula == 'yes':
                print("\n-Simple Moving Average Calculation:")
                for category in categories:
                    expense_data = expenses[category]
                    moving_average = sum(expense_data) / len(expense_data)
                    print(f" ({category}_Month1 + {category}_Month2 + {category}_Month3) + {category}_Month4 + {category}_Month5 + {category}_Month6 = MVR {moving_average:.2f}")
                print()
        elif choice == '3':
            print("\n>> You’ve selected 'Savings Plan for Next Month'")
            recommendations, potential_savings = calculate_savings_recommendations(predictions)
            savings_goal = float(input("Please enter your savings goal for next month in MVR: "))
            print("\nRecommendations:")
            for category, recommendation in recommendations.items():
                print(f"\t- {recommendation}")
            print(f"\nLimit your spendings upto: MVR {potential_savings:.2f}\n")
            adjust_savings_goal = input("Adjust your savings goal or follow more recommendations to achieve your desired savings. Press Enter to continue...")
        elif choice == '4':
            print(f">> Thank you for using the Expense Prediction & Savings Planner Software, {name}! Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a valid option (1/2/3/4).")

if __name__ == "__main__":
    main()
