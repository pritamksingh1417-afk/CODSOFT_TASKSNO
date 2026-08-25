import tkinter as tk
import random
from tkinter import messagebox


choices = ["Rock", "Paper", "Scissors"]

player_score = 0
computer_score = 0


def play_game(player_choice):
    global player_score, computer_score

    computer_choice = random.choice(choices)

    player_label.config(text=f"You: {player_choice}")
    computer_label.config(text=f"Computer: {computer_choice}")

    if player_choice == computer_choice:
        result = "It's a Tie!"
    elif (
        (player_choice == "Rock" and computer_choice == "Scissors")
        or (player_choice == "Paper" and computer_choice == "Rock")
        or (player_choice == "Scissors" and computer_choice == "Paper")
    ):
        player_score += 1
        result = "You Win! 🎉"
    else:
        computer_score += 1
        result = "Computer Wins!"

    result_label.config(text=result)
    score_label.config(
        text=f"Your Score: {player_score}    Computer Score: {computer_score}"
    )


def reset_game():
    global player_score, computer_score

    player_score = 0
    computer_score = 0

    player_label.config(text="You: —")
    computer_label.config(text="Computer: —")
    result_label.config(text="Choose your move!")
    score_label.config(text="Your Score: 0    Computer Score: 0")


root = tk.Tk()
root.title("Rock Paper Scissors")
root.geometry("500x550")
root.resizable(False, False)

title_label = tk.Label(
    root,
    text="🎮 Rock Paper Scissors",
    font=("Arial", 24, "bold")
)
title_label.pack(pady=25)

instruction_label = tk.Label(
    root,
    text="Choose your move",
    font=("Arial", 14)
)
instruction_label.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=20)

rock_button = tk.Button(
    button_frame,
    text="🪨 Rock",
    command=lambda: play_game("Rock"),
    font=("Arial", 13, "bold"),
    width=10
)
rock_button.grid(row=0, column=0, padx=8)

paper_button = tk.Button(
    button_frame,
    text="📄 Paper",
    command=lambda: play_game("Paper"),
    font=("Arial", 13, "bold"),
    width=10
)
paper_button.grid(row=0, column=1, padx=8)

scissors_button = tk.Button(
    button_frame,
    text="✂️ Scissors",
    command=lambda: play_game("Scissors"),
    font=("Arial", 13, "bold"),
    width=10
)
scissors_button.grid(row=0, column=2, padx=8)

player_label = tk.Label(
    root,
    text="You: —",
    font=("Arial", 14)
)
player_label.pack(pady=10)

computer_label = tk.Label(
    root,
    text="Computer: —",
    font=("Arial", 14)
)
computer_label.pack(pady=10)

result_label = tk.Label(
    root,
    text="Choose your move!",
    font=("Arial", 20, "bold")
)
result_label.pack(pady=25)

score_label = tk.Label(
    root,
    text="Your Score: 0    Computer Score: 0",
    font=("Arial", 13, "bold")
)
score_label.pack(pady=10)

reset_button = tk.Button(
    root,
    text="Reset Game",
    command=reset_game,
    font=("Arial", 12, "bold"),
    width=15
)
reset_button.pack(pady=20)

root.mainloop()