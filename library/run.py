from client import Client
from database import Database

# Database.reset_database()
db = Database()
client = Client(database=db)
