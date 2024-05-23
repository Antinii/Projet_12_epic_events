# from texttable import Texttable
# from controllers.contracts_controller import get_contracts


# def manage_contracts_menu():
#     while True:
#         table = Texttable()
#         table.header(["Contracts menu, please select an option"])
#         table.add_row(["1. Create a new contract"])
#         table.add_row(["2. Show all the contracts"])
#         table.add_row(["3. Update a contract"])
#         table.add_row(["4. Go back"])
#         print(table.draw())

#         choice = input("Enter your choice: ")

#         if choice == '1':
#             pass
#         elif choice == '2':
#             get_contracts()
#         elif choice == '3':
#             pass
#         elif choice == '4':
#             break
#         else:
#             print("Invalid choice")