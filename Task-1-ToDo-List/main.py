import customtkinter as ctk
from tkinter import messagebox
import json
import os


# -------------------- DATA --------------------

tasks = []
FILE_NAME = "tasks.json"
current_filter = "All"


# -------------------- SAVE / LOAD --------------------

def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)


def load_tasks():
    global tasks

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r") as file:
            tasks = json.load(file)


# -------------------- TASK FUNCTIONS --------------------

def add_task():
    task_name = task_entry.get().strip()

    if task_name == "":
        messagebox.showwarning("Warning", "Please enter a task.")
        return

    tasks.append({
        "name": task_name,
        "completed": False
    })

    task_entry.delete(0, ctk.END)

    save_tasks()
    refresh_tasks()


def get_visible_tasks():
    visible_tasks = []

    search_text = search_entry.get().lower()

    for task in tasks:

        if search_text not in task["name"].lower():
            continue

        if current_filter == "Pending" and task["completed"]:
            continue

        if current_filter == "Completed" and not task["completed"]:
            continue

        visible_tasks.append(task)

    return visible_tasks


def refresh_tasks():
    for widget in task_scroll_frame.winfo_children():
        widget.destroy()

    visible_tasks = get_visible_tasks()

    for index, task in enumerate(visible_tasks):

        task_frame = ctk.CTkFrame(
            task_scroll_frame,
            corner_radius=10
        )

        task_frame.pack(
            fill="x",
            padx=10,
            pady=5
        )

        if task["completed"]:
            text = "✓  " + task["name"]
        else:
            text = task["name"]

        task_label = ctk.CTkLabel(
            task_frame,
            text=text,
            font=("Arial", 15),
            anchor="w"
        )

        task_label.pack(
            side="left",
            padx=15,
            pady=12,
            fill="x",
            expand=True
        )

        complete_button = ctk.CTkButton(
            task_frame,
            text="✓",
            width=40,
            command=lambda t=task: complete_task(t)
        )

        complete_button.pack(
            side="right",
            padx=5
        )

        edit_button = ctk.CTkButton(
            task_frame,
            text="Edit",
            width=55,
            command=lambda t=task: edit_task(t)
        )

        edit_button.pack(
            side="right",
            padx=5
        )

        delete_button = ctk.CTkButton(
            task_frame,
            text="Delete",
            width=65,
            command=lambda t=task: delete_task(t)
        )

        delete_button.pack(
            side="right",
            padx=5
        )

    update_statistics()


def complete_task(task):
    task["completed"] = True

    save_tasks()
    refresh_tasks()


def delete_task(task):
    confirm = messagebox.askyesno(
        "Delete Task",
        "Are you sure you want to delete this task?"
    )

    if confirm:
        tasks.remove(task)

        save_tasks()
        refresh_tasks()


def edit_task(task):
    edit_window = ctk.CTkToplevel(root)

    edit_window.title("Edit Task")
    edit_window.geometry("400x200")

    edit_window.grab_set()

    label = ctk.CTkLabel(
        edit_window,
        text="Edit Task",
        font=("Arial", 20, "bold")
    )

    label.pack(pady=20)

    edit_entry = ctk.CTkEntry(
        edit_window,
        width=300
    )

    edit_entry.pack(pady=10)

    edit_entry.insert(0, task["name"])

    def save_edit():

        new_name = edit_entry.get().strip()

        if new_name == "":
            messagebox.showwarning(
                "Warning",
                "Task cannot be empty."
            )
            return

        task["name"] = new_name

        save_tasks()
        refresh_tasks()

        edit_window.destroy()

    save_button = ctk.CTkButton(
        edit_window,
        text="Save Changes",
        command=save_edit
    )

    save_button.pack(pady=15)


# -------------------- SEARCH --------------------

def search_tasks(event=None):
    refresh_tasks()


# -------------------- FILTERS --------------------

