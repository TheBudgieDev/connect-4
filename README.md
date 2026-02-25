# Connect 4 (Python Console Game)

A feature-rich, console-based Connect 4 game with an AI opponent, written in Python for the ICS3UI midterm project.

---

## Features

- **Classic Connect 4 gameplay**: 7x6 board, two players (human vs. AI)
- **Animated piece drops** and coloured output for an engaging terminal experience
- **AI opponent** using Minimax with alpha-beta pruning and positional heuristics
- **Win detection** for horizontal, vertical, and diagonal connections
- **Replay option** after each game
- **Customizable difficulty** (by changing AI search depth in code)
- **Clear, modular codebase** for easy extension

---

## How to Play

1. **Run the game**:
   ```bash
   python main.py

---

## Requirements
- Python 3.7 or higher
- Windows, macOS, or Linux terminal with ANSI color support
- No external dependencies (uses only Python standard library)

---

## File Structure

- `main.py` \- Main game loop and UI
- `Game.py` \- Game logic and board representation
- `AI.py` \- AI solver logic
- `TextFormatting.py` \- Terminal text formatting
