import customtkinter as ctk
from tkinter import messagebox
import json
import os


tasks = []
file_name = "tasks.json"
current_filter = "All"


def save_tasks():
    with open(file_name, "w") as file:
        json.dump(tasks, file, indent=4)


def load_tasks():
    global tasks

    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            tasks = json.load(file)


def add_task():
    task = task_entry.get().strip()

    if task == "":
        messagebox.showwarning("Warning", "Enter a task first.")
        return

    tasks.append({
        "name": task,
        "completed": False
    })

    task_entry.delete(0, ctk.END)

    save_tasks()
    show_tasks()


def get_tasks():
    result = []
    search = search_entry.get().lower()

    for task in tasks:

        if search not in task["name"].lower():
            continue

        if current_filter == "Pending" and task["completed"]:
            continue

        if current_filter == "Completed" and not task["completed"]:
            continue

        result.append(task)

    return result


def show_tasks():

    for widget in task_frame.winfo_children():
        widget.destroy()

    visible_tasks = get_tasks()

    for task in visible_tasks:

        box = ctk.CTkFrame(task_frame)
        box.pack(
            fill="x",
            padx=5,
            pady=5
        )

        if task["completed"]:
            text = "✓ " + task["name"]
        else:
            text = task["name"]

        label = ctk.CTkLabel(
            box,
            text=text,
            font=("Arial", 15),
            anchor="w"
        )

        label.pack(
            side="left",
            padx=10,
            pady=10,
            fill="x",
            expand=True
        )

        complete_button = ctk.CTkButton(
            box,
            text="✓",
            width=40,
            command=lambda t=task: complete_task(t)
        )

        complete_button.pack(
            side="right",
            padx=4
        )

        edit_button = ctk.CTkButton(
            box,
            text="Edit",
            width=60,
            command=lambda t=task: edit_task(t)
        )

        edit_button.pack(
            side="right",
            padx=4
        )

        delete_button = ctk.CTkButton(
            box,
            text="Delete",
            width=70,
            command=lambda t=task: delete_task(t)
        )

        delete_button.pack(
            side="right",
            padx=4
        )

    update_count()


def complete_task(task):

    task["completed"] = True

    save_tasks()
    show_tasks()


def delete_task(task):

    answer = messagebox.askyesno(
        "Delete",
        "Do you want to delete this task?"
    )

    if answer:
        tasks.remove(task)
        save_tasks()
        show_tasks()


def edit_task(task):

    window = ctk.CTkToplevel(root)

    window.title("Edit Task")
    window.geometry("400x200")

    window.grab_set()

    label = ctk.CTkLabel(
        window,
        text="Edit Task",
        font=("Arial", 20, "bold")
    )

    label.pack(pady=20)

    entry = ctk.CTkEntry(
        window,
        width=300
    )

    entry.pack(pady=10)

    entry.insert(0, task["name"])

    def save_change():

        new_name = entry.get().strip()

        if new_name == "":
            messagebox.showwarning(
                "Warning",
                "Task cannot be empty."
            )
            return

        task["name"] = new_name

        save_tasks()
        show_tasks()

        window.destroy()

    button = ctk.CTkButton(
        window,
        text="Save",
        command=save_change
    )

    button.pack(pady=10)


def search_task(event=None):
    show_tasks()


def change_filter(value):

    global current_filter

    current_filter = value

    show_tasks()


def update_count():

    total = len(tasks)
    completed = 0

    for task in tasks:
        if task["completed"]:
            completed += 1

    pending = total - completed

    count_label.configure(
        text="Total: " + str(total) +
        "    Pending: " + str(pending) +
        "    Completed: " + str(completed)
    )


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


root = ctk.CTk()

root.title("My To-Do List")
root.geometry("800x650")
root.minsize(650, 500)


title = ctk.CTkLabel(
    root,
    text="My To-Do List",
    font=("Arial", 30, "bold")
)

title.pack(pady=(25, 5))


subtitle = ctk.CTkLabel(
    root,
    text="Organize your tasks",
    font=("Arial", 14)
)

subtitle.pack(pady=(0, 20))


input_frame = ctk.CTkFrame(
    root,
    fg_color="transparent"
)

input_frame.pack(
    fill="x",
    padx=30
)


task_entry = ctk.CTkEntry(
    input_frame,
    placeholder_text="Enter a new task...",
    height=40
)

task_entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 10)
)


add_button = ctk.CTkButton(
    input_frame,
    text="Add Task",
    width=100,
    height=40,
    command=add_task
)

add_button.pack(side="right")


search_entry = ctk.CTkEntry(
    root,
    placeholder_text="Search tasks...",
    height=38
)

search_entry.pack(
    fill="x",
    padx=30,
    pady=15
)

search_entry.bind(
    "<KeyRelease>",
    search_task
)


filter_frame = ctk.CTkFrame(
    root,
    fg_color="transparent"
)

filter_frame.pack(pady=5)


all_button = ctk.CTkButton(
    filter_frame,
    text="All",
    width=90,
    command=lambda: change_filter("All")
)

all_button.grid(
    row=0,
    column=0,
    padx=5
)


pending_button = ctk.CTkButton(
    filter_frame,
    text="Pending",
    width=90,
    command=lambda: change_filter("Pending")
)

pending_button.grid(
    row=0,
    column=1,
    padx=5
)


completed_button = ctk.CTkButton(
    filter_frame,
    text="Completed",
    width=90,
    command=lambda: change_filter("Completed")
)

completed_button.grid(
    row=0,
    column=2,
    padx=5
)


count_label = ctk.CTkLabel(
    root,
    text="Total: 0    Pending: 0    Completed: 0",
    font=("Arial", 14, "bold")
)

count_label.pack(pady=15)


task_frame = ctk.CTkScrollableFrame(
    root,
    label_text="Tasks"
)

task_frame.pack(
    fill="both",
    expand=True,
    padx=30,
    pady=(0, 20)
)


load_tasks()
show_tasks()

root.mainloop()