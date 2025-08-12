# Wordle Game
## What is this?
This is the sixth task for the MIA (Made In Alexandria) robotics team, and it required us to create a working wordle game with a fully functional GUI using a dataset of five-letter words.

## Folder Structure
| Name | Contents |
| ----- | --- |
| gui.py | main game logic and GUI elements |
| state.py | game state variables such as the currently guessed word |
| words.txt | words dataset |

## Logical Structure
### Code flow
1. gui.py builds the UI (grid of entry widgets) and handles input.

2. Player types letters; input is restricted to the current cell and letters only.

3. On Enter (last column and can't be empty), the row is read and:

   - If the guess is invalid (not in word list) → row cleared, 
player retries same row.

   - If valid → color feedback applied, attempts incremented, move to next row.
4. If the guess matches the currently selected word from the word list, show a popup that indicates a win. If all attempts are used, show a popup that indicates a loss.

### Design choices

1. all logic happens in response to UI events, which is appropriate for Tkinter.
2. restrict input to the active cell: achieves Wordle-like sequential typing and maintains game state.
3. readonly + styles for feedback: locks past rows and visually communicates correctness.
4. colored popups to clearly indicate game state (win or loss)

### Main functions

#### on_key(event, row, col)
- Ensures only the active cell accepts input; redirects focus if needed.

- Handles:

  - Typing: accepts the character entered(last character only if multiple were entered), uppercases it, advances to the next cell.

  - Backspace: deletes current cell; if empty, steps back one cell and clears it, like in Wordle.

  - Enter: if last cell has text, builds the guess and calls on_submit.

### on_submit(row)
- Reads the current guess (get_current_guess()).

- If not in state.words: clear the row, show invalid-word popup, keep same row.

- If valid:

  - Color each letter box (Green / Yellow / Grey) accordingly and sets the current row to readonly.

  - Increment attempts, moves on to the next row, resets current_col variable to start again from the first box in that row.

  - If guess == current_word → show win popup.

  - If attempts all attempts have been used → show loss popup.
