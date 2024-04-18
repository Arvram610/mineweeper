import random
import pygame
import color


class Piece:
    EMPTY = 0
    BOMB = 1
    type = EMPTY

    def __init__(self):
        self.type = self.EMPTY
        self.flagged = False
        self.opened = False
        self.nearby = 0
        self.font = pygame.font.Font(pygame.font.get_default_font(), 40)

    def __repr__(self):
        if self.opened:
            return str(self.nearby)
        return " "

    def open(self) -> bool:
        """ Opens and returns if it is EMPTY """
        self.opened = True
        return self.type == self.EMPTY

    def flag(self):
        self.flagged = not self.flagged

    def draw(self):
        surface = pygame.Surface((100, 100))
        if self.opened:
            if self.type == self.BOMB:
                surface.fill(color.RED)
                text = self.font.render("B", True, color.BLACK)
                surface.blit(text, (50 - text.get_width() / 2, 50 - text.get_height() / 2))
            else:
                surface.fill(color.WHITE)
                if self.nearby != 0:
                    text = self.font.render(str(self.nearby), True, color.BLACK)
                    surface.blit(text, (50-text.get_width()/2, 50-text.get_height()/2))
        else:
            surface.fill(color.GRAY)
            if self.flagged:
                text = self.font.render("F", True, color.BLACK)
                surface.blit(text, (50 - text.get_width() / 2, 50 - text.get_height() / 2))

        return surface
            

class Board:
    def __init__(self, cols, rows, mines):
        # Build board
        self.board = [[Piece() for _ in range(cols)] for _ in range(rows)]
        self.dims = (cols, rows)

        # Place mines
        while mines != 0:
            piece = self.board[random.randint(0, rows-1)][random.randint(0, cols-1)]
            if piece.type == Piece.BOMB:
                continue
            piece.type = Piece.BOMB
            mines -= 1

        # Calculate nearby mines
        for pos_x in range(cols):
            for pos_y in range(rows):
                self.get_piece(pos_x, pos_y).nearby = self.calc_nearby(pos_x, pos_y)

    def get_piece(self, col, row) -> Piece:
        return self.board[row][col]

    def open(self, col, row) -> bool:
        """ Opens selected square and nearby squares
            Returns if game is running """
        piece = self.get_piece(col, row)
        if piece.opened or piece.flagged:
            return True
        if not piece.open():
            return False
        if piece.nearby == 0:
            for pos_xx in range(3):
                for pos_yy in range(3):
                    pos_x, pos_y = pos_xx + col - 1, pos_yy + row - 1
                    if 0 <= pos_x < self.dims[0] and 0 <= pos_y < self.dims[1]:
                        self.open(pos_x, pos_y)
        return True

    def flag(self, col, row):
        self.get_piece(col, row).flag()

    def calc_nearby(self, pos_x, pos_y):
        count = 0
        for pos_xx in range(3):
            for pos_yy in range(3):
                col, row = pos_xx+pos_x - 1, pos_yy+pos_y - 1
                if 0 <= col < self.dims[0] and 0 <= row < self.dims[1]:
                    if self.get_piece(col, row).type == Piece.BOMB:
                        count += 1
        return count
