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
player_moves = []  # Moves by the player (X or O)
ai_moves = []      # Moves by the AI (O or X)

# Fonts
font = pygame.font.SysFont(None, 55)
button_font = pygame.font.SysFont(None, 40)

# Game State
game_mode = None  # "PVP" or "PVAI"
player_symbol = None  # "X" or "O"
difficulty = None  # "easy", "medium", "hard"

# Score Tracking
scores = {
    "PVAI": {"Easy": {"Wins": 0, "Losses": 0},
             "Medium": {"Wins": 0, "Losses": 0},
             "Hard": {"Wins": 0, "Losses": 0}},
    "PVP": {"Wins": 0, "Losses": 0}
}

# Load Scores from File
def load_scores():
    try:
        with open("scores.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()  # Remove leading/trailing whitespace
                if "Player vs AI:" in line:
                    continue
                elif "Easy:" in line:
                    scores["PVAI"]["Easy"]["Wins"] = int(line.split("Wins=")[1].split(",")[0])
                    scores["PVAI"]["Easy"]["Losses"] = int(line.split("Losses=")[1])
                elif "Medium:" in line:
                    scores["PVAI"]["Medium"]["Wins"] = int(line.split("Wins=")[1].split(",")[0])
                    scores["PVAI"]["Medium"]["Losses"] = int(line.split("Losses=")[1])
                elif "Hard:" in line:
                    scores["PVAI"]["Hard"]["Wins"] = int(line.split("Wins=")[1].split(",")[0])
                    scores["PVAI"]["Hard"]["Losses"] = int(line.split("Losses=")[1])
                elif "Player vs Player:" in line:
                    # Ensure the line has the correct format
                    if "Wins=" in line and "Losses=" in line:
                        scores["PVP"]["Wins"] = int(line.split("Wins=")[1].split(",")[0])
                        scores["PVP"]["Losses"] = int(line.split("Losses=")[1])
    except FileNotFoundError:
        # If the file doesn't exist, initialize with default scores
        with open("scores.txt", "w") as file:
            file.write("Player vs AI:\n")
            file.write("Easy: Wins=0, Losses=0\n")
            file.write("Medium: Wins=0, Losses=0\n")
            file.write("Hard: Wins=0, Losses=0\n")
            file.write("Player vs Player:\n")
            file.write("Wins=0, Losses=0\n")
    except Exception as e:
        print(f"Error loading scores: {e}")
        # If there's an error, reset the scores to default
        scores["PVAI"]["Easy"]["Wins"] = 0
        scores["PVAI"]["Easy"]["Losses"] = 0
        scores["PVAI"]["Medium"]["Wins"] = 0
        scores["PVAI"]["Medium"]["Losses"] = 0
        scores["PVAI"]["Hard"]["Wins"] = 0
        scores["PVAI"]["Hard"]["Losses"] = 0
        scores["PVP"]["Wins"] = 0
        scores["PVP"]["Losses"] = 0

# Save Scores to File
def save_scores():
    with open("scores.txt", "w") as file:
        file.write("Player vs AI:\n")
        file.write(f"Easy: Wins={scores['PVAI']['Easy']['Wins']}, Losses={scores['PVAI']['Easy']['Losses']}\n")
        file.write(f"Medium: Wins={scores['PVAI']['Medium']['Wins']}, Losses={scores['PVAI']['Medium']['Losses']}\n")
        file.write(f"Hard: Wins={scores['PVAI']['Hard']['Wins']}, Losses={scores['PVAI']['Hard']['Losses']}\n")
        file.write("Player vs Player:\n")
        file.write(f"Wins={scores['PVP']['Wins']}, Losses={scores['PVP']['Losses']}\n")

# Home Screen
def home_screen():
    screen.fill(BG_COLOR)  # Use the current BG_COLOR
    title = font.render("Infinite Tic Tac Toe", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    
    pvp_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
    pvai_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
    colour_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50)
    
    pygame.draw.rect(screen, BUTTON_COLOR, pvp_button)
    pygame.draw.rect(screen, BUTTON_COLOR, pvai_button)
    pygame.draw.rect(screen, BUTTON_COLOR, colour_button)
    
    pvp_text = button_font.render("Player vs Player", True, BUTTON_TEXT_COLOR)
    pvai_text = button_font.render("Player vs AI", True, BUTTON_TEXT_COLOR)
    colour_text = button_font.render("Colour Scheme", True, BUTTON_TEXT_COLOR)
    
    screen.blit(pvp_text, (WIDTH // 2 - pvp_text.get_width() // 2, HEIGHT // 2 - 35))
    screen.blit(pvai_text, (WIDTH // 2 - pvai_text.get_width() // 2, HEIGHT // 2 + 65))
    screen.blit(colour_text, (WIDTH // 2 - colour_text.get_width() // 2, HEIGHT // 2 + 165))
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                if pvp_button.collidepoint(mouseX, mouseY):
                    return "PVP"
                elif pvai_button.collidepoint(mouseX, mouseY):
                    return "PVAI"
                elif colour_button.collidepoint(mouseX, mouseY):
                    colour_scheme_screen()
                    return home_screen()  # Restart home screen after returning from color scheme

# Colour Scheme Selection Screen
def colour_scheme_screen():
    global BG_COLOR, LINE_COLOR, CIRCLE_COLOR, CROSS_COLOR

    # Define 5 colour schemes
    schemes = [
        {"BG_COLOR": (28, 170, 156), "LINE_COLOR": (23, 145, 135), "CIRCLE_COLOR": (239, 231, 200), "CROSS_COLOR": (66, 66, 66)},
        {"BG_COLOR": (173, 216, 230), "LINE_COLOR": (135, 206, 250), "CIRCLE_COLOR": (255, 182, 193), "CROSS_COLOR": (255, 105, 180)},
        {"BG_COLOR": (144, 238, 144), "LINE_COLOR": (50, 205, 50), "CIRCLE_COLOR": (255, 255, 0), "CROSS_COLOR": (255, 140, 0)},
        {"BG_COLOR": (240, 230, 140), "LINE_COLOR": (210, 180, 140), "CIRCLE_COLOR": (255, 215, 0), "CROSS_COLOR": (139, 69, 19)},
        {"BG_COLOR": (221, 160, 221), "LINE_COLOR": (186, 85, 211), "CIRCLE_COLOR": (147, 112, 219), "CROSS_COLOR": (75, 0, 130)}
    ]
    
    screen.fill(BG_COLOR)
    title = font.render("Select Colour Scheme", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    
    buttons = []
    for i in range(5):
        button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 100 + i * 60, 200, 50)
        buttons.append(button)
        pygame.draw.rect(screen, schemes[i]["BG_COLOR"], button)
        scheme_text = button_font.render(f"Scheme {i+1}", True, BUTTON_TEXT_COLOR)
        screen.blit(scheme_text, (WIDTH // 2 - scheme_text.get_width() // 2, HEIGHT // 2 - 85 + i * 60))
    
    # Add "Back to Home" button
    back_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 70, 200, 50)
    pygame.draw.rect(screen, BUTTON_COLOR, back_button)
    back_text = button_font.render("Back to Home", True, BUTTON_TEXT_COLOR)
    screen.blit(back_text, (WIDTH // 2 - back_text.get_width() // 2, HEIGHT - 55))
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                for i in range(5):
                    if buttons[i].collidepoint(mouseX, mouseY):
                        # Update global colour variables
                        BG_COLOR = schemes[i]["BG_COLOR"]
                        LINE_COLOR = schemes[i]["LINE_COLOR"]
                        CIRCLE_COLOR = schemes[i]["CIRCLE_COLOR"]
                        CROSS_COLOR = schemes[i]["CROSS_COLOR"]
                        home_screen()  # Return to home screen immediately after selection
                        return
                if back_button.collidepoint(mouseX, mouseY):
                    home_screen()  # Call home_screen before returning
                    return

# Symbol Selection Screen
def symbol_selection_screen():
    screen.fill(BG_COLOR)
    title = font.render("Player 1: Choose Your Symbol", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    
    x_button = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 50, 100, 100)
    o_button = pygame.Rect(WIDTH // 2 + 50, HEIGHT // 2 - 50, 100, 100)
    
    pygame.draw.rect(screen, BUTTON_COLOR, x_button)
    pygame.draw.rect(screen, BUTTON_COLOR, o_button)
    
    x_text = button_font.render("X", True, BUTTON_TEXT_COLOR)
    o_text = button_font.render("O", True, BUTTON_TEXT_COLOR)
    
    screen.blit(x_text, (WIDTH // 2 - 120, HEIGHT // 2 - 15))
    screen.blit(o_text, (WIDTH // 2 + 80, HEIGHT // 2 - 15))
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                if x_button.collidepoint(mouseX, mouseY):
                    return "X"
                elif o_button.collidepoint(mouseX, mouseY):
                    return "O"

# Difficulty Selection Screen
def difficulty_selection_screen():
    screen.fill(BG_COLOR)
    title = font.render("Select Difficulty", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    
    easy_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 100, 200, 50)
    medium_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    hard_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)
    
    pygame.draw.rect(screen, BUTTON_COLOR, easy_button)
    pygame.draw.rect(screen, BUTTON_COLOR, medium_button)
    pygame.draw.rect(screen, BUTTON_COLOR, hard_button)
    
    easy_text = button_font.render(f"Easy (W: {scores['PVAI']['Easy']['Wins']}, L: {scores['PVAI']['Easy']['Losses']})", True, BUTTON_TEXT_COLOR)
    medium_text = button_font.render(f"Medium (W: {scores['PVAI']['Medium']['Wins']}, L: {scores['PVAI']['Medium']['Losses']})", True, BUTTON_TEXT_COLOR)
    hard_text = button_font.render(f"Hard (W: {scores['PVAI']['Hard']['Wins']}, L: {scores['PVAI']['Hard']['Losses']})", True, BUTTON_TEXT_COLOR)
    
    screen.blit(easy_text, (WIDTH // 2 - easy_text.get_width() // 2, HEIGHT // 2 - 85))
    screen.blit(medium_text, (WIDTH // 2 - medium_text.get_width() // 2, HEIGHT // 2 + 15))
    screen.blit(hard_text, (WIDTH // 2 - hard_text.get_width() // 2, HEIGHT // 2 + 115))
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                if easy_button.collidepoint(mouseX, mouseY):
                    return "easy"
                elif medium_button.collidepoint(mouseX, mouseY):
                    return "medium"
                elif hard_button.collidepoint(mouseX, mouseY):
                    return "hard"

# Player vs Player Start Screen
def pvp_start_screen(player_symbol):
    screen.fill(BG_COLOR)
    title = font.render("Player vs Player", True, (255, 255, 255))
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 4))
    
    player1_text = button_font.render(f"Player 1: {player_symbol}", True, BUTTON_TEXT_COLOR)
    player2_text = button_font.render(f"Player 2: {'O' if player_symbol == 'X' else 'X'}", True, BUTTON_TEXT_COLOR)
    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 100, 200, 50)
    
    screen.blit(player1_text, (WIDTH // 2 - player1_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(player2_text, (WIDTH // 2 - player2_text.get_width() // 2, HEIGHT // 2))
    pygame.draw.rect(screen, BUTTON_COLOR, start_button)
    start_text = button_font.render("Start Game", True, BUTTON_TEXT_COLOR)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 115))
    
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos
                if start_button.collidepoint(mouseX, mouseY):
                    return  # Exit the function and start the game
                

# Difficulty
difficulty = "easy"

# AI Memory
ai_memory = {}

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
    global scores, game_mode, difficulty

    screen.fill(BG_COLOR)
    win_text = font.render(f"{winner} wins!", True, (255, 255, 255))
    screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()

    # Update scores based on game mode and winner
    if game_mode == "PVAI":
        if winner == "Player":
            scores["PVAI"][difficulty.capitalize()]["Wins"] += 1
        elif winner == "AI":
            scores["PVAI"][difficulty.capitalize()]["Losses"] += 1
    elif game_mode == "PVP":
        if winner == "Player 1":
            scores["PVP"]["Wins"] += 1
        elif winner == "Player 2":
            scores["PVP"]["Losses"] += 1

    # Save updated scores to file
    save_scores()
    
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

# Game Loop for Player vs AI
def pvai_game_loop():
    global player_moves, ai_moves, difficulty, player_symbol

    reset_game()
    player_turn = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_scores()  # Save scores before quitting
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos

                # Check if Back button is clicked
                back_button_rect = draw_back_button()
                if back_button_rect.collidepoint(mouseX, mouseY):
                    save_scores()  # Save scores before returning to home screen
                    return

                if player_turn:
                    mouseX = mouseX // SQUARE_SIZE
                    mouseY = mouseY // SQUARE_SIZE

                    if board[mouseY][mouseX] is None:
                        board[mouseY][mouseX] = player_symbol
                        player_moves.append((mouseY, mouseX, player_symbol))
                        player_turn = False
                        update_board()

                        if check_win(player_symbol):
                            show_win_screen("Player")
                            return
                        else:
                            # Add a 2-second delay before AI's turn
                            time.sleep(2)
                            ai_move_result = ai_move()
                            if ai_move_result:
                                row, col = ai_move_result
                                board[row][col] = 'O' if player_symbol == 'X' else 'X'
                                ai_moves.append((row, col, 'O' if player_symbol == 'X' else 'X'))
                                player_turn = True
                                update_board()

                                if check_win('O' if player_symbol == 'X' else 'X'):
                                    show_win_screen("AI")
                                    return

        # Draw the back button
        draw_back_button()
        pygame.display.update()

# Game Loop for Player vs Player
def pvp_game_loop():
    global player_moves, ai_moves, player_symbol
    
    # Initialize separate move lists for each player
    player1_moves = []  # For tracking Player 1's moves
    player2_moves = []  # For tracking Player 2's moves
    current_player = "Player 1"

    reset_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_scores()
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = event.pos

                # Check if Back button is clicked
                back_button_rect = draw_back_button()
                if back_button_rect.collidepoint(mouseX, mouseY):
                    save_scores()
                    return

                mouseX = mouseX // SQUARE_SIZE
                mouseY = mouseY // SQUARE_SIZE

                if board[mouseY][mouseX] is None:
                    board[mouseY][mouseX] = player_symbol
                    
                    # Add move to appropriate player's list
                    if current_player == "Player 1":
                        player1_moves.append((mouseY, mouseX, player_symbol))
                        # Remove oldest move if player has more than 3 moves
                        if len(player1_moves) > 3:
                            old_row, old_col, _ = player1_moves.pop(0)
                            # Only clear the cell if it belongs to Player 1
                            if board[old_row][old_col] == player_symbol:
                                board[old_row][old_col] = None
                    else:
                        player2_moves.append((mouseY, mouseX, player_symbol))
                        # Remove oldest move if player has more than 3 moves
                        if len(player2_moves) > 3:
                            old_row, old_col, _ = player2_moves.pop(0)
                            # Only clear the cell if it belongs to Player 2
                            if board[old_row][old_col] == player_symbol:
                                board[old_row][old_col] = None

                    # Redraw the board with all current moves
                    screen.fill(BG_COLOR)
                    draw_lines()
                    
                    # Redraw all pieces from both players' moves
                    for move in player1_moves:
                        row, col, symbol = move
                        board[row][col] = symbol
                    for move in player2_moves:
                        row, col, symbol = move
                        board[row][col] = symbol
                    
                    draw_figures()
                    pygame.display.update()

                    if check_win(player_symbol):
                        show_win_screen(current_player)
                        return
                    else:
                        # Switch players
                        player_symbol = 'O' if player_symbol == 'X' else 'X'
                        current_player = "Player 2" if current_player == "Player 1" else "Player 1"

        # Draw the back button
        draw_back_button()
        pygame.display.update()

# Main Function
def main():
    global game_mode, player_symbol, difficulty

    # Load scores at the start
    load_scores()
    
    while True:
        game_mode = home_screen()
        player_symbol = symbol_selection_screen()
        
        if game_mode == "PVAI":
            difficulty = difficulty_selection_screen()
            pvai_game_loop()
        elif game_mode == "PVP":
            pvp_start_screen(player_symbol)
            pvp_game_loop()
        
        # Save scores before resetting the board
        save_scores()
        
        # Reset the board and move history
        board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
        player_moves = []
        ai_moves = []

if __name__ == "__main__":
    main()