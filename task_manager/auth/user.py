class User:
    def __init__(self, id, username, password=None):
        self.id = id
        self.username = username
        self.password = password  # we'll store hashed passwords

    def __repr__(self):
        return f"<User id={self.id}, username={self.username}>"