import tkinter as tk

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

entries = []
for i in range(6):
    entries_row = []
    for j in range(5):
        entry = tk.Entry(
            frame,
            font=('Arial', 40, 'bold'),
            width=2,
            justify='center',
            bg='grey')
        entry.grid(row=i, column=j, padx=5, pady=5)
        entries_row.append(entry)
        
        entry.bind("<KeyRelease>", lambda event, row=i, col=j: on_key(event, row, col))
        
    entries.append(entries_row)

def on_key(event, row, col):
   
    box = event.widget
    
    if event.keysym == "BackSpace":
        if col > 0:
            entries[row][col - 1].focus()
        box.delete(0, "end")
        return
        
    typed = box.get().upper()
    if len(typed) > 0:
        box.delete(0, "end")
        box.insert(0, typed[-1])
        if col < 4:
            entries[row][col + 1].focus()
    

        
        
        


master.mainloop()