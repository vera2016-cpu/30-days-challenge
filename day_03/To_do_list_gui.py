import tkinter as tk
import os

# Clear the terminal screen before the app starts
os.system('cls')

# Create the main window
root = tk.Tk()
root.configure(bg="#242424")
root.title("My To-Do List")
root.geometry("300x400")

# --- FUNCTIONS ---

def save_tasks():
    tasks = listbox_tasks.get(0, tk.END)
    with open("tasks.txt", "w") as f:
        for t in tasks:
            f.write(t + "\n")

def load_tasks():
    if os.path.exists("tasks.txt"):
        with open("tasks.txt", "r") as f:
            tasks = f.readlines()
            for t in tasks:
                listbox_tasks.insert(tk.END, t.strip())

# We added 'event=None' here so it works with both the Button AND the Enter key
def add_task(event=None):
    # Get the text that the user typed
    task = entry_task.get()
    
    if task:
        # Add the task to the end of the listbox
        listbox_tasks.insert(tk.END, task)
        # Clear the text box
        entry_task.delete(0, tk.END)
        save_tasks()

def delete_task():
    # Get the index of the item currently selected
    selection = listbox_tasks.curselection()
    
    if selection:
        task_index = selection[0]
        listbox_tasks.delete(task_index)
        save_tasks()

# --- GUI LAYOUT ---

label_title = tk.Label(root, text="My To-Do List", bg="#242424", fg="white", font=("Helvetica", 16, "bold"))
label_title.pack(pady=10)

# Create an entry box where the user can type a task
entry_task = tk.Entry(root, width=30)
entry_task.pack(pady=10)

# Create a button to add the task
button_add = tk.Button(root, text="Add Task", command=add_task)
button_add.pack(pady=5)

# Create a button to delete
button_delete = tk.Button(root, text="Delete Task", command=delete_task)
button_delete.pack(pady=5)

# Create the listbox to display tasks
listbox_tasks = tk.Listbox(root, height=10, width=40)
listbox_tasks.pack(pady=10)

# --- BINDING & LOADING ---

# This tells the app: "When the user hits Enter, run the add_task function"
root.bind('<Return>', add_task)

# Load old tasks
load_tasks()

# Start the application loop
root.mainloop()