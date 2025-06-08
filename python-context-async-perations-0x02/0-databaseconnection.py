import sqlite3

class DatabaseConnection:
    def __init__(self, db_name="users.db"):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn  # This gets assigned to the variable in `with` block

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()

# ✅ Use the context manager to query the users table
if __name__ == "__main__":
    with DatabaseConnection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
