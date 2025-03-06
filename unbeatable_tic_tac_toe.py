import sys
import pygame
import numpy as np

pygame.init()

# Colors
WHITE = (255, 255, 255)
GREY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Sizes
WIDTH = 600
HEIGHT = 600
LINE_W = 5
BOARD_Rows = 3
BOARD_Columns = 3
square_size = WIDTH // BOARD_Columns
circle_radius = square_size // 3
circle_width = 10
cross_width = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe AI')
screen.fill(BLACK)

board = np.zeros((BOARD_Rows, BOARD_Columns))

def draw_lines(color=WHITE):
    for i in range(1, BOARD_Rows):
        pygame.draw.line(screen, color, (0, square_size * i), (WIDTH, square_size * i), LINE_W)
        pygame.draw.line(screen, color, (square_size * i, 0), (square_size * i, HEIGHT), LINE_W)

def draw_figures(color=WHITE):
    for row in range(BOARD_Rows):
        for col in range(BOARD_Columns):
            if board[row][col] == 1:
                pygame.draw.circle(screen, color,
                                   (int(col * square_size + square_size // 2), int(row * square_size + square_size // 2)),
                                   circle_radius, width=circle_width)
            elif board[row][col] == 2:
                pygame.draw.line(screen, color,
                                 (col * square_size + square_size // 4, row * square_size + square_size // 4),
                                 (col * square_size + 3 * square_size // 4, row * square_size + 3 * square_size // 4),
                                 cross_width)
                pygame.draw.line(screen, color,
                                 (col * square_size + square_size // 4, row * square_size + 3 * square_size // 4),
                                 (col * square_size + 3 * square_size // 4, row * square_size + square_size // 4),
                                 cross_width)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] == 0

def is_board_full(check_board=board):
    for row in range(BOARD_Rows):
        for col in range(BOARD_Columns):
            if check_board[row][col] == 0:
                return False
    return True

def check_win(player, check_board=board):
    for col in range(BOARD_Columns):
        if check_board[0][col] == player and check_board[1][col] == player and check_board[2][col] == player:
            return True

    for row in range(BOARD_Rows):
        if check_board[row][0] == player and check_board[row][1] == player and check_board[row][2] == player:
            return True

    if check_board[0][0] == player and check_board[1][1] == player and check_board[2][2] == player:
        return True

    if check_board[0][2] == player and check_board[1][1] == player and check_board[2][0] == player:
        return True

    return False

def minimax(minimax_board, depth, is_maximising):
    if check_win(2, minimax_board):  # AI wins (Player 2)
        return float('inf')
    elif check_win(1, minimax_board):  # Player 1 (X) wins
        return float('-inf')
    elif is_board_full(minimax_board):
        return 0

    if is_maximising:
        best_score = -1000
        for row in range(BOARD_Rows):
            for column in range(BOARD_Columns):
                if minimax_board[row][column] == 0:
                    minimax_board[row][column] = 2  # AI's turn (O)
                    score = minimax(minimax_board, depth + 1, False)
                    minimax_board[row][column] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = 1000
        for row in range(BOARD_Rows):
            for column in range(BOARD_Columns):
                if minimax_board[row][column] == 0:
                    minimax_board[row][column] = 1  # Player's turn (X)
                    score = minimax(minimax_board, depth + 1, True)
                    minimax_board[row][column] = 0
                    best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -1000
    move = (-1, -1)
    for row in range(BOARD_Rows):
        for col in range(BOARD_Columns):
            if board[row][col] == 0:
                board[row][col] = 2  # AI's move (O)
                score = minimax(board, depth=0, is_maximising=False)
                board[row][col] = 0
                if score > best_score:
                    best_score = score
                    move = (row, col)

    if move != (-1, -1):
        mark_square(move[0], move[1], 2)  # Mark AI's move
        return True
    return False

def restart_game():
    screen.fill(BLACK)
    draw_lines()
    board.fill(0)

draw_lines()

player = 1  # Player 1 (X) starts first
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0] // square_size
            mouseY = event.pos[1] // square_size

            if available_square(mouseY, mouseX):
                mark_square(mouseY, mouseX, player)  # Player makes their move
                if check_win(player):
                    game_over = True
                player = player % 2 + 1  # Switch between player 1 (X) and player 2 (O)

                if not game_over:
                    if best_move():  # AI (O) makes its move
                        if check_win(2):  # Check if AI wins
                            game_over = True
                        player = player % 2 + 1  # Switch between player 1 (X) and player 2 (O)

                if not game_over:
                    if is_board_full():
                        game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()
                game_over = False
                player = 1  # Start with Player 1 (X) again

    if not game_over:
        draw_figures()
    else:
        if check_win(1):  # Player 1 (X) wins
            draw_figures(GREEN)
            draw_lines(GREEN)
        elif check_win(2):  # Player 2 (O) wins
            draw_figures(RED)
            draw_lines(RED)
        else:
            draw_figures(YELLOW)
            draw_lines(YELLOW)

    pygame.display.update()
