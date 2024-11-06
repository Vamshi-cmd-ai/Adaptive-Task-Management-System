import datetime
import heapq
import uuid

# Task class represents individual tasks
class Task:
    def __init__(self, title, description, due_date, priority):
        self.id = str(uuid.uuid4())  # Unique identifier for each task
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority  # Priority (1 is highest, larger numbers are lower priority)
        self.completed = False

    def __lt__(self, other):
        return self.priority < other.priority

    def mark_complete(self):
        self.completed = True

    def __str__(self):
        return f"[{self.priority}] {self.title} - Due: {self.due_date} | Status: {'Completed' if self.completed else 'Pending'}"

# TaskManager class to handle task creation, updating, and prioritization
class TaskManager:
    def __init__(self):
        self.tasks = []  # Priority queue for tasks (min-heap)

    def add_task(self, title, description, due_date, priority):
        task = Task(title, description, due_date, priority)
        heapq.heappush(self.tasks, task)
        print(f"Task '{title}' added successfully!")

    def view_tasks(self):
        if not self.tasks:
            print("No tasks available.")
            return
        print("Current Tasks:")
        for task in self.tasks:
            print(task)

    def complete_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.mark_complete()
                print(f"Task '{task.title}' marked as completed!")
                return
        print("Task not found.")

    def get_next_task(self):
        while self.tasks:
            next_task = heapq.heappop(self.tasks)
            if not next_task.completed:
                print("Next task based on priority:")
                print(next_task)
                return
        print("No pending tasks available.")

    def reschedule_task(self, task_id, new_due_date):
        for task in self.tasks:
            if task.id == task_id:
                task.due_date = new_due_date
                print(f"Task '{task.title}' rescheduled to {new_due_date}.")
                return
        print("Task not found.")

    def delete_task(self, task_id):
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                print(f"Task '{task.title}' deleted.")
                return
        print("Task not found.")

# Main function to interact with the user
def main():
    task_manager = TaskManager()

    while True:
        print("\n1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Get Next Task")
        print("5. Reschedule Task")
        print("6. Delete Task")
        print("7. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            title = input("Enter task title: ")
            description = input("Enter task description: ")
            due_date = input("Enter task due date (YYYY-MM-DD): ")
            priority = int(input("Enter task priority (1 for high, 10 for low): "))
            task_manager.add_task(title, description, due_date, priority)

        elif choice == "2":
            task_manager.view_tasks()

        elif choice == "3":
            task_id = input("Enter task ID to mark as complete: ")
            task_manager.complete_task(task_id)

        elif choice == "4":
            task_manager.get_next_task()

        elif choice == "5":
            task_id = input("Enter task ID to reschedule: ")
            new_due_date = input("Enter new due date (YYYY-MM-DD): ")
            task_manager.reschedule_task(task_id, new_due_date)

        elif choice == "6":
            task_id = input("Enter task ID to delete: ")
            task_manager.delete_task(task_id)

        elif choice == "7":
            print("Exiting Task Manager. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
