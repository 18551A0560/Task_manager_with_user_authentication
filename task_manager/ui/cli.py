from rich.console import Console
from rich.table import Table
from auth.auth_manager import AuthManager
from tasks.task_manager import TaskManager

console = Console()

class CLI:
  def __init__(self):
    self.auth_manager = AuthManager()
    self.task_manager = TaskManager()
    self.current_user = None

  def display_menu(self):
        console.print("\n[bold blue]Task Manager Menu[/bold blue]")
        console.print("1. Register")
        console.print("2. Login")
        console.print("3. Add Task")
        console.print("4. List Tasks")
        console.print("5. Mark task as complete")
        console.print("6. Delete task")
        console.print("7. Logout")
        console.print("8. Exit")

  def run(self):
        while True:
          self.display_menu()
          choice = console.input("Enter your choice: ")

          if choice == '1':
            self.register_user()
          elif choice == '2':
            self.login_user()
          elif choice == '3':
            self.add_task()
          elif choice == '4':
            self.list_tasks()
          elif choice == '5':
            self.mark_task_complete()
          elif choice == '6':
            self.delete_task()
          elif choice == '7':
            self.logout_user()
          elif choice == '8':
             console.print("Exiting....")
             break
          else:
            console.print("Invalid choice. Please try again.")
  
  def register_user(self):
       username = console.input("Enter a username: ")
       password = console.input("Enter a password: ")

       if self.auth_manager.register_user(username,password):
          console.print("[green]User registered successfully[/green]")
       else:
         console.print("[red]Registration Failed, try again[/red]")

  def login_user(self):
        username = console.input("Enter username: ")
        password = console.input("Enter password: ")

        user = self.auth_manager.login_user(username, password)

        if user:
            self.current_user = user
            console.print(f"[green]Welcome {user.username}![/green]")
        else:
            console.print("[red]Login Failed. Incorrect credentials[/red]")

  def add_task(self):
      if not self.current_user:
         console.print("[red]Please login to add tasks[/red]")
         return
      title = console.input("Enter task title: ")
      description = console.input("Enter task description: ")

      self.task_manager.create_task(self.current_user.id, title, description)
      console.print("[green]Task added successfully![/green]")

  def list_tasks(self):
        if not self.current_user:
            console.print("[red]Please login to view your tasks[/red]")
            return
        
        tasks = self.task_manager.list_tasks(self.current_user.id)

        if not tasks:
            console.print("[yellow]No tasks available[/yellow]")
            return
        
        table = Table(title="Your Tasks")
        table.add_column("ID", style="bold blue")
        table.add_column("Title", style="bold cyan")
        table.add_column("Description")
        table.add_column("Status", style="bold green")

        for task in tasks:
            status = "[green]Completed[/green]" if task.completed else "[red]Pending[/red]"
            table.add_row(str(task.id),task.title, task.description or "No Description", status)

        console.print(table)
  
  def mark_task_complete(self):
      if not self.current_user:
         console.print("[red]Please login to add tasks[/red]")
         return
      try:
          task_id = int(console.input("Enter the ID of the task to mark as complete: "))
      except ValueError:
          console.print("[red]Invalid task ID. Please enter a number.[/red]")
          return
      
      task = self.task_manager.get_task_by_id(task_id)

      if not task:
        console.print("[red]Task not found[/red]")
        return
      
      if task.user_id != self.current_user.id:
         console.print("[red]You can not mark other users tasks[/red]")
         return
      
      self.task_manager.mark_task_as_complete(task_id)
      console.print("[green]Task marked as completed[/green]")

  def delete_task(self):
        if not self.current_user:
            console.print("[red]Please login to delete tasks[/red]")
            return
        
        try:
           task_id = int(console.input("Enter the id of the task to delete: "))
        except ValueError:
            console.print("[red]Invalid Task ID. Please enter a number[/red]")
            return
        
        task = self.task_manager.get_task_by_id(task_id)
        if not task:
            console.print("[red]Task not found.[/red]")
            return
        
        if task.user_id != self.current_user.id:
            console.print("[red]You can not delete other users tasks.[/red]")
            return
        
        self.task_manager.delete_task(task_id)
        console.print("[green]Task deleted[/green]")
  
  def logout_user(self):
      if self.current_user:
         self.current_user = None
         console.print("[yellow]Logged out successfully[/yellow]")
      else:
        console.print("[yellow]No user logged in[/yellow]")