from constants import *


CROWN_IMG = None


class Checker ():
    '''
    A single checker
    '''

    def __init__(self, color, board_coordinate, is_king=False, is_movable=False):
        """
        Constructor for a checker
        """
        self.color = color
        self.board_coordinate = board_coordinate
        self.is_king = is_king
        # is_movable will be in use for part 2, for part 1 the Checker object created has it as True
        self.is_movable = is_movable
        self.x = None
        self.y = None

    def draw_checker(self, being_dragged):
        # convert the given board coordinate into canvas coordinate
        self.x = self.board_coordinate[0]*CELL_SIZE+CELL_SIZE/2
        self.y = self.board_coordinate[1]*CELL_SIZE+CELL_SIZE/2

        # if the checker is captured by mouse, checker coordinate = mouse coordinate
        if being_dragged:
            self.x = mouseX
            self.y = mouseY

        # set different stroke weight for the outter circle depending on if checker can be captured
        if self.is_draggable() and self.color == BLACK:
            outter_stroke_weight = 4
        else:
            outter_stroke_weight = 2

        # draw shadow
        noStroke()
        fill(0, 60)
        circle(self.x+SHADOW_OFFSET, self.y+SHADOW_OFFSET, CHECKER_SIZE)
        # draw circle
        fill(*self.color)
        stroke(*WHITE)
        strokeWeight(outter_stroke_weight)
        circle(self.x, self.y, CHECKER_SIZE)
        strokeWeight(2)
        circle(self.x, self.y, CHECKER_SIZE*0.8)

        # load image when the checker is marked a king
        if self.is_king:
            global CROWN_IMG
            if CROWN_IMG is None:
                CROWN_IMG = loadImage("crown.png")
            image(CROWN_IMG, self.x, self.y, CHECKER_SIZE*0.6, CHECKER_SIZE*0.6)

    def is_draggable(self):
        # determine if the checker can be captured by mouse
        return dist(self.x, self.y, mouseX, mouseY) < CHECKER_SIZE / 2 and self.is_movable
