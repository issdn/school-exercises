from bibliothek_types import *
from config import Config


class DictManipulator:
    def normalize(entries: RowT, remove_defaults: bool = True) -> RowT:
        """Removes items listed in config in disabled_columns or default_columns from the row (dictionary)."""
        entries = DictManipulator.first_value(entries)
        to_delete = []
        for k, v in entries.items():
            if k in Config.disabled_columns:
                to_delete.append(k)
            if remove_defaults:
                if k in Config.default_columns and len(str(v)) != 0:
                    to_delete.append(k)
        for i in to_delete:
            del entries[i]
        return entries

    def normalize_list(lst: list, remove_defaults: bool = True) -> list:
        """Removes items listed in config in disabled_columns or default_columns from a list."""
        to_delete = []
        for i in lst:
            if i in Config.disabled_columns:
                to_delete.append(i)
            if remove_defaults:
                if i in Config.default_columns:
                    to_delete.append(i)
        for i in to_delete:
            lst.remove(i)
        return lst

    def entries(d: dict | RowT | RowT) -> RowT:
        return next(iter(d.values()))

    def first_key(self, d: dict | RowT | RowT) -> str:
        return next(iter(d))

    def first_value(self, d: dict | RowT | RowT) -> dict | RowT | ValueT:
        return next(iter(d.values()))

    def all_values(self, d: dict | RowT) -> ValueT:
        return list(d.values())
