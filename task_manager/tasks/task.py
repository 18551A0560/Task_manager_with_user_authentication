class Task:
    def __init__(self, id, user_id, title, description, completed):
       self.id = id
       self.user_id = user_id
       self.title = title
       self.description = description
       self.completed = completed

    def __repr__(self):
       return f"<Task id={self.id}, title={self.title}, completed={self.completed}>"