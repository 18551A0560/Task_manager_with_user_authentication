from tasks.task import Task
from database.database import DatabaseManager
class TaskManager:

    def __init__(self):
        self.db_manager = DatabaseManager()

    def create_task(self, user_id, title, description):
      query = "INSERT INTO tasks (user_id, title, description) VALUES (?,?,?)"
      self.db_manager.execute(query, (user_id, title, description))

    def get_task_by_id(self, task_id):
        query = "SELECT id, user_id, title, description, completed FROM tasks WHERE id = ?"
        result = self.db_manager.fetchone(query, (task_id,))
        if result:
            id, user_id, title, description, completed = result
            return Task(id,user_id,title,description, completed)
        else:
          return None
    
    def list_tasks(self, user_id):
        query = "SELECT id, user_id, title, description, completed FROM tasks WHERE user_id = ?"
        results = self.db_manager.fetchall(query, (user_id,))
        tasks = []
        for result in results:
            id,user_id, title, description, completed = result
            tasks.append(Task(id, user_id,title,description, completed))
        return tasks
    
    def mark_task_as_complete(self, task_id):
      query = "UPDATE tasks SET completed = True WHERE id = ?"
      self.db_manager.execute(query, (task_id,))
    
    def delete_task(self, task_id):
        query = "DELETE FROM tasks WHERE id = ?"
        self.db_manager.execute(query,(task_id,))