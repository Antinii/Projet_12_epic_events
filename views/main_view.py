import sys
import os
from texttable import Texttable

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from employees_view import create_user_view, login_view

def main():
    """
    Display the Login menu of the application.
    """
    while True:
        table = Texttable()
        table.header(["Welcome to the Epic Events app, please select an option:"])
        table.add_row(["1. Create an user"])
        table.add_row(["2. Login"])
        table.add_row(["3. Exit the app"])
        print(table.draw())

        choice = input("Enter your choice: ")

        if choice == '1':
            create_user_view()
        elif choice == '2':
            login_view()
        elif choice == '3':
            print("Exiting the app... Goodbye !")
            break
        else:
            print("\n Invalid choice, try again \n")


if __name__ == "__main__":
    main()
