import sys
from client import Client
from database import Database


def main() -> None:
    args = sys.argv[1:]
    if "-r" in args or "--Reset" in args:
        Database.reset_database()
    Client()


if __name__ == "__main__":
    main()
