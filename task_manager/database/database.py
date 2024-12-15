import sqlite3

class DatabaseManager:
    def __init__(self, db_name='task_manager.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
           self.conn = sqlite3.connect(self.db_name)
           self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
           print(f"Database connection error: {e}")

    def close(self):
        if self.conn:
            self.conn.close()

    def execute(self, query, params=()):
        try:
          self.connect()
          self.cursor.execute(query, params)
          self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database execute error: {e}")
        finally:
            self.close()

    def fetchone(self, query, params=()):
        try:
            self.connect()
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Database fetchone error: {e}")
        finally:
            self.close()
    
    def fetchall(self, query, params=()):
        try:
           self.connect()
           self.cursor.execute(query,params)
           return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database fetchall error: {e}")
        finally:
            self.close()


    def initialize_database(self):
      self.execute("""
      CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE NOT NULL,
      password TEXT NOT NULL
      )
      """)
      self.execute("""
      CREATE TABLE IF NOT EXISTS tasks(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          user_id INTEGER NOT NULL,
          title TEXT NOT NULL,
          description TEXT,
          completed BOOLEAN DEFAULT FALSE,
          FOREIGN KEY (user_id) REFERENCES users(id)
      )
      """)

if __name__ == '__main__':
    db_manager = DatabaseManager()
    db_manager.initialize_database()
    print("Database initialized")