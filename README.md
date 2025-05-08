# Reversi Game (Othello) against Minimax AI

This is a Python implementation of the Reversi (Othello) board game, where a human player (Black) plays against an AI (White) using the Minimax algorithm with alpha-beta pruning.

## Game rules

- [How to Play Reversi - Wikihow](https://www.wikihow.com/Play-Reversi)

## Features

- Text-based Reversi game on an 8x8 board
- Black player (B) is human-controlled
- White player (W) is AI-controlled using the Minimax algorithm
- AI evaluates board positions dynamically with adjustable search depth
- Valid move detection and disc flipping logic
- Displays the board after each turn
- Declares the winner when no more moves are available
- The end of game:
	- all fields are filled
	- there are no more available fields

## Files

### `board.py`
Defines the `Board` class, which includes:

- Board initialization
- Move validation
- Move execution and disc flipping
- Board rendering to the console
- Evaluation function for the AI
- Game end and winner announcement logic

### `reverse.py`
Handles the game loop and AI:

- Human player move input and validation
- AI move selection using Minimax with alpha-beta pruning
- Dynamically adjusts AI search depth based on number of available moves
- Main loop alternates turns between the player and AI until no moves remain

## How to Run

1. Make sure you have Python 3 installed.
2. Save `board.py` and `reverse.py` in the same directory.
3. Run the game with:

```bash
python reverse.py

