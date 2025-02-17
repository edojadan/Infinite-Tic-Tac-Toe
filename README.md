# Infinite Tic Tac Toe
 An infinite tic tac toe game

 great game! 

Infinite Tic Tac Toe is a unique twist on the classic Tic Tac Toe game. Instead of a static 3x3 grid, the game features a sliding window of moves, where each player's oldest move disappears after they make their 4th move. This creates a dynamic and ever-changing board, adding a new layer of strategy to the game.

The game also includes:

A home screen with difficulty selection.

An adaptive AI that learns from your moves at the hardest difficulty.

A 2-second delay between the player's turn and the AI's turn for smoother gameplay.

## Table of Contents
- Features

+ Installation

+ How to Play

+ Difficulty Levels

+ Contributing

## Features
**Infinite Gameplay**: The board is constantly updated, with each player's oldest move disappearing after their 4th move.

**Difficulty Levels**: Choose from Easy, Medium, or Hard difficulty.

**Adaptive AI**: At the hardest difficulty, the AI learns from your moves and adapts its strategy.

**Win Screen**: When a player wins, a momentary screen displays the winner before returning to the home screen.

**Back to Home Button**: A button allows you to return to the home screen at any time.

## Installation
Prerequisites
- Python 3.x

+ Pygame library

Steps
Clone the Repository:

bash
Copy
git clone https://github.com/your-username/infinite-tic-tac-toe.git
cd infinite-tic-tac-toe
Install Pygame:
If you don't have Pygame installed, you can install it using pip:

bash
Copy
pip install pygame
Run the Game:

bash
Copy
python main.py

## How to Play
Home Screen:

When you start the game, you'll see the home screen with difficulty options.

Press 1 for Easy, 2 for Medium, or 3 for Hard.

Gameplay:

Click on the board to place your X.

The AI will place an O in response after a 2-second delay.

After each player makes their 4th move, their oldest move will disappear.

Winning:

The game checks for a win after each move.

If a player wins, a screen will display the winner for 3 seconds before returning to the home screen.

Back to Home:

Click the "Back to Home" button at any time to return to the home screen.

## Difficulty Levels
Easy:

The AI makes random moves.

Medium:

The AI mixes random moves with the Minimax algorithm.

Hard:

The AI uses the Minimax algorithm with Alpha-Beta pruning and **learns** from your moves.

## Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

Fork the repository.

Create a new branch for your feature or bugfix.

Commit your changes.

Push your branch to your forked repository.

Submit a pull request.

## Acknowledgments
Thanks to the Pygame community for providing an excellent library for game development.

Inspired by classic Tic Tac Toe and the concept of infinite gameplay.

Enjoy the game! If you have any questions or feedback, feel free to open an issue or contact me.


