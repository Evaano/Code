import csv
import os
import matplotlib.pyplot as plt

# Define a class to represent an expense
class Expense:
    def __init__(self, description, category, amount, date):
        self.description = description
        self.category = category
        self.amount = amount
        self.date = date

# Function to enter expense data
def enter_expense():
    print("You've selected 'Enter Expense Data'")
    
    # Input the expense details
    description = input("\nEnter a description for the expense: ")
    
    print("\nSelect a category:")
    print("1. Coffees")
    print("2. Movies")
    print("3. Dinners")
    
    category_choice = input("Enter the category number: ")
    
    categories = ["Coffees", "Movies", "Dinners"]
    
    try:
        # Convert the category choice to an index in the 'categories' list
        category_index = int(category_choice) - 1
        selected_category = categories[category_index]
    except (ValueError, IndexError):
        print("Invalid category choice. Expense not recorded.")
        return
    
    amount = float(input("Enter the expense amount: "))
    date = input("Enter the expense date (e.g., YYYY-MM-DD): ")
    
    # Create an Expense object with the entered data
    expense = Expense(description, selected_category, amount, date)
    
    # Check if the CSV file exists, and create it if it doesn't
    csv_file_exists = os.path.isfile('expenses.csv')
    
    # Append the expense to the CSV file
    with open('expenses.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        
        # Write header row if the file was just created
        if not csv_file_exists:
            writer.writerow(["Description", "Category", "Amount", "Date"])
        
        writer.writerow([expense.description, expense.category, expense.amount, expense.date])

    # You can now store this expense object or process it as needed
    print(f"Expense recorded: {expense.description}, {expense.category}, MVR {expense.amount}, Date: {expense.date}")

# Function to read expenses from a CSV file and return them as a list of Expense objects
def read_expenses_from_csv():
    expenses = []
    try:
        with open('expenses.csv', mode='r') as file:
            reader = csv.reader(file)
            header_skipped = False  # Flag to skip the header row
            for row in reader:
                if not header_skipped:
                    header_skipped = True
                    continue  # Skip the header row
                description, category, amount, date = row
                expenses.append(Expense(description, category, float(amount), date))
    except FileNotFoundError:
        pass  # If the file doesn't exist, return an empty list
    return expenses

# Function to predict next month's expenses based on past data
def predict_next_month_expenses(expenses, categories):
    predictions = {}
    for category in categories:
        # Extract the amounts of expenses for the selected category
        expense_data = [expense.amount for expense in expenses if expense.category == category]
        
        # Use a simple moving average for prediction
        if len(expense_data) >= 3:
            prediction = sum(expense_data[-3:]) / 3
        else:
            prediction = sum(expense_data) / len(expense_data) if len(expense_data) > 0 else 0
        
        predictions[category] = prediction
    
    return predictions

# Function to plan savings for the next month
def savings_planner(predictions):
    savings_goal = float(input("Please enter your savings goal for next month: MVR "))
    recommendations = {}
    total_predicted_expenses = sum(predictions.values())
    
    if total_predicted_expenses <= savings_goal:
        print("Congratulations! Your predicted expenses are already within your savings goal.")
    else:
        potential_savings = total_predicted_expenses - savings_goal
        for category, prediction in predictions.items():
            if prediction > 0:
                # Calculate the percentage by which expenses need to be reduced
                reduction_percentage = (prediction - (savings_goal / len(predictions))) / prediction * 100
                if reduction_percentage > 0:
                    recommendations[category] = f"Consider reducing your {category} expense by {reduction_percentage:.2f}%"
        
        if not recommendations:
            print("You're already on track to meet your savings goal. Keep it up!")
        else:
            print("Recommendations to meet your savings goal:")
            for category, recommendation in recommendations.items():
                print(f"- {category}: {recommendation}")

    return recommendations, potential_savings

# Function to visualize spending trends for a chosen category
def visualize_spending_trend(expenses, category, predictions):
    # Filter expenses for the chosen category
    category_expenses = [expense for expense in expenses if expense.category == category]

    # Extract the amount and date for each expense
    expense_dates = [expense.date for expense in category_expenses[-3:]]
    expense_amounts = [expense.amount for expense in category_expenses[-3:]]

    # Create a list of month labels for the x-axis
    month_labels = ["Month 1", "Month 2", "Month 3"]

    # Add the next month prediction to the data
    next_month_prediction = predictions.get(category, 0)
    expense_dates.append("Prediction")
    expense_amounts.append(next_month_prediction)
    month_labels.append("Prediction")

    # Create a bar chart to visualize the spending trend
    plt.figure(figsize=(8, 6))
    plt.bar(month_labels, expense_amounts, color=['blue', 'green', 'orange', 'red'])
    plt.xlabel("Month")
    plt.ylabel("Expense Amount (MVR)")
    plt.title(f"Spending Trend for {category}")
    plt.show()

# Modify the main function to pass predictions to the visualize_spending_trend function
def main():
    expenses = read_expenses_from_csv()
    categories = ["Coffees", "Movies", "Dinners"]
    predictions = {}

    print('Welcome to the Expense Prediction & Savings Planner Software!')

    while True:
        print('\nPlease select an option:')
        print("1. Enter Expense Data")
        print("2. Predict Next Month's Expenses")
        print("3. Savings Plan for Next Month")
        print("4. Visualize Spending Trend for a Category")
        print("5. Exit")
    
        choice = input('Enter your choice: ')

        if choice == "1":
            enter_expense()
        elif choice == "2":
            predictions = predict_next_month_expenses(expenses, categories)
            print("\nPredicted Expenses for Next Month:")
            for category, prediction in predictions.items():
                print(f"{category}: MVR {prediction:.2f}")
        elif choice == "3":
            if not predictions:
                print("Please predict next month's expenses first (Option 2) before using the savings planner (Option 3).")
            else:
                savings_planner(predictions)
        elif choice == "4":
            category = input("Enter one of the categories (Coffees, Movies, Dinners) to visualize spending trend: ")
            visualize_spending_trend(expenses, category, predictions)
        elif choice == "5":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()