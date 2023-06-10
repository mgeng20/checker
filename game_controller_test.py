from constants import *
from game_controller import GameController
from checker import Checker


def test_constructor():
    gc = GameController()
    assert True


def test_ai_move():
    gc = GameController()
    gc.ai_checkers = [Checker(RED, (5, 7-6), False, False)]
    gc.player_checkers = [Checker(BLACK, (2, 7-1), False, False), Checker(BLACK, (2, 7-3), False, False), Checker(BLACK, (4, 7-5), False, False)]
    gc.update_movables()
    gc.ai_move()
    assert gc.ai_checkers[0].board_coordinate == (3, 3)
    gc.ai_move()
    assert gc.ai_checkers[0].board_coordinate == (1, 5)
    gc.ai_move()
    assert gc.ai_checkers[0].board_coordinate == (3, 7)


def test_try_become_king():
    gc = GameController()
    gc.player_checkers = [Checker(BLACK, (5, 0), False, False)]
    gc.try_become_king(gc.player_checkers[0])
    assert gc.player_checkers[0].is_king == True


def test_is_within_board():
    gc = GameController()
    coordinate = (3, 5)
    assert gc.is_within_board(coordinate)


def test_find_legal_moves():
    gc = GameController()
    c1 = gc.get_checker_by_coordinate((1, 0))
    assert gc.find_legal_moves(c1) == []

    c2 = gc.get_checker_by_coordinate((1, 2))
    assert gc.find_legal_moves(c2) == [((0, 3), None), ((2, 3), None)]


def test_find_movable_checkers():
    gc = GameController()
    assert len(gc.find_movable_checkers(gc.ai_checkers)) == 4
    assert len(gc.find_movable_checkers(gc.player_checkers)) == 4


def test_update_movables():
    gc = GameController()
    gc.ai_checkers = [Checker(RED, (5, 1), False, False)]
    gc.player_checkers = [Checker(BLACK, (2, 6), False, False)]
    gc.update_movables()
    assert gc.ai_checkers[0].is_movable == True
    assert gc.player_checkers[0].is_movable == True


def test_get_checker_by_coordinate():
    coordinate = 5, 0
    gc = GameController()
    assert gc.get_checker_by_coordinate(coordinate)


def test_remove_checker():
    gc = GameController()
    gc.remove_checker(gc.player_checkers[0])
    assert len(gc.player_checkers) == 11


def test_is_occupied():
    coordinate = 5, 6
    gc = GameController()
    assert gc.is_occupied(coordinate) == True


def test_is_draw():
    gc = GameController()
    gc.normal_moves = 50
    assert gc.is_draw()


def test_is_player_won():
    gc = GameController()
    gc.ai_checkers = []
    assert gc.is_player_won()


def test_is_ai_won():
    gc = GameController()
    gc.player_checkers = []
    assert gc.is_ai_won()


def test_freeze_checkers():
    gc = GameController()
    gc.freeze_checkers()
    assert gc.ai_checkers[0].is_movable == False
    assert gc.player_checkers[11].is_movable == False
