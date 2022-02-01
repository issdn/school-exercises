from client import Client
from database import Database

db = Database()
# db.add_schema()
client = Client(database=db)
