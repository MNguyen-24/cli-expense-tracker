import json

# Reading text file function
def read_text_file():
    
    # Defining Expenses object
    expenses = {
        "balance": 0,
        "expense_count": 0,
        "expenses": []
    }

    try:
        # Open the file and loop through each line
        with open('expenses.txt', 'r') as expenses_file:
            for line in expenses_file:

                expense_line = line.strip() # Removes the newline character \n

                # Use the comma delimiter to get the category and amount
                current_expense = expense_line.split(',')
                category = current_expense[0]
                amount = current_expense[1]

                # Append the current line/expense and update the total balance and total transactions
                expenses["expense_count"] += 1
                expenses["balance"] += float(amount)
                expenses["expenses"].append({ "category": category, "amount": amount })
    
    # If File is not found, set expenses to default data amounts and return
    except FileNotFoundError:
        expenses = {
            "balance": 0,
            "expense_count": 0,
            "expenses": []
        }
    except ValueError:
        expenses = {
            "balance": 0,
            "expense_count": 0,
            "expenses": []
        }
    
    return expenses # Return the expenses dictionary


# Normalize the expenses dictionary into a list of expenses grouped by category (list of dictionaries)
def normalize_expense_categories(expenses_data):

    # Initialize variables for operation
    expenses_by_category = []
    grouped_expenses = {}

    # Loop through every expense
    for expense in list(expenses_data["expenses"]):
        # Get the category and amount
        category = expense["category"]
        amount = expense["amount"]

        # For every category, add the category and amount and amount
        if category in grouped_expenses:
            grouped_expenses[category] += amount
        else:
            grouped_expenses[category] = amount
    
    # Normalize the dictionary into a list
    for key, value in grouped_expenses.items():
        expenses_by_category.append({'category': key, 'amount': value})

    return expenses_by_category # Return the normalized list of expenses grouped by category

# Displaying Normalized List of Grouped by Category Expenses into a nice format
def display_normalized_expenses_grouped_by_category(normalized_expenses_list, total_balance):
    print(f"Total balance: {total_balance}")
    print("Here are the Expenses grouped by category:\n")
    for expense in normalized_expenses_list:
        print(f"Category: {expense['category']} --- Amount: {expense['amount']}")
    print()

# Displaying Normalized List of Expenses into a nice format (Individually)
def display_expenses_individually(transactions):
    print("Here are all the Individual Expense Transactions:\n")
    index = 1
    for expense in transactions:
        print(f"Transaction ID: {index} - Category: {expense['category']} --- Amount: {expense['amount']}")
        index += 1
    print()

# Displaying Formatted Expenses Wrapper method that runs both display functions for normalized expense data and individual transactions
def display_formatted_expenses(normalized_expenses_list, total_balance, transactions):
    if total_balance <= 0:
        print("\nNO EXPENSES TO DISPLAY!\n")
    else:
        display_normalized_expenses_grouped_by_category(normalized_expenses_list, total_balance)
        display_expenses_individually(transactions)

# Checkes if number is a valid decimal value and greater than 0
def is_valid_float(input_string):
  try:
    number = float(input_string) # If this fails, it means the value is not a decimal value, so it will trigger a ValueError
    if number <= 0: # If the value is negative, or 0, return False. This is invalid input.
        print(f"{input_string} is a valid decimal value, but it is less than 0. Please try again!")
        return False

  except ValueError: # If there is a ValueError, the input is invalid, so return False
    print(input_string + " is not a valid decimal value!")
    return False
  
  return True # If all above works out, then the input is a valid decimal value

# Checkes if number is a valid Integer and greater than or equal to 1
def is_valid_integer(input_string):
    try:
        number = int(input_string) # If this fails, it means the value is not a Integer, so it will trigger a ValueError
        if number < 1: # If the value less than 1, return False. This is invalid input.
            print(f"{input_string} is a valid decimal value, but it is less than 0. Please try again!")
            return False

    except ValueError: # If there is a ValueError, the input is invalid, so return False
        print(input_string + " is not a valid decimal value!")
        return False
    
    return True # If all above works out, then the input is a valid Integer

# We prompt the use for the category name and return the input
def prompt_user_for_transaction_category():
    category_input = input("What would you like to name the new category? ")
    return category_input

# We prompt the user for the transaction amount
def prompt_user_for_transaction_amount():
    transaction_amount = 0 # We set the initial amoun to 0 to avoid errors
    transaction_amount_input = input("How much was this expense (please enter a positive number. Decimals are allowed)? ")
    # We validate if the input is valid
    if(is_valid_float(transaction_amount_input)):
        # We convert the input to a float
        transaction_amount = float(transaction_amount_input)
    else:
        # if the input is invalid, we try again
        return prompt_user_for_transaction_amount()
    return transaction_amount # We return the transaction amount
        