def set_filter(filter_name):
    global current_filter

    current_filter = filter_name

    refresh_tasks()


# -------------------- STATISTICS --------------------

def update_statistics():

    total = len(tasks)

    completed = 0

    for task in tasks:
        if task["completed"]:
            completed += 1

    pending = total - completed

    statistics_label.configure(
        text=f"Total: {total}     Pending: {pending}     Completed: {completed}"
    )


# -------------------- APPEARANCE --------------------

ctk.set_appearance_mode("System")

ctk.set_default_color_theme("blue")

def add_task_with_enter(event):
    add_task()


def focus_search(event):
    search_entry.focus()


def clear_search(event):
    search_entry.delete(0, ctk.END)
    refresh_tasks()
# -------------------- MAIN WINDOW --------------------

root = ctk.CTk()

root.title("Smart To-Do List")

root.geometry("900x700")

root.minsize(750, 600)


# -------------------- HEADER --------------------

header_frame = ctk.CTkFrame(
    root,
    corner_radius=0
)

header_frame.pack(
    fill="x"
)


title_label = ctk.CTkLabel(
    header_frame,
    text="Smart To-Do List",
    font=("Arial", 30, "bold")
)

title_label.pack(pady=(20, 5))


subtitle_label = ctk.CTkLabel(
    header_frame,
    text="Organize your tasks. Stay productive.",
    font=("Arial", 14)
)

subtitle_label.pack(
    pady=(0, 20)
)


# -------------------- INPUT AREA --------------------

input_frame = ctk.CTkFrame(
    root,
    fg_color="transparent"
)

input_frame.pack(
    fill="x",
    padx=40,
    pady=20
)


task_entry = ctk.CTkEntry(
    input_frame,
    placeholder_text="Enter a new task...",
    height=45,
    font=("Arial", 14)
)

task_entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 10)
)


add_button = ctk.CTkButton(
    input_frame,
    text="+ Add Task",
    width=120,
    height=45,
    command=add_task
)

add_button.pack(
    side="right"
)


# -------------------- SEARCH --------------------

search_entry = ctk.CTkEntry(
    root,
    placeholder_text="🔍 Search tasks...",
    height=40,
    font=("Arial", 13)
)

search_entry.pack(
    fill="x",
    padx=40,
    pady=(0, 15)
)

search_entry.bind(
    "<KeyRelease>",
    search_tasks
)
root.bind("<Return>", add_task_with_enter)
root.bind("<Control-f>", focus_search)
root.bind("<Escape>", clear_search)


# -------------------- FILTER BUTTONS --------------------

filter_frame = ctk.CTkFrame(
    root,
    fg_color="transparent"
)

filter_frame.pack(pady=5)


all_button = ctk.CTkButton(
    filter_frame,
    text="All",
    width=100,
    command=lambda: set_filter("All")
)

all_button.grid(
    row=0,
    column=0,
    padx=5
)


pending_button = ctk.CTkButton(
    filter_frame,
    text="Pending",
    width=100,
    command=lambda: set_filter("Pending")
)

pending_button.grid(
    row=0,
    column=1,
    padx=5
)


completed_button = ctk.CTkButton(
    filter_frame,
    text="Completed",
    width=100,
    command=lambda: set_filter("Completed")
)

completed_button.grid(
    row=0,
    column=2,
    padx=5
)


# -------------------- STATISTICS --------------------

statistics_label = ctk.CTkLabel(
    root,
    text="Total: 0     Pending: 0     Completed: 0",
    font=("Arial", 14, "bold")
)

statistics_label.pack(
    pady=15
)


# -------------------- TASK LIST --------------------

task_scroll_frame = ctk.CTkScrollableFrame(
    root,
    label_text="Your Tasks"
)

task_scroll_frame.pack(
    fill="both",
    expand=True,
    padx=40,
    pady=(0, 20)
)


# -------------------- START APPLICATION --------------------

load_tasks()

refresh_tasks()

root.mainloop()