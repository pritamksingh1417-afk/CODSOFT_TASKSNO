import customtkinter as ctk
import string
import secrets


def generate_password():
    length = int(length_slider.get())

    characters = ""

    if uppercase_var.get():
        characters += string.ascii_uppercase

    if lowercase_var.get():
        characters += string.ascii_lowercase

    if numbers_var.get():
        characters += string.digits

    if symbols_var.get():
        characters += string.punctuation

    if characters == "":
        password_box.delete(0, ctk.END)
        password_box.insert(0, "Select an option")
        strength_label.configure(text="Strength: None")
        return

    password = ""

    for i in range(length):
        password += secrets.choice(characters)

    password_box.delete(0, ctk.END)
    password_box.insert(0, password)

    check_strength(password)


def copy_password():
    password = password_box.get()

    if password == "":
        return

    root.clipboard_clear()
    root.clipboard_append(password)


def change_length(value):
    length_label.configure(text="Length: " + str(int(value)))


def check_strength(password):
    score = 0

    if len(password) >= 8:
        score += 1

    if len(password) >= 12:
        score += 1

    if any(char.isupper() for char in password):
        score += 1

    if any(char.islower() for char in password):
        score += 1

    if any(char.isdigit() for char in password):
        score += 1

    if any(char in string.punctuation for char in password):
        score += 1

    if score <= 2:
        strength_label.configure(text="Strength: Weak")

    elif score <= 4:
        strength_label.configure(text="Strength: Medium")

    else:
        strength_label.configure(text="Strength: Strong")

def change_mode():
    if mode_switch.get() == 1:
        ctk.set_appearance_mode("Dark")
    else:
        ctk.set_appearance_mode("Light")

root = ctk.CTk()

root.title("Password Generator")
root.geometry("600x750")


title = ctk.CTkLabel(
    root,
    text="Password Generator",
    font=("Arial", 28, "bold")
)
title.pack(pady=30)


length_label = ctk.CTkLabel(
    root,
    text="Length: 12",
    font=("Arial", 16)
)
length_label.pack(pady=10)


length_slider = ctk.CTkSlider(
    root,
    from_=6,
    to=32,
    number_of_steps=26,
    command=change_length
)
length_slider.set(12)
length_slider.pack(pady=10)


uppercase_var = ctk.BooleanVar(value=True)
lowercase_var = ctk.BooleanVar(value=True)
numbers_var = ctk.BooleanVar(value=True)
symbols_var = ctk.BooleanVar(value=True)


uppercase_box = ctk.CTkCheckBox(
    root,
    text="Uppercase (A-Z)",
    variable=uppercase_var
)
uppercase_box.pack(pady=8)


lowercase_box = ctk.CTkCheckBox(
    root,
    text="Lowercase (a-z)",
    variable=lowercase_var
)
lowercase_box.pack(pady=8)


numbers_box = ctk.CTkCheckBox(
    root,
    text="Numbers (0-9)",
    variable=numbers_var
)
numbers_box.pack(pady=8)


symbols_box = ctk.CTkCheckBox(
    root,
    text="Symbols (!@#)",
    variable=symbols_var
)
symbols_box.pack(pady=8)


password_box = ctk.CTkEntry(
    root,
    width=450,
    height=40
)
password_box.pack(pady=25)


generate_button = ctk.CTkButton(
    root,
    text="Generate Password",
    command=generate_password
)
generate_button.pack(pady=10)


copy_button = ctk.CTkButton(
    root,
    text="Copy Password",
    command=copy_password
)
copy_button.pack(pady=10)


strength_label = ctk.CTkLabel(
    root,
    text="Strength: Not Generated",
    font=("Arial", 16, "bold")
)
strength_label.pack(pady=20)

mode_switch = ctk.CTkSwitch(
    root,
    text="Dark Mode",
    command=change_mode
)

mode_switch.select()
mode_switch.pack(pady=10)

root.mainloop()
