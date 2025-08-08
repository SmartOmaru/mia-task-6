from random import choice as random_choice

with open("words.txt", "r") as file:
    words = [line.strip() for line in file] 
    
current_word = random_choice(words)
current_guess = ""
attempts = 0
guessed = False