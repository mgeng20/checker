from constants import *


class Board():
    '''
    A chess board
    '''

    def draw_board(self):
        noStroke()
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if (i % 2 == 0) == (j % 2 == 0):
                    fill(*LIGHT_COLOR)

                else:
                    fill(*DARK_COLOR)

                square(i*CELL_SIZE, j*CELL_SIZE, CELL_SIZE)
