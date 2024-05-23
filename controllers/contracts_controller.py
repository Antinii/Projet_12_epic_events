# from models.contracts import Contract
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import create_engine
# from texttable import Texttable

# engine = create_engine('sqlite:///db.sqlite3')
# Session = sessionmaker(bind=engine)
# session = Session()

# def get_contracts():
#     """
#     Show all contracts in a nice table format.
#     """
#     contracts = session.query(Contract).all()

#     if not contracts:
#         print("No contracts found.")
#         return

#     table = Texttable()
#     table.header(["ID", "Total Price", "Pending Amount", "Created Date", "Is Signed"])
#     for contract in contracts:
#         table.add_row([contract.id, contract.total_price, contract.pending_amount, contract.created_date,
#                        contract.is_signed])
    
#     print(table.draw())