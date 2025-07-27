import tkinter as tk
from tkinter import messagebox
import csv
import random

# Load wordlist from CSV
def load_words(filename):
    words = []
    with open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            words.append({"English": row["English"], "Arabic": row["Arabic"]})
    return words

# Pick question and choices
def get_question(wordlist):
    correct = random.choice(wordlist)
    choices = [correct["Arabic"]]
    while len(choices) < 4:
        option = random.choice(wordlist)["Arabic"]
        if option not in choices:
            choices.append(option)
    random.shuffle(choices)
    return correct["English"], correct["Arabic"], choices

# Handle team answer
def handle_answer(team, selected_choice, correct_answer):
    global team1_score, team2_score, current_turn
    stop_timer()
    if selected_choice == correct_answer:
        if team == 1:
            team1_score += 1
        else:
            team2_score += 1
    update_score()
    root.after(500, next_question)

# Update score display
def update_score():
    score_label.config(text=f"Team 1: {team1_score}     Team 2: {team2_score}")

# Countdown timer function
def start_timer():
    global remaining_time
    remaining_time = 20
    update_timer()

def update_timer():
    global remaining_time
    timer_label.config(text=f"⏱️ Time left: {remaining_time}s")
    if remaining_time > 0:
        remaining_time -= 1
        global timer_id
        timer_id = root.after(1000, update_timer)
    else:
        messagebox.showinfo("Time's up!", "No answer in time!\nNext question.")
        next_question()

def stop_timer():
    global timer_id
    if timer_id is not None:
        root.after_cancel(timer_id)
        timer_id = None

# Show next question
def next_question():
    global current_question, correct_answer, choices, current_turn
    stop_timer()
    if len(used_words) == len(wordlist):
        end_game()
        return
    while True:
        english, correct, choices_list = get_question(wordlist)
        if english not in used_words:
            used_words.add(english)
            break
    current_question.set(english)
    correct_answer = correct
    choices = choices_list
    for i, choice in enumerate(choices):
        buttons[i].config(text=choice)
    current_turn = 1 if current_turn == 2 else 2
    turn_label.config(text=f"Team {current_turn}'s Turn")
    start_timer()

# End of game
def end_game():
    stop_timer()
    if team1_score > team2_score:
        winner = "Team 1 Wins!"
    elif team2_score > team1_score:
        winner = "Team 2 Wins!"
    else:
        winner = "It's a Tie!"
    messagebox.showinfo("Game Over", f"Final Score:\nTeam 1: {team1_score}\nTeam 2: {team2_score}\n\n{winner}")
    root.destroy()

# -------------------- GUI Setup --------------------
wordlist = load_words("wordlist.csv")
used_words = set()
team1_score = 0
team2_score = 0
current_turn = 1
current_question = tk.StringVar()
correct_answer = ""
choices = []
remaining_time = 20
timer_id = None

root = tk.Tk()
root.title("Vocabulary Quiz Game")
root.geometry("500x450")

title = tk.Label(root, text="English Vocabulary Quiz", font=("Arial", 20))
title.pack(pady=10)

turn_label = tk.Label(root, text="Team 1's Turn", font=("Arial", 14))
turn_label.pack(pady=5)

question_label = tk.Label(root, textvariable=current_question, font=("Arial", 18))
question_label.pack(pady=10)

timer_label = tk.Label(root, text="⏱️ Time left: 20s", font=("Arial", 14), fg="red")
timer_label.pack(pady=5)

buttons = []
for i in range(4):
    btn = tk.Button(root, text="", font=("Arial", 16), width=20,
                    command=lambda i=i: handle_answer(current_turn, buttons[i]['text'], correct_answer))
    btn.pack(pady=5)
    buttons.append(btn)

score_label = tk.Label(root, text="Team 1: 0     Team 2: 0", font=("Arial", 14))
score_label.pack(pady=15)

next_question()
root.mainloop()
