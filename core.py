import logging
import os
import json
import traceback

from filelock import FileLock


class DBManager:
    def __init__(self, db_file_path):
        self.db_file_path = db_file_path
        self.database = self.load_db()

    def load_db(self):
        if os.path.exists(self.db_file_path):
            with open(self.db_file_path, 'r') as db_file:
                return json.load(db_file)
        return {}

    def save_db(self):
        with open(self.db_file_path, 'w') as db_file:
            json.dump(self.database, db_file)

    def get(self, key):
        return self.database.get(key, [])

    def set(self, key, value):
        if key not in self.database:
            self.database[key] = []
        if value not in self.database[key]:
            self.database[key].append(value)
            self.save_db()
            return True
        return False

    def remove_value(self, key, value):
        if key in self.database and value in self.database[key]:
            self.database[key].remove(value)
            if not self.database[key]:
                del self.database[key]  # Remove key if no values remain
            self.save_db()
            return True
        return False

    def remove(self, key):
        if key in self.database:
            del self.database[key]
            self.save_db()
            return True
        return False

    def keys(self):
        return self.database.keys()

    def values(self):
        return self.database.values()

    def items(self):
        return self.database.items()

    def dumps(self):
        return json.dumps(self.database)

    def truncate_db(self):
        self.database.clear()
        self.save_db()
        return True
