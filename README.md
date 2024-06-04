# Minesweeper Game

Python 3.12 implementation of the classic Minesweeper game.

## Constants

```py
MINE = -1    # Represents a cell that contains a mine.
EMPTY = 0    # Represents an empty cell with no adjacent mines.
HIDDEN = -2  # Represents a hidden cell that has not been revealed by the player.
MARKED = -3  # Represents a cell marked by the player as containing a mine.
```

## Board Size and Mine Count
```py
SIZE = 16        # Size of the game board (16x16).
MINE_COUNT = 40  # Total number of mines on the board.
```

## How to Play

1. Run the main.py script.
    The game will display the current state of the player table.
2. Enter your move in the format Mode (o/m), Row, Col where:
    - o stands for opening a cell.
    - m stands for marking a cell as containing a mine.
    - Row is the row number of the cell.
    - Col is the column number of the cell.

    
- The game will update the board based on your input.
- The game ends when you open a cell containing a mine (lose) or mark all mines correctly and open all other cells (win).

## Example

`Mode (o/m), Row, Col: o, 3, 5`

This command opens the cell at row 3, column 5.

`Mode (o/m), Row, Col: m, 4, 6`

This command marks the cell at row 4, column 6 as containing a mine.
