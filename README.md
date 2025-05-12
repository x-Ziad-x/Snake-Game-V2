# Snake Game

A classic Snake game implementation with player profiles, high score tracking, and customizable settings.

## Features

- Player profile system with alias management
- Persistent high score tracking using SQLite database
- Adjustable game speed (Slow/Medium/Fast)
- Toggleable border collision (enabled/disabled)
- Clean graphical interface

## How to Run

### Option 1: EXE Version (Recommended for Windows)
1. Download the `SnakeGame.exe` file from releases
2. Double-click to run the game
3. If Windows shows a security warning, click "More info" then "Run anyway"

### Option 2: Python Version
1. Ensure you have Python 3.x installed
2. Run the game:

## Game Settings

- Speed: Slow, Medium, Fast
- Slow: Easier difficulty
- Medium: Balanced gameplay
- Fast: Challenging difficulty

- Borders:
- Enabled: Classic mode (die on wall collision)
- Disabled: Wraparound mode (snake appears on opposite side)

## Database

The game stores data in a SQLite database file (`User DataBase.db` in the same directory):
- Player aliases
- All game scores
- Highest scores per player

## Author

Developed by Ziad
