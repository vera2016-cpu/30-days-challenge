import os
import json
from datetime import datetime

class TodoList:
    def __init__(self, filename="todo_list.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self):
        """Load tasks from file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.tasks = json.load(f)
                print(f"📂 Loaded {len(self.tasks)} tasks from {self.filename}")
            except Exception as e:
                print(f"❌ Error loading tasks: {e}")
                print("Starting with empty list.")
                self.tasks = []
        else:
            print("📝 No existing todo list found. Starting fresh!")
            self.tasks = []
    
    def save_tasks(self):
        """Save tasks to file"""
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.tasks, f, indent=2)
            print(f"💾 Tasks saved successfully!")
        except Exception as e:
            print(f"❌ Error saving tasks: {e}")
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("📝 TO-DO LIST MANAGER")
        print("="*50)
        print(f"📊 Total Tasks: {len(self.tasks)} | 📌 Pending: {len([t for t in self.tasks if not t['completed']])}")
        print("="*50)
        print("1. 📋 View all tasks")
        print("2. ➕ Add new task")
        print("3. ✅ Mark task as complete")
        print("4. ❌ Delete task")
        print("5. 🏆 View completed tasks")
        print("6. ⏳ View pending tasks")
        print("7. 🗑️  Clear all tasks")
        print("8. 🔄 Edit task")
        print("9. 🔍 Search tasks")
        print("10.💾 Save and exit")
        print("="*50)
    
    def view_tasks(self, tasks=None, title="ALL TASKS"):
        """Display tasks with formatting"""
        if tasks is None:
            tasks = self.tasks
        
        if not tasks:
            print(f"\n📭 No {title.lower()} to display.")
            return
        
        print(f"\n{'='*60}")
        print(f"📋 {title} ({len(tasks)} tasks)")
        print('='*60)
        
        for i, task in enumerate(tasks, 1):
            status = "✅" if task['completed'] else "⏳"
            priority = task.get('priority', 'Medium')
            priority_symbol = {
                'High': '🔴',
                'Medium': '🟡', 
                'Low': '🟢'
            }.get(priority, '🟡')
            
            print(f"\n{i}. {status} {priority_symbol} {task['title']}")
            print(f"   📅 Created: {task['created_at']}")
            if task.get('due_date'):
                print(f"   ⏰ Due: {task['due_date']}")
            if task.get('description'):
                print(f"   📝 Description: {task['description'][:50]}...")
    
    def add_task(self):
        """Add a new task"""
        print("\n➕ ADD NEW TASK")
        print("-" * 30)
        
        title = input("Task title: ").strip()
        if not title:
            print("❌ Task title cannot be empty!")
            return
        
        description = input("Description (optional): ").strip()
        
        # Priority selection
        print("\nPriority levels:")
        print("1. 🔴 High")
        print("2. 🟡 Medium")
        print("3. 🟢 Low")
        
        priority_choice = input("Select priority (1-3, default 2): ").strip()
        priority_map = {'1': 'High', '2': 'Medium', '3': 'Low'}
        priority = priority_map.get(priority_choice, 'Medium')
        
        # Due date (optional)
        due_date = input("Due date (YYYY-MM-DD, optional): ").strip()
        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                print("❌ Invalid date format. Using None.")
                due_date = None
        
        task = {
            'id': len(self.tasks) + 1,
            'title': title,
            'description': description,
            'priority': priority,
            'completed': False,
            'created_at': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'due_date': due_date,
            'completed_at': None
        }
        
        self.tasks.append(task)
        print(f"\n✅ Task '{title}' added successfully!")
        self.save_tasks()
    
    def mark_complete(self):
        """Mark a task as complete"""
        pending_tasks = [t for t in self.tasks if not t['completed']]
        
        if not pending_tasks:
            print("\n🎉 All tasks are already completed!")
            return
        
        print("\n⏳ PENDING TASKS:")
        for i, task in enumerate(pending_tasks, 1):
            print(f"{i}. {task['title']}")
        
        try:
            choice = int(input(f"\nEnter task number to mark complete (1-{len(pending_tasks)}): "))
            if 1 <= choice <= len(pending_tasks):
                task = pending_tasks[choice - 1]
                task['completed'] = True
                task['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                print(f"\n✅ Task '{task['title']}' marked as complete!")
                self.save_tasks()
            else:
                print("❌ Invalid task number!")
        except ValueError:
            print("❌ Please enter a valid number!")
    
    def delete_task(self):
        """Delete a task"""
        if not self.tasks:
            print("\n📭 No tasks to delete!")
            return
        
        self.view_tasks()
        
        try:
            choice = int(input(f"\nEnter task number to delete (1-{len(self.tasks)}): "))
            if 1 <= choice <= len(self.tasks):
                task = self.tasks.pop(choice - 1)
                # Update IDs
                for i, t in enumerate(self.tasks, 1):
                    t['id'] = i
                print(f"\n🗑️  Task '{task['title']}' deleted successfully!")
                self.save_tasks()
            else:
                print("❌ Invalid task number!")
        except ValueError:
            print("❌ Please enter a valid number!")
    
    def view_completed(self):
        """View completed tasks"""
        completed = [t for t in self.tasks if t['completed']]
        self.view_tasks(completed, "COMPLETED TASKS")
    
    def view_pending(self):
        """View pending tasks"""
        pending = [t for t in self.tasks if not t['completed']]
        self.view_tasks(pending, "PENDING TASKS")
    
    def clear_all(self):
        """Clear all tasks"""
        if not self.tasks:
            print("\n📭 Task list is already empty!")
            return
        
        confirmation = input("\n⚠️  Are you sure you want to delete ALL tasks? (yes/no): ").lower()
        if confirmation == 'yes':
            self.tasks = []
            self.save_tasks()
            print("\n🗑️  All tasks cleared!")
        else:
            print("\n❌ Clear operation cancelled.")
    
    def edit_task(self):
        """Edit an existing task"""
        if not self.tasks:
            print("\n📭 No tasks to edit!")
            return
        
        self.view_tasks()
        
        try:
            choice = int(input(f"\nEnter task number to edit (1-{len(self.tasks)}): "))
            if 1 <= choice <= len(self.tasks):
                task = self.tasks[choice - 1]
                
                print(f"\n✏️  EDITING TASK: {task['title']}")
                print("-" * 40)
                
                new_title = input(f"New title [{task['title']}]: ").strip()
                if new_title:
                    task['title'] = new_title
                
                new_desc = input(f"New description [{task.get('description', '')}]: ").strip()
                task['description'] = new_desc if new_desc else task.get('description', '')
                
                # Priority
                print(f"\nCurrent priority: {task.get('priority', 'Medium')}")
                print("1. 🔴 High")
                print("2. 🟡 Medium") 
                print("3. 🟢 Low")
                new_priority = input("New priority (1-3, press Enter to skip): ").strip()
                if new_priority in ['1', '2', '3']:
                    priority_map = {'1': 'High', '2': 'Medium', '3': 'Low'}
                    task['priority'] = priority_map[new_priority]
                
                print(f"\n✅ Task updated successfully!")
                self.save_tasks()
            else:
                print("❌ Invalid task number!")
        except ValueError:
            print("❌ Please enter a valid number!")
    
    def search_tasks(self):
        """Search tasks by keyword"""
        if not self.tasks:
            print("\n📭 No tasks to search!")
            return
        
        keyword = input("\n🔍 Enter search keyword: ").lower().strip()
        if not keyword:
            print("❌ Please enter a keyword!")
            return
        
        results = []
        for task in self.tasks:
            if (keyword in task['title'].lower() or 
                keyword in task.get('description', '').lower()):
                results.append(task)
        
        if results:
            self.view_tasks(results, f"SEARCH RESULTS FOR '{keyword}'")
        else:
            print(f"\n🔍 No tasks found containing '{keyword}'")

def main():
    todo = TodoList()
    
    while True:
        todo.display_menu()
        choice = input("\nEnter your choice (1-10): ").strip()
        
        if choice == '1':
            todo.view_tasks()
        elif choice == '2':
            todo.add_task()
        elif choice == '3':
            todo.mark_complete()
        elif choice == '4':
            todo.delete_task()
        elif choice == '5':
            todo.view_completed()
        elif choice == '6':
            todo.view_pending()
        elif choice == '7':
            todo.clear_all()
        elif choice == '8':
            todo.edit_task()
        elif choice == '9':
            todo.search_tasks()
        elif choice == '10':
            print("\n💾 Saving tasks...")
            todo.save_tasks()
            print("👋 Goodbye! See you next time!")
            break
        else:
            print("❌ Invalid choice! Please enter 1-10.")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()