from client import Client
from database import Database
import tkinter as tk

database = Database('library')

gui = Client(database=database)
# x = ['1', '2022-01-22', 'MDA']
# print(", ".join(x))

# q = []
# nr_q = 5
# [q.append("?") for nr in range(nr_q)]
# print(", ".join(q))
    