import pytest
from .test import create_board

# filepath: /e:/workspace/python/rdm/rdm/test_test.py

def test_create_board_size():
    size = 5
    num_mines = 3
    board = create_board(size, num_mines)
    assert len(board) == size
    assert all(len(row) == size for row in board)

def test_create_board_mines_count():
    size = 5
    num_mines = 3
    board = create_board(size, num_mines)
    mine_count = sum(cell == -1 for row in board for cell in row)
    assert mine_count == num_mines

def test_create_board_mines_placement():
    size = 5
    num_mines = 3
    board = create_board(size, num_mines)
    for i in range(size):
        for j in range(size):
            if board[i][j] == -1:
                for x in range(max(0, i-1), min(size, i+2)):
                    for y in range(max(0, j-1), min(size, j+2)):
                        if board[x][y] != -1:
                            assert board[x][y] > 0

def test_create_board_no_negative_numbers():
    size = 5
    num_mines = 3
    board = create_board(size, num_mines)
    for row in board:
        for cell in row:
            assert cell >= -1