import sqlite3


#class to manage db
class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.begin_transaction()

    def begin_transaction(self):
        try:
            if not self.conn.in_transaction:
                self.cursor.execute("BEGIN")
        except sqlite3.Error as e:
            print(f"Error: {e}")

    def commit_transaction(self):
        try:
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error: {e}")

    def rollback_transaction(self):
        try:
            self.conn.rollback()
        except sqlite3.Error as e:
            print(f"Error: {e}")

    def execute_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return self.cursor
        except sqlite3.Error as e:
            print(f"Database Error: {e}")
            return None

    def close(self):
        self.conn.close()
