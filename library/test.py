from database import Database
import random

Database.initialize()

# row = {"users": {"id": "1", "name": 1, "surname": 2}}
# v = Validator(row=row, require_id=True)
# v.validate()
# print(v.errors)


def a():
    return random.randint(1, 20), random.randint(1, 20)


b = {random.randint(1, 20): "2" for i in range(1, 5)}
# b = dict(b)
print(b)
