import sys
import os
from rich.console import Console
from rich.table import Table

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from views.employees_view import create_user_view, login_view

def main():
    """
    Display the Login menu of the application.
    """
    console = Console()

    while True:
        table = Table(show_header=True, header_style="bold green")

        table.add_column("Welcome to the Epic Events app, please select an option:", justify="left", style="cyan", no_wrap=True)
       
        table.add_row("1. Create an user")
        table.add_row("2. Login")
        table.add_row("3. Exit the app")

        console.print(table)

        choice = input("Enter your choice: ")

        if choice == '1':
            create_user_view()
        elif choice == '2':
            login_view()
        elif choice == '3':
            console.print("Exiting the app... Goodbye! :smiley:", style="red")
            quit()
        else:
            console.print("\nInvalid choice, try again\n", style="bold red")
