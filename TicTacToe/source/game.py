import random
import threading


class Game:
    def __init__(self):
        self.board = [None] * 100  # 10x10 board
        self.win_event = threading.Event()
        self.winner = None
        self.winning_numbers = []
        self.player_turn = None

    def check_win(self):
        # Check rows
        for i in range(0, 100, 10):
            for j in range(i, i + 8):
                if self.board[j] == self.board[j + 1] == self.board[j + 2] and self.board[j] is not None:
                    self.winning_numbers.append(j)
                    self.winning_numbers.append(j + 1)
                    self.winning_numbers.append(j + 2)
                    self.winner = self.board[j]
                    return True
        # Check columns
        for i in range(10):
            for j in range(i, 80, 10):
                if self.board[j] == self.board[j + 10] == self.board[j + 20] and self.board[j] is not None:
                    self.winning_numbers.append(j)
                    self.winning_numbers.append(j + 10)
                    self.winning_numbers.append(j + 20)
                    self.winner = self.board[j]
                    return True

        # Check decreasing diagonals
        for i in range(0, 80, 10):
            for j in range(i, i + 8):
                if self.board[j] == self.board[j + 11] == self.board[j + 22] and self.board[j] is not None:
                    self.winning_numbers.append(j)
                    self.winning_numbers.append(j + 11)
                    self.winning_numbers.append(j + 22)
                    self.winner = self.board[j]
                    return True

        # Check increasing diagonals
        for i in range(20, 100, 10):
            for j in range(i, i + 8):
                if self.board[j] == self.board[j - 9] == self.board[j - 18] and self.board[j] is not None:
                    self.winning_numbers.append(j)
                    self.winning_numbers.append(j - 9)
                    self.winning_numbers.append(j - 18)
                    self.winner = self.board[j]
                    return True

        # Check for tie
        if all(self.board):
            return True

        return False

    def computer(self, player):
        while not self.win_event.is_set():
            self.player_turn = player
            move = random.randint(0, 99)
            if self.board[move] is None:
                self.board[move] = player
                if self.check_win():
                    self.win_event.set()
                break

    def get_win_event(self):
        return self.win_event

    def get_board(self):
        return self.board
