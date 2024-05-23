from texttable import Texttable
from controllers.customers_controller import get_customers


def manage_customers_menu():
    while True:
        table = Texttable()
        table.header(["Customers menu, please select an option"])
        table.add_row(["1. Create a new customer"])
        table.add_row(["2. Show all the customers"])
        table.add_row(["3. Update a customer"])
        table.add_row(["4. Go back"])
        print(table.draw())

        choice = input("Enter your choice: ")

        if choice == '1':
            pass
        elif choice == '2':
            get_customers()
        elif choice == '3':
            pass
        elif choice == '4':
            break
        else:
            print("Invalid choice")