from random import choice as random_choice

with open("words.txt", "r") as file:
    words = [line.strip() for line in file] 
      
entries = [0]
current_word = random_choice(words)
current_guess = str("")
attempts = 0
current_row = 0
current_col = 0
