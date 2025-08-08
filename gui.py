import state
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox

master = tk.Tk()
master.title("Wordle Game")
master.geometry("520x600")
master.config(bg='black')

label = tk.Label(
    master,
    text="Wordle Game",
    font=('Arial', 24, 'bold'),
    bg='black',
    fg='white')

label.pack(pady=20)
frame = tk.Frame(master, bg='black')
frame.pack()

style = ttk.Style()
style.theme_use("clam")
style.configure("Grey.TEntry", 
                foreground='black',
                fieldbackground='grey',
                font=('Arial', 40, 'bold'))

style.configure("Yellow.TEntry", 
                foreground='black',
                fieldbackground='yellow',
                font=('Arial', 40, 'bold'))
                
style.configure("Green.TEntry", 
                foreground='black',
                fieldbackground='green',
                font=('Arial', 40, 'bold'))

def only_current():
    for i in range(6):
        for j in range (5):
            if i == current_row and j == current_col:
                entries[i][j].config(state="normal")
                entries[i][j].focus()
            else:
                entries[i][j].config(state="readonly")

def only_letters(char):
    return char.isalpha() or char == ""

validate_command = (master.register(only_letters), "%S")

entries = []
for i in range(6):
    entries_row = []
    for j in range(5):
        entry = ttk.Entry(
            frame,
            validate="key",
            validatecommand=(validate_command),
            font=('Arial', 40, 'bold'),
            width=2,
            justify='center',
            style="Grey.TEntry",
            state="normal" if i == 0 and j == 0 else "readonly")
        entry.grid(row=i, column=j, padx=5, pady=5)
        entries_row.append(entry)
        
        entry.bind("<KeyRelease>", lambda event, row=i, col=j: on_key(event, row, col))
        
    entries.append(entries_row)
current_row = 0
current_col = 0
def on_key(event, row, col):
    global current_row, current_col
    box = event.widget
    
    if row != current_row or col != current_col:
        entries[current_row][current_col].focus()
        return
     
    if event.keysym == "BackSpace":
        if col > 0:
            current_col -= 1
            only_current()
        box.delete(0, "end")
        return
        
    typed = box.get().upper()
    if len(typed) > 0:
        box.delete(0, "end")
        box.insert(0, typed[-1])
        if col < 4:
            current_col += 1
            only_current()
    
    if event.keysym == "Return" and  col == 4:
        state.current_guess = get_current_guess()
        print(state.current_guess)
        print("bro the word is ", state.current_word)
        on_submit(row)
        if row < 5:
            current_row += 1
            current_col = 0
            only_current()
            
def get_current_guess():
    return ("".join(entry.get() for entry in entries[state.attempts if state.attempts < 6 else 5])).lower()

def show_popup(title, message, color, function="end"):
    popup = tk.Toplevel(master)
    popup.title(title)
    popup.config(bg=color)
    popup.geometry("300x200")
    label = tk.Label(popup, text=message, bg=color, fg='black', font=('Arial', 14))
    label.pack(padx=20, pady=20)
    if function == "end":
        button = tk.Button(popup, text="Exit", command=master.destroy)
    elif function == "continue":
         button = tk.Button(popup, text="OK", command=popup.destroy)
    button.pack(pady=10)
    popup.grab_set()

def on_submit(row):
    global current_row
    global current_col
    state.attempts += 1
    if state.current_guess not in state.words:
        for i in range(5):
            entries[current_row][i].config(state="normal")
            entries[current_row][i].delete(0, "end")
        show_popup("Invalid Word", "Not in word list", "white", "continue")
        current_row -= 1 
        current_col = 0
        only_current()
        state.attempts -= 1
        return
    if state.current_guess == state.current_word:
        show_popup("You won :)", "Congrats!", "green")
    if state.attempts >= 6:
        show_popup("You lost :(", "The word was: " + state.current_word, "red")
    for i in range(len(state.current_guess)):
        if state.current_guess[i] == state.current_word[i]:
            entries[row][i].config(state="readonly", style="Green.TEntry")
        elif state.current_guess[i] in state.current_word:
            entries[row][i].config(state="readonly", style="Yellow.TEntry")
        else:
            entries[row][i].config(state="readonly", style="Grey.TEntry")
    

master.mainloop()