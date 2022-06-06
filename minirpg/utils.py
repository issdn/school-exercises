import sys

def is_int(string: str) -> bool:
    try:
        int(string)
        return True
    except ValueError:
        return False

def supports_unicode(text: str="▮▮▮") -> bool:
    try:
        "▮▮▮"
        return True
    except UnicodeEncodeError:
        return False


print(supports_unicode())