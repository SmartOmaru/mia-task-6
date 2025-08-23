import state
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox

#initialize tkinter 
master = tk.Tk()
master.title("Wordle Game")
master.geometry("520x600")
master.config(bg='black')

#create label
label = tk.Label(
    master,
    text="Wordle Game",
    font=('Arial', 24, 'bold'),
    bg='black',
    fg='white')

#create frame and pack label and frame
label.pack(pady=20)
frame = tk.Frame(master, bg='grey')
frame.pack()

#create style for the letter entry boxes
style = ttk.Style()
style.theme_use("clam")

#created three styles for the entry boxes
#grey for empty boxes or not in word, yellow for letters in the word but not in the right position, and green for letters in the right position
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

#function to check if the character is a letter
def only_letters(char):
    return char.isalpha() or char == ""

#validate command to check if the character entered is a letter
validate_command = (master.register(only_letters), "%S")
#creating the main grid of boxes
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
        
        entry.bind("<KeyRelease>", lambda event, row=i, col=j: on_key(event, row, col)) #run function "on_key" on key release
        
    state.entries.append(entries_row) #storing the entries in a list for later use

#function to focus on the current entry box and disable others for stability
def only_current():
    for i in range(6):
        for j in range (5):
            if i == state.current_row and j == state.current_col:
                state.entries[i][j].config(state="normal")
                state.entries[i][j].focus()
                
            else:
                state.entries[i][j].config(state="readonly")

#function to handle key presses such as typing letters, backspace, and enter
#it also checks if the current row and column match the state variables to ensure the correct entry
def on_key(event, row, col):
    box = event.widget
    
    if row != state.current_row or col != state.current_col:
        state.entries[state.current_row][state.current_col].focus()
        return
     
    if event.keysym == "BackSpace":
        if box.get() != "":
            box.delete(0, "end")
        elif col > 0:
            state.current_col -= 1
            only_current()
            prev_box = state.entries[state.current_row][state.current_col]
            prev_box.delete(0, "end")
        return
        
    typed = box.get().upper()
    if len(typed) > 0:
        box.delete(0, "end")
        box.insert(0, typed[-1])
        
        if col < 4:
            state.current_col += 1
            only_current()
    
    if event.keysym == "Return" and  col == 4 and state.entries[row][col].get() != "":
        state.current_guess = get_current_guess()
        on_submit(row)
        
        if row < 5:
            state.current_row += 1
            state.current_col = 0
            only_current()

#function to get the current guess from the entry boxes
#it concatenates the text from the entry boxes in the current row to form the guess and returns it as lowercase
#this is used to compare the guess with the current word
def get_current_guess():
    return ("".join(entry.get() for entry in state.entries[state.attempts if state.attempts < 6 else 5])).lower()

#function to show a popup message with a title, message, color, and optional function
#the popup can either end the game or continue based on the function parameter
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

#function to handle the submission of the current guess
#it checks if the guess is a word in the word list, then compares it with the current word and updates the entry boxes based on the result
def on_submit(row):
    state.attempts += 1
    
    if state.current_guess not in state.words:
        for i in range(5):
            state.entries[state.current_row][i].config(state="normal")
            state.entries[state.current_row][i].delete(0, "end")
        show_popup("Invalid Word", "Not in word list", "white", "continue")
        if state.current_row < 5:
            state.current_row -= 1 
        state.current_col = 0
        only_current()
        state.attempts -= 1
        return
    
    if state.current_guess == state.current_word:
        show_popup("You won :)", "Congrats!", "green")
        
    if state.attempts >= 6:
        show_popup("You lost :(", "The word was: " + (state.current_word).upper, "red")
        
    for i in range(len(state.current_guess)):
        if state.current_guess[i] == state.current_word[i]:
            state.entries[row][i].config(state="readonly", style="Green.TEntry")
        elif state.current_guess[i] in state.current_word:
            state.entries[row][i].config(state="readonly", style="Yellow.TEntry")
        else:
            state.entries[row][i].config(state="readonly", style="Grey.TEntry")

#run the main loop of the tkinter application
#this keeps the window open and responsive to user input unless closed by the user or game ends
master.mainloop() 