# We prompt the user for the expense category and amount (wrapper method)
def prompt_user_for_expense():
    category = prompt_user_for_transaction_category()
    amount = prompt_user_for_transaction_amount()
    return (category, amount) # We return the category and amount as a tuple

# We prompt the user if they'd like to create, update, display expenses, or exit the program
def prompt_user_for_create_update_show_exit_choice_and_validate():
    acceptable_inputs = ['a', 'b', 'c', 'd'] # List of acceptable inputs
    # We ask the user for their choice as 1 letter
    user_choice = input("What would you like to do? (Please type the letter of your choice)\nA. Add Expense\nB. Update Expense\nC. Display Current Expenses\nD. Exit Program\n")
    
    # If the input is more than 1 letter, try again
    if len(user_choice) > 1:
        print("Invalid choice. Please try again!")
        return prompt_user_for_create_update_show_exit_choice_and_validate()
    
    # If the choice is not an acceptable input, try again
    if user_choice.lower() not in acceptable_inputs:
        print("Invalid choice. Please try again!")
        return prompt_user_for_create_update_show_exit_choice_and_validate()
    return user_choice.lower() # Return the user choice

# We prompt the user for the transaction id they'd like to update
def prompt_user_for_transaction_id(expense_count):
    transaction_id = 0
    transaction_id_input = input("What is the Transaction ID for the transaction you want to update? (Minimum value is 1)?")
    if(is_valid_integer(transaction_id_input)): # Check if transaction id is valid
        transaction_id = int(transaction_id_input)
        if expense_count <= transaction_id or transaction_id < 1: # Check if the transaction ID meets the index bounds
            print("ID cannot be greater than the total number of expenses or less than 1. Try again.")
            return prompt_user_for_transaction_id(expense_count)

    else:
        return prompt_user_for_transaction_id(expense_count)
    
    # If any validations fail, try again
    return transaction_id # Return transaction ID
   


# Add expense function, updates the current expenses and writes them to a file
def add_expense(expenses, category, amount):
    current_expenses = expenses

    # Adding to the current Expenses, updating values
    current_expenses['expenses'].append({"category": category, "amount": amount})
    current_expenses['balance'] += amount
    current_expenses['expense_count'] += 1

    write_current_dictionary_to_text_file(current_expenses['expenses']) # Writing to file

    print("Added expense to file...")

# Update expense function, updates an expense and writes updated expenses to a file
def update_expense(expenses, category, transaction_id, updated_amount):
    current_expenses = expenses

    # Updating values
    current_expenses['expenses'][transaction_id - 1] = {"category": category, "amount": updated_amount}
    current_expenses['balance'] = current_expenses['balance'] - current_expenses['expenses'][transaction_id - 1]['amount'] + updated_amount


    write_current_dictionary_to_text_file(current_expenses['expenses']) # Write to file

    print("Added expense to file...")

# Write to file method
def write_current_dictionary_to_text_file(expenses):
    print("Writing updated data to text file...")

    try:
        # Open file and write every line in expenses to the text file with , as the delimiter
        with open("expenses.txt", "w") as expenses_file_output:
            for expense in expenses:
                current_expense_string = str(expense['category']) + "," + str(expense['amount']) + "\n"
                expenses_file_output.write(current_expense_string)

    except IOError as e:
        print(f"Failed to write to file: {e}")
        return

    print("Finished writing updated data to text file...")

# Read and normalize data wrapper method. returns the expenses dictionary and expenses grouped by category list
def read_and_normalize_data():
    expenses = read_text_file()
    expenses_by_category = normalize_expense_categories(expenses) # Normalize Expenses (grouped by category)
    return (expenses, expenses_by_category)





# Main method
def main():

    # Running status flag is true at first
    running_status = True
    (expenses, expenses_by_category) = read_and_normalize_data() # get current data from file

    # Infinite loop based on running status flag
    while(running_status):
        user_operation = prompt_user_for_create_update_show_exit_choice_and_validate() # Ask user for their choice of operation
        
        if user_operation == 'a': # Adding expense
            (category, amount) = prompt_user_for_expense()
            add_expense(expenses, category, amount)
            
        elif user_operation == 'b': # Updating existing expense
            transaction_id = prompt_user_for_transaction_id(expenses['expense_count'])
            (category, updated_amount) = prompt_user_for_expense()
            update_expense(expenses, category, transaction_id, updated_amount)

        elif user_operation == 'c': # Displaying Expenses
            display_formatted_expenses(expenses_by_category, expenses['balance'], expenses['expenses']) # Display Formatted Expenses

        elif user_operation == 'd': # Exiting program. Setting Running status flag to false
            running_status = False

        # Updating data
        (expenses, expenses_by_category) = read_and_normalize_data()

        # Exiting program
        if running_status == False:
            print("Exiting Program...")
            break

    return 0


main()