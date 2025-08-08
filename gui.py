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

for i in range(6):
    for j in range(5):
        entry = tk.Entry(
            frame,
            font=('Arial', 40, 'bold'),
            width=2,
            justify='center',
            bg='grey')
        entry.grid(row=i, column=j, padx=5, pady=5)
        
master.mainloop()