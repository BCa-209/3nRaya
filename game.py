import pygame
import sys
import copy

# -----------------------------
# CONFIGURACIONES
# -----------------------------
WIDTH, HEIGHT = 600, 600
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
CIRCLE_COLOR = (242, 85, 96)
CROSS_COLOR = (28, 170, 156)
LINE_WIDTH = 15
MARK_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tres en Raya')
screen.fill(BG_COLOR)

# -----------------------------
# TABLERO
# -----------------------------
class TicTacToe:
    def __init__(self):
        self.board = [[None]*BOARD_COLS for _ in range(BOARD_ROWS)]
        self.current_player = 'X'  # X siempre empieza

    # Devuelve el jugador actual
    def player(self):
        return self.current_player

    # Devuelve las acciones posibles: lista de (fila, col)
    def actions(self):
        return [(r, c) for r in range(BOARD_ROWS)
                        for c in range(BOARD_COLS)
                        if self.board[r][c] is None]

    # Aplica acción y devuelve nuevo estado
    def result(self, action):
        r, c = action
        new_state = copy.deepcopy(self)
        new_state.board[r][c] = self.current_player
        new_state.current_player = 'O' if self.current_player == 'X' else 'X'
        return new_state

    # Verifica si el juego terminó
    def terminal(self):
        return self.winner() is not None or all(
            self.board[r][c] is not None for r in range(BOARD_ROWS) for c in range(BOARD_COLS)
        )

    # Devuelve utilidad: 1 si X gana, -1 si O gana, 0 empate
    def utility(self):
        win = self.winner()
        if win == 'X':
            return 1
        elif win == 'O':
            return -1
        else:
            return 0

    # Comprueba si hay un ganador
    def winner(self):
        # Filas y columnas
        for i in range(BOARD_ROWS):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0]:
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i]:
                return self.board[0][i]
        # Diagonales
        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0]:
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2]:
            return self.board[0][2]
        return None

# -----------------------------
# MINIMAX
# -----------------------------
def minimax(state):
    if state.terminal():
        return None, state.utility()

    if state.player() == 'X':
        best_value = -float('inf')
        best_action = None
        for action in state.actions():
            _, value = minimax(state.result(action))
            if value > best_value:
                best_value = value
                best_action = action
        return best_action, best_value
    else:
        best_value = float('inf')
        best_action = None
        for action in state.actions():
            _, value = minimax(state.result(action))
            if value < best_value:
                best_value = value
                best_action = action
        return best_action, best_value

# -----------------------------
# DIBUJAR TABLERO
# -----------------------------
def draw_lines():
    # Horizontales
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE*i), (WIDTH, SQUARE_SIZE*i), LINE_WIDTH)
    # Verticales
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE*i, 0), (SQUARE_SIZE*i, HEIGHT), LINE_WIDTH)

def draw_marks(board):
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if board[r][c] == 'X':
                pygame.draw.line(screen, CROSS_COLOR,
                                 (c*SQUARE_SIZE + 20, r*SQUARE_SIZE + 20),
                                 ((c+1)*SQUARE_SIZE - 20, (r+1)*SQUARE_SIZE - 20), MARK_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR,
                                 (c*SQUARE_SIZE + 20, (r+1)*SQUARE_SIZE - 20),
                                 ((c+1)*SQUARE_SIZE - 20, r*SQUARE_SIZE + 20), MARK_WIDTH)
            elif board[r][c] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR,
                                   (c*SQUARE_SIZE + SQUARE_SIZE//2, r*SQUARE_SIZE + SQUARE_SIZE//2),
                                   SQUARE_SIZE//2 - 20, MARK_WIDTH)

# -----------------------------
# JUEGO PRINCIPAL
# -----------------------------
game = TicTacToe()
draw_lines()
pygame.display.update()

ai_player = 'O'

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and game.player() != ai_player:
            mouseX, mouseY = event.pos
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE
            if game.board[clicked_row][clicked_col] is None:
                game.board[clicked_row][clicked_col] = game.player()
                game.current_player = 'O' if game.current_player == 'X' else 'X'

        # Turno de la IA
        if game.player() == ai_player and not game.terminal():
            action, _ = minimax(game)
            if action:
                r, c = action
                game.board[r][c] = ai_player
                game.current_player = 'X'

    draw_marks(game.board)
    pygame.display.update()

    # Revisar si termina el juego
    if game.terminal():
        print("Juego terminado!")
        if game.winner():
            print("Ganador:", game.winner())
        else:
            print("Empate")
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()