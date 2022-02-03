from client import Client
from database import Database

db = Database()
# db.add_schema()
# db.fetch_table("books")
print(db.search_table("books", "6"))
client = Client(database=db)
