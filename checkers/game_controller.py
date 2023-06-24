import random
from board import Board
from constants import *
from checker import Checker


class GameController:
    """
    A controller for the game of Checkers
    """

    def __init__(self):
        """
        Constructor for game controller
        """
        board_x = [0, 1, 2, 3, 4, 5, 6, 7]
        board_y = [0, 1, 2, 5, 6, 7]

        self.ai_checkers = [Checker(RED, (x, y), False, False)
                            for y in board_y if y < 3
                            for x in board_x if (x+y) % 2 == 1]
        self.player_checkers = [Checker(BLACK, (x, y), False, False)
                                for y in board_y if y > 4
                                for x in board_x if (x+y) % 2 == 1]

        self.the_dragging_checker = None
        self.board = Board()
        self.update_movables()
        self.ai_countdown = 0
        self.normal_moves = 0
        self.game_over = False
        self.pop_up_countdown = 0
        self.score_to_add = 0
        print("Player's turn")

    def draw(self):

        if self.ai_countdown > 0:
            self.ai_countdown -= 1
            if self.ai_countdown == 0:
                self.ai_move()
        # draw the board and checkers
        self.board.draw_board()
        for c in self.ai_checkers:
            c.draw_checker(c == self.the_dragging_checker)
        for c in self.player_checkers:
            c.draw_checker(c == self.the_dragging_checker)
        if self.game_over:
            self.end_game()
            if self.pop_up_countdown > 0:
                self.pop_up_countdown -= 1
                if self.pop_up_countdown == 0:
                    self.update_score(self.score_to_add)

    def mousePressed(self):
        if self.ai_countdown > 0:
            return
        # drag a checker
        for c in self.player_checkers:
            if c.is_draggable():
                self.the_dragging_checker = c
        # make the checker on the top layer and over other checkers
        if self.the_dragging_checker != None:
            if self.the_dragging_checker.color == BLACK:
                self.player_checkers.remove(self.the_dragging_checker)
                self.player_checkers.append(self.the_dragging_checker)
            else:
                self.ai_checkers.remove(self.the_dragging_checker)
                self.ai_checkers.append(self.the_dragging_checker)

    def mouseReleased(self):
        if self.the_dragging_checker == None:
            return
        # convert mouse coordinate
        mouse_board_coordinate = (mouseX//CELL_SIZE, mouseY//CELL_SIZE)
        # determine legal spots
        for coordinate, captured in self.find_legal_moves(self.the_dragging_checker):
            if mouse_board_coordinate == coordinate:
                self.the_dragging_checker.board_coordinate = coordinate
                # mark a king on checker when reaching the top row
                self.try_become_king(self.the_dragging_checker)
                if captured is None:
                    self.normal_moves += 1
                else:
                    self.remove_checker(captured)
                    self.normal_moves = 0
                more_moves = self.find_legal_moves(self.the_dragging_checker)
                # captured and has more move and has capture move, extra step
                if not (captured is not None and more_moves != [] and more_moves[0][1] != None):
                    self.update_movables()
                    # check if the game is over
                    if self.is_draw() or self.is_player_won() or self.is_ai_won():
                        self.freeze_checkers()
                    else:
                        # pass to ai's turn
                        self.ai_countdown = DELAY
                        print("Computer's turn")
                # make more jumps
                else:
                    for checker in self.player_checkers:
                        if checker != self.the_dragging_checker:
                            checker.is_movable = False

        # release checker from mouse
        self.the_dragging_checker = None

    def ai_move(self):
        # basic algorithm for ai move
        if self.ai_checkers == []:
            return
        checkers = self.find_movable_checkers(self.ai_checkers)
        checker_to_move = random.choice(checkers)
        moves = self.find_legal_moves(checker_to_move)
        coordinate, captured = random.choice(moves)
        checker_to_move.board_coordinate = coordinate
        self.try_become_king(checker_to_move)
        if captured is None:
            self.normal_moves += 1
        else:
            self.remove_checker(captured)
            self.normal_moves = 0
        more_moves = self.find_legal_moves(checker_to_move)
        if captured is not None and more_moves != [] and more_moves[0][1] != None:
            for checker in self.ai_checkers:
                if checker != checker_to_move:
                    checker.is_movable = False
            self.ai_countdown = DELAY
        else:
            self.update_movables()
            if self.is_draw() or self.is_player_won() or self.is_ai_won():
                self.freeze_checkers()
            else:
                print("Player's turn")

    def try_become_king(self, checker):
        # check if a checker can become king
        if not checker.is_king:
            if (checker.board_coordinate[1] == 0 and checker.color == BLACK) or (checker.board_coordinate[1] == 7 and checker.color == RED):
                checker.is_king = True
                print("Woohoo!")

    def is_within_board(self, coordinate):
        # set the edges of the board
        return coordinate[0] >= 0 and coordinate[1] >= 0 and coordinate[0] < BOARD_SIZE and coordinate[1] < BOARD_SIZE

    def find_legal_moves(self, checker):
        # return a list of all legal moves of one checker
        legal_moves = []
        a, b = checker.board_coordinate
        top_left = [(a-1, b-1), (a-2, b-2)]
        top_right = [(a+1, b-1), (a+2, b-2)]
        bottom_left = [(a-1, b+1), (a-2, b+2)]
        bottom_right = [(a+1, b+1), (a+2, b+2)]
        all_spots = [top_left, top_right, bottom_left, bottom_right]

        if checker.is_king:
            spots = all_spots
        elif checker.color == BLACK:
            spots = [top_left, top_right]
        elif checker.color == RED:
            spots = [bottom_left, bottom_right]
        for normal_move_coordinate, jump_coordinate in spots:
            c = self.get_checker_by_coordinate(normal_move_coordinate)
            if self.is_within_board(jump_coordinate) and not self.is_occupied(jump_coordinate) and c is not None and c.color != checker.color:
                legal_moves.append((jump_coordinate, c))

        if legal_moves == []:
            for normal_move_coordinate, jump_coordinate in spots:
                if self.is_within_board(normal_move_coordinate) and not self.is_occupied(normal_move_coordinate):
                    legal_moves.append((normal_move_coordinate, None))

        return legal_moves

    def find_movable_checkers(self, checker_list):
        # return a list of all checkers that have at least one legal move
        movable_checkers = []
        for checker in checker_list:
            for coordinate, captured in self.find_legal_moves(checker):
                if captured != None:
                    movable_checkers.append(checker)
                    break
        if movable_checkers == []:
            for checker in checker_list:
                for coordinate, captured in self.find_legal_moves(checker):
                    if coordinate != None:
                        movable_checkers.append(checker)
                        break
        return movable_checkers

    def update_movables(self):
        for checker in self.player_checkers + self.ai_checkers:
            checker.is_movable = False
        for checker in self.find_movable_checkers(self.player_checkers):
            checker.is_movable = True
        for checker in self.find_movable_checkers(self.ai_checkers):
            checker.is_movable = True

    def get_checker_by_coordinate(self, coordinate):
        # return a checker the cell has
        for c in self.player_checkers + self.ai_checkers:
            if c.board_coordinate == coordinate:
                return c
        return None

    def remove_checker(self, checker):
        # remove a checker from the game
        if checker in self.player_checkers:
            self.player_checkers.remove(checker)
        else:
            self.ai_checkers.remove(checker)

    def is_occupied(self, coordinate):
        # return t/f if a cell has a checker
        return self.get_checker_by_coordinate(coordinate) is not None

    def end_game(self):
        # display end game message
        if self.is_draw():
            self.display_message("IT'S A DRAW")

        elif self.is_ai_won():
            self.display_message("SORRY, YOU LOST :(")

        elif self.is_player_won():
            self.display_message("YEA, YOU WIN!! :)")
            self.score_to_add = 1

    def display_message(self, message):
        fill(0)
        textSize(80)
        textAlign(CENTER)
        text(message, WINDOW_SIZE/2 + 5, WINDOW_SIZE/2 + 5)
        fill(255)
        text(message, WINDOW_SIZE/2, WINDOW_SIZE/2)

    def is_draw(self):
        return self.normal_moves == 50

    def is_player_won(self):
        return self.ai_checkers == [] or self.find_movable_checkers(self.ai_checkers) == []

    def is_ai_won(self):
        return self.player_checkers == [] or self.find_movable_checkers(self.player_checkers) == []

    def freeze_checkers(self):
        # make all checkers not movable
        for c in self.player_checkers + self.ai_checkers:
            c.is_movable = False
        self.game_over = True
        self.pop_up_countdown = POP_UP_DELAY

    def update_score(self, score_to_add):
        # read file and write score
        from javax.swing import JOptionPane
        answer = JOptionPane.showInputDialog(frame, 'Please enter your name')

        if answer:
            print('hi ' + answer)
        elif answer == '':
            print('[empty string]')
        else:
            print(answer)

        scores = {}

        file = open("scores.txt", "r")
        lines = file.readlines()
        for l in lines:
            record = l.split()
            name = record[0]
            score = int(record[1])
            scores[name] = score
        file.close()

        if answer not in scores:
            scores[answer] = score_to_add
        scores[answer] += score_to_add

        final_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        file = open("scores.txt", "w")
        for name, score in final_scores:
            file.write(" ".join([name, str(score)]) + "\n")
        file.close()
