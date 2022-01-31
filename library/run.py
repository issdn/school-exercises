from new_client import Client
from database import Database

db = Database()
# print(db.fetch_all_tables())
client = Client(database=db)
