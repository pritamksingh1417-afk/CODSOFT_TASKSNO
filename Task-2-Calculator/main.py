import tkinter as tk
from tkinter import messagebox


def calculate():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        operation = operation_var.get()

        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "×":
            result = num1 * num2
        elif operation == "÷":
            if num2 == 0:
                messagebox.showerror("Error", "Cannot divide by zero.")
                return
            result = num1 / num2
        else:
            messagebox.showwarning("Warning", "Please select an operation.")
            return

        result_label.config(text=f"Result: {result:g}")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numbers.")


def clear():
    entry_num1.delete(0, tk.END)
    entry_num2.delete(0, tk.END)
    operation_var.set("+")
    result_label.config(text="Result: —")


root = tk.Tk()
root.title(" Calculator")
root.geometry("400x550")
root.resizable(False, False)

title_label = tk.Label(
    root,
    text="🧮 Calculator",
    font=("Arial", 22, "bold")
)
title_label.pack(pady=25)

tk.Label(
    root,
    text="Enter First Number",
    font=("Arial", 12)
).pack()

entry_num1 = tk.Entry(
    root,
    font=("Arial", 14),
    justify="center"
)
entry_num1.pack(pady=8)

tk.Label(
    root,
    text="Enter Second Number",
    font=("Arial", 12)
).pack()

entry_num2 = tk.Entry(
    root,
    font=("Arial", 14),
    justify="center"
)
entry_num2.pack(pady=8)

tk.Label(
    root,
    text="Select Operation",
    font=("Arial", 12)
).pack(pady=(15, 5))

operation_var = tk.StringVar(value="+")

operation_menu = tk.OptionMenu(
    root,
    operation_var,
    "+",
    "-",
    "×",
    "÷"
)
operation_menu.config(
    font=("Arial", 13),
    width=8
)
operation_menu.pack()

calculate_button = tk.Button(
    root,
    text="Calculate",
    command=calculate,
    font=("Arial", 13, "bold"),
    width=15
)
calculate_button.pack(pady=20)

clear_button = tk.Button(
    root,
    text="Clear",
    command=clear,
    font=("Arial", 12),
    width=15
)
clear_button.pack()

result_frame = tk.Frame(
    root,
    bd=2,
    relief="groove"
)
result_frame.pack(
    pady=20,
    padx=40,
    fill="x"
)

result_label = tk.Label(
    result_frame,
    text="Result: —",
    font=("Arial", 18, "bold"),
    pady=15
)
result_label.pack()

root.mainloop()