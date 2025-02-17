# Infinite Tic Tac Toe

wow!

A modern twist on the classic Tic Tac Toe game, featuring a unique "infinite" gameplay mechanic where pieces have limited permanence on the board. Built with Pygame, this game offers both Player vs Player and Player vs AI modes with multiple difficulty levels.

## Features

### Multiple Game Modes
- **Player vs Player (PVP)**
  - Traditional 2-player gameplay
  - Each player can have up to 3 pieces on the board
  - Oldest piece disappears when placing a 4th piece
  - Players can choose their symbol (X or O)

- **Player vs AI (PVAI)**
  - Play against the computer
  - Three difficulty levels:
    - Easy: Random moves
    - Medium: Mix of random and strategic moves
    - Hard: Uses minimax algorithm with memory for optimal play
  - AI adapts to player's chosen symbol

### Dynamic Board Mechanics
- 3x3 grid with sliding window mechanics
- Maximum of 6 pieces on board (3 per player)
- Pieces automatically cycle as new ones are placed
- Win condition remains traditional (3 in a row)

### Customization Options
- Five distinct color schemes to choose from
- Custom color combinations for:
  - Background
  - Grid lines
  - X's and O's
  - One-click application of color schemes

### Score Tracking
- Persistent score tracking across sessions
- Separate statistics for:
  - PVP mode wins/losses
  - PVAI mode with different difficulty levels
  - Scores saved automatically after each game
- Viewable statistics on difficulty selection screen

### User Interface
- Clean, modern design
- Responsive buttons and controls
- Clear visual feedback
- Easy navigation with "Back to Home" option
- Smooth transitions between screens

### Additional Features
- Game state preservation
- Automatic score saving
- Clear win/loss notifications
- Configurable player symbols
- AI move delay for better gameplay feel

## Controls
- Left mouse click to:
  - Place pieces
  - Select game modes
  - Choose color schemes
  - Navigate menus
- Back button available during gameplay

## Technical Details
- Built with Python and Pygame
- Implements minimax algorithm for AI
- Uses alpha-beta pruning for optimization
- Persistent storage for scores

## Game Flow
1. Start at home screen
2. Choose game mode (PVP or PVAI)
3. Select player symbol (X or O)
4. For PVAI, select difficulty
5. Play game with infinite mechanics
6. View results and scores
7. Return to home screen

## Requirements
- Python 3.x
- Pygame library
- Score tracking requires write permissions in game directory

## Setup
1. Ensure Python is installed
2. Install Pygame: `pip install pygame`
3. Run the game: `python main.py`

## File Structure
- `main.py` - Main game file
- `scores.txt` - Score tracking file

## Scoring System
The game automatically tracks and updates scores for:
- PVP Mode:
  - Player 1 wins
  - Player 2 wins
- PVAI Mode (per difficulty):
  - Player wins
  - AI wins

## Known Features
- Pieces cycle automatically after 3 moves per player
- Color schemes persist between sessions
- AI difficulty affects move calculation time
- Score tracking updates in real-time

## Tips
- In PVP mode, strategize around the 3-piece limit
- Against AI, consider the difficulty level's impact on strategy
- Use color schemes to reduce eye strain
- Watch for piece cycling to plan moves ahead

## Acknowledgments
Thanks to the Pygame community for providing an excellent library for game development.

Inspired by classic Tic Tac Toe and the concept of infinite gameplay.

Enjoy the game! If you have any questions or feedback, feel free to open an issue or contact me.


