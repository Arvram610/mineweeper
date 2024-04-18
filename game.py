import pygame
import color

from board import Board, Piece

ROWS = 10
COLS = 10
MINES = 10

WIDTH, HEIGHT = 500, 500


class Game:
    def __init__(self):
        self.board = Board(rows=ROWS, cols=COLS, mines=MINES)
        self.started = False

    def restart(self):
        self.__init__()

    def open(self, col, row):
        self.started = True
        return self.board.open(row, col)

    def flag(self, col, row):
        self.board.flag(row, col)

    def get_piece(self, col, row) -> Piece:
        return self.board.get_piece(row, col)

    def debug_print(self):
        for i in self.board.board:
            print(i)


class Window:
    def __init__(self, game):
        self.game_on = False
        self.is_pressed = [False, False, False]
        self.running = False
        self.square_size_y = HEIGHT/ROWS
        self.square_size_x = WIDTH/COLS
        self.game = game
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

    def draw(self):
        def draw_lines():
            for row in range(ROWS + 1):
                pygame.draw.line(self.screen, color.BLACK,
                                 (0, self.square_size_y * row - 1),
                                 (width, self.square_size_y * row - 1),
                                 2)
            for col in range(ROWS + 1):
                pygame.draw.line(self.screen, color.BLACK,
                                 (self.square_size_x * col - 1, 0),
                                 (self.square_size_x * col - 1, height),
                                 2)

        def draw_squares():
            for row in range(ROWS):
                for col in range(COLS):
                    surface = self.game.get_piece(col, row).draw()
                    surface = pygame.transform.scale(surface, (self.square_size_x, self.square_size_y))
                    self.screen.blit(surface, (col*self.square_size_x, row*self.square_size_y))

        self.screen.fill(color.GRAY)
        width, height = pygame.display.get_window_size()
        self.square_size_x = width/COLS
        self.square_size_y = width/ROWS

        draw_squares()
        draw_lines()

        pygame.display.flip()

    def run(self):
        self.running = True
        self.game_on = True
        while self.running:
            self.events()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        if not self.game_on:
            return
        pressed = pygame.mouse.get_pressed(3)
        if pressed[0] or pressed[2]:
            if pressed[0] and not self.is_pressed[0]:
                x, y = pygame.mouse.get_pos()
                x, y = int(x//self.square_size_x), int(y//self.square_size_y)
                self.open(x, y)
                self.is_pressed[0] = True
            if pressed[2] and not self.is_pressed[2]:
                x, y = pygame.mouse.get_pos()
                x, y = int(x//self.square_size_x), int(y//self.square_size_y)
                self.game.flag(x, y)
                self.is_pressed[2] = True
        self.is_pressed = list(pressed)

    def open(self, col, row):
        if not self.game.started:
            while 1:
                piece = self.game.get_piece(col, row)
                if not (piece.type == Piece.BOMB or piece.nearby != 0):
                    break
                self.game.restart()

        self.game_on = self.game.open(col, row)




if __name__ == "__main__":
    if not pygame.get_init():
        pygame.init()
    game = Game()
    w = Window(game)
    w.run()