import uuid
import datetime
import json


class Task:
    def __init__(self, title, description, due_date, priority, estimated_time, category=None):
        self.task_id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.estimated_time = estimated_time
        self.category = category
        self.status = "Pending"
        self.labels = []
        self.recurring_pattern = None
        self.history_log = []
        self.progress = 0  # For tracking progress
        self.parent_goal = None
        self.assigned_to = None

    def add_label(self, label):
        self.labels.append(label)

    def update_status(self, status):
        self.status = status
        self.history_log.append({"status": status, "timestamp": datetime.datetime.now()})

    def update_progress(self, progress):
        self.progress = progress


class Goal:
    def __init__(self, title, description):
        self.goal_id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.linked_tasks = []

    def link_task(self, task):
        self.linked_tasks.append(task)
        task.parent_goal = self.title


class User:
    def __init__(self, username):
        self.user_id = str(uuid.uuid4())
        self.username = username
        self.tasks = []
        self.goals = []
        self.preferences = {"notifications": True, "calendar_sync": False}
        self.history = []
        self.productivity_data = {"completed": 0, "missed_deadlines": 0}

    def create_task(self, title, description, due_date, priority, estimated_time, category=None):
        task = Task(title, description, due_date, priority, estimated_time, category)
        self.tasks.append(task)
        return task

    def create_goal(self, title, description):
        goal = Goal(title, description)
        self.goals.append(goal)
        return goal

    def assign_task(self, task_id, user):
        task = self.get_task(task_id)
        if task:
            task.assigned_to = user.username
            user.tasks.append(task)

    def track_progress(self, task_id, progress):
        task = self.get_task(task_id)
        if task:
            task.update_progress(progress)

    def get_task(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def filter_tasks(self, filter_by, value):
        if filter_by == "priority":
            return [task for task in self.tasks if task.priority == value]
        elif filter_by == "due_date":
            return [task for task in self.tasks if task.due_date <= value]
        elif filter_by == "category":
            return [task for task in self.tasks if task.category == value]
        return []

    def sync_calendar(self):
        if self.preferences["calendar_sync"]:
            return "Syncing tasks with the external calendar."
        return "Calendar sync disabled."

    def archive_task(self, task_id):
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self.history.append(task)

    def export_tasks(self, file_format="csv"):
        if file_format == "csv":
            file_content = "Title,Description,Due Date,Priority,Status,Progress\n"
            for task in self.tasks:
                file_content += f"{task.title},{task.description},{task.due_date},{task.priority},{task.status},{task.progress}\n"
            with open(f"{self.username}_tasks.csv", "w") as file:
                file.write(file_content)
            return "Exported to CSV."
        elif file_format == "json":
            with open(f"{self.username}_tasks.json", "w") as file:
                json.dump([task.__dict__ for task in self.tasks], file)
            return "Exported to JSON."


class TaskManagementSystem:
    def __init__(self):
        self.users = {}

    def register_user(self, username):
        user = User(username)
        self.users[user.user_id] = user
        return user

    def login(self, user_id):
        return self.users.get(user_id)

    def ai_suggestions(self, user_id):
        # Placeholder for AI-powered recommendations
        user = self.users.get(user_id)
        if user:
            return "AI suggests prioritizing tasks nearing deadlines."
        return None

    def productivity_dashboard(self, user_id):
        user = self.users.get(user_id)
        if user:
            return {
                "tasks_completed": user.productivity_data["completed"],
                "missed_deadlines": user.productivity_data["missed_deadlines"],
                "active_tasks": len(user.tasks)
            }

    def break_down_task(self, task_id, user_id):
        user = self.users.get(user_id)
        task = user.get_task(task_id)
        if task:
            sub_tasks = [
                Task(f"{task.title} - Part {i+1}", task.description, task.due_date, task.priority, task.estimated_time // 3)
                for i in range(3)
            ]
            user.tasks.extend(sub_tasks)
            return sub_tasks


# Example Usage
if __name__ == "__main__":
    tms = TaskManagementSystem()

    # Register users
    john = tms.register_user("JohnDoe")
    jane = tms.register_user("JaneDoe")

    # Create tasks
    task1 = john.create_task("Prepare Report", "Annual report", datetime.datetime(2024, 12, 1), "High", 5)
    task2 = john.create_task("Client Call", "Discuss project updates", datetime.datetime(2024, 11, 25), "Medium", 2)

    # Create goals and link tasks
    goal = john.create_goal("Complete Q4 Objectives", "Achieve all Q4 deliverables.")
    goal.link_task(task1)

    # Assign task to Jane
    john.assign_task(task2.task_id, jane)

    # Track progress
    john.track_progress(task1.task_id, 50)

    # Export tasks
    print(john.export_tasks("csv"))

    # View productivity dashboard
    print(tms.productivity_dashboard(john.user_id))
