import pygame
import sys
import random
import math
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 15
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = SQUARE_SIZE // 4
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)
BUTTON_COLOR = (100, 100, 100)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Infinite Tic Tac Toe")
screen.fill(BG_COLOR)

# Board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Move history: stores (row, col, symbol)
player_moves = []  # Moves by the player (X)
ai_moves = []      # Moves by the AI (O)

# Fonts
font = pygame.font.SysFont(None, 55)
button_font = pygame.font.SysFont(None, 40)

# Difficulty
difficulty = "easy"

# AI Memory
ai_memory = {}

# Home Screen
def home_screen():
    screen.fill(BG_COLOR)
    title = font.render("Infinite Tic Tac Toe", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    
    easy_text = font.render("1 - Easy", True, (255, 255, 255))
    medium_text = font.render("2 - Medium", True, (255, 255, 255))
    hard_text = font.render("3 - Hard", True, (255, 255, 255))
    
    screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, HEIGHT // 2))
    screen.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, HEIGHT // 2 + 60))
    screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, HEIGHT // 2 + 120))
    
    pygame.display.update()

# Draw Lines
def draw_lines():
    # Horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Draw Figures
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)

# Update Board (Sliding Window per Player)
def update_board():
    global board, player_moves, ai_moves
    # Remove oldest move for player (X) if they have more than 3 moves
    if len(player_moves) > 3:
        old_row, old_col, _ = player_moves.pop(0)
        board[old_row][old_col] = None
    # Remove oldest move for AI (O) if they have more than 3 moves
    if len(ai_moves) > 3:
        old_row, old_col, _ = ai_moves.pop(0)
        board[old_row][old_col] = None
    # Rebuild the board
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    for move in player_moves:
        row, col, symbol = move
        board[row][col] = symbol
    for move in ai_moves:
        row, col, symbol = move
        board[row][col] = symbol
    # Redraw the board
    screen.fill(BG_COLOR)
    draw_lines()
    draw_figures()
    pygame.display.update()

# Check Win
def check_win(player):
    # Check rows
    for row in range(BOARD_ROWS):
        if all([cell == player for cell in board[row]]):
            return True
    # Check columns
    for col in range(BOARD_COLS):
        if all([board[row][col] == player for row in range(BOARD_ROWS)]):
            return True
    # Check diagonals
    if all([board[i][i] == player for i in range(BOARD_ROWS)]):
        return True
    if all([board[i][BOARD_COLS - i - 1] == player for i in range(BOARD_ROWS)]):
        return True
    return False

# Show Win Screen
def show_win_screen(winner):
    screen.fill(BG_COLOR)
    win_text = font.render(f"{winner} wins!", True, (255, 255, 255))
    screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    time.sleep(3)  # Display for 3 seconds
    main()  # Return to home screen

# Minimax Algorithm
def minimax(board, depth, is_maximizing, alpha, beta):
    if check_win('X'):
        return -10 + depth, None
    elif check_win('O'):
        return 10 - depth, None
    elif all([cell is not None for row in board for cell in row]):
        return 0, None

    if is_maximizing:
        best_score = -math.inf
        best_move = None
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] is None:
                    board[row][col] = 'O'
                    score, _ = minimax(board, depth + 1, False, alpha, beta)
                    board[row][col] = None
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break
        return best_score, best_move
    else:
        best_score = math.inf
        best_move = None
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] is None:
                    board[row][col] = 'X'
                    score, _ = minimax(board, depth + 1, True, alpha, beta)
                    board[row][col] = None
                    if score < best_score:
                        best_score = score
                        best_move = (row, col)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break
        return best_score, best_move

# AI Move
def ai_move():
    global difficulty, ai_memory

    if difficulty == "easy":
        # Random move
        available_moves = [(row, col) for row in range(BOARD_ROWS) for col in range(BOARD_COLS) if board[row][col] is None]
        return random.choice(available_moves)
    elif difficulty == "medium":
        # Mix of random and minimax
        if random.random() < 0.5:
            available_moves = [(row, col) for row in range(BOARD_ROWS) for col in range(BOARD_COLS) if board[row][col] is None]
            return random.choice(available_moves)
        else:
            _, move = minimax(board, 0, True, -math.inf, math.inf)
            return move
    elif difficulty == "hard":
        # Minimax with memory
        board_state = tuple(tuple(row) for row in board)
        if board_state in ai_memory:
            return ai_memory[board_state]
        else:
            _, move = minimax(board, 0, True, -math.inf, math.inf)
            ai_memory[board_state] = move
            return move

# Reset Game
def reset_game():
    global board, player_moves, ai_moves
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    player_moves = []
    ai_moves = []
    screen.fill(BG_COLOR)
    draw_lines()
    pygame.display.update()

# Draw Back Button
def draw_back_button():
    button_rect = pygame.Rect(WIDTH - 150, HEIGHT - 50, 140, 40)
    pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
    back_text = button_font.render("Back to Home", True, BUTTON_TEXT_COLOR)
    screen.blit(back_text, (WIDTH - 140, HEIGHT - 45))
    return button_rect

# Main Game Loop
def main():
    global difficulty

    home_screen()
    selecting_difficulty = True
    while selecting_difficulty:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    difficulty = "easy"
                    selecting_difficulty = False
                elif event.key == pygame.K_2:
                    difficulty = "medium"
                    selecting_difficulty = False
                elif event.key == pygame.K_3:
                    difficulty = "hard"
                    selecting_difficulty = False

    reset_game()
    player_turn = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos

                # Check if Back button is clicked
                back_button_rect = draw_back_button()
                if back_button_rect.collidepoint(mouseX, mouseY):
                    main()  # Return to home screen

                if player_turn:
                    mouseX = mouseX // SQUARE_SIZE
                    mouseY = mouseY // SQUARE_SIZE

                    if board[mouseY][mouseX] is None:
                        board[mouseY][mouseX] = 'X'
                        player_moves.append((mouseY, mouseX, 'X'))
                        player_turn = False
                        update_board()

                        if check_win('X'):
                            show_win_screen("Player")
                        else:
                            # Add a 2-second delay before AI's turn
                            time.sleep(2)
                            ai_move_result = ai_move()
                            if ai_move_result:
                                row, col = ai_move_result
                                board[row][col] = 'O'
                                ai_moves.append((row, col, 'O'))
                                player_turn = True
                                update_board()

                                if check_win('O'):
                                    show_win_screen("AI")

        # Draw the back button
        draw_back_button()
        pygame.display.update()

if __name__ == "__main__":
    main()