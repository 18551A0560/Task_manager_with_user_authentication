import bcrypt
from auth.user import User
from database.database import DatabaseManager
class AuthManager:
    def __init__(self):
       self.db_manager = DatabaseManager()

    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')
    
    def register_user(self, username, password):
        hashed_password = self.hash_password(password)
        query = "INSERT INTO users (username, password) VALUES (?,?)"
        self.db_manager.execute(query, (username, hashed_password))
        return True

    def get_user_by_username(self, username):
       query = "SELECT id, username, password FROM users WHERE username = ?"
       result = self.db_manager.fetchone(query,(username,))
       if result:
         id,username,hashed_password = result
         return User(id,username,hashed_password)
       return None

    def check_password(self, password, hashed_password):
       return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def login_user(self, username, password):
        user = self.get_user_by_username(username)
        if user and self.check_password(password,user.password):
          return user
        else:
          return None