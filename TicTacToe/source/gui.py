import threading
import time
import tkinter as tk
from tkinter import messagebox
import game
import ttkbootstrap as ttk


class GUIApplication:
    def __init__(self):
        self.game = None
        self.root = ttk.Window()
        self.style = ttk.Style("darkly")
        self.root.title("Tic Tac Toe")
        self.root.geometry("1200x900")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # main label frame
        self.main_label_frame = ttk.Frame(self.root)
        self.label = tk.Label(self.main_label_frame, text="Tic Tac Toe", font=("Ariel", 30))

        self.label.pack(pady=20, side="left")
        self.main_label_frame.pack()

        # game board frame
        self.game_board_frame = ttk.Frame(self.root)
        self.board_labels = []
        self.create_board()

        self.game_board_frame.pack(padx=30, pady=10)

        # state frame
        self.game_state_frame = tk.Frame(self.root)
        self.state_label = tk.Label(self.game_state_frame, text="Press Start ...", font=("Ariel", 20))
        self.state_label.pack()
        self.game_state_frame.pack(padx=30, pady=30)

        # button frame
        self.buttons_frame = tk.Frame(self.root)
        self.start_button = tk.Button(self.buttons_frame, text="Start", font=("Ariel", 18), command=self.start_game)
        self.start_button.pack(side="left")
        self.finish_button = tk.Button(self.buttons_frame, text="Finish", font=("Ariel", 18), command=self.finish_game)
        self.finish_button.pack(side="left", padx=20)
        self.buttons_frame.pack()

    def create_board(self):
        for row in range(10):
            labels_row = []
            for col in range(10):
                label = ttk.Label(self.game_board_frame,
                                  style='Custom.TLabel',
                                  relief='flat',
                                  anchor='center',
                                  font=("Ariel", 25),
                                  width=5)
                label.config(foreground='black', background='lightblue')
                label.grid(row=row, column=col, padx=4, pady=4)
                labels_row.append(label)

            self.board_labels.append(labels_row)

            for i in range(10):
                self.game_board_frame.rowconfigure(i, weight=1)
            for j in range(10):
                self.game_board_frame.columnconfigure(j, weight=1)

    def update_board(self):
        if self.game:
            for row in range(0, 10):
                for col in range(0, 10):
                    cell_value = self.game.get_board()[row * 10 + col]
                    self.board_labels[row][col].config(text=cell_value)
            self.root.update()

    def handle_win(self):
        winners = self.game.winning_numbers
        for number in winners:
            row = number // 10
            col = number % 10
            self.board_labels[row][col].config(background="green")
        self.finish_button.config(text='Reset')
        self.state_label.config(text=f"{self.game.winner} wins")

    def handle_tie(self):
        for row in range(10):
            for col in range(10):
                self.board_labels[row][col].config(bg="yellow")
        self.finish_button.config(text='Reset')

    def on_close(self):
        if messagebox.askokcancel("Quit", "Do you want to quit the game?"):
            if self.game:
                self.finish_game()
            self.root.destroy()

    def start_game(self):
        self.start_button.config(state='disabled')
        self.finish_button.config(text='Finish')
        self.game = game.Game()
        while True:
            if self.game is None:
                break
            player1 = threading.Thread(target=self.game.computer, args=('x',))
            player2 = threading.Thread(target=self.game.computer, args=('o',))

            player1.start()
            self.update_turn_label()
            player1.join()
            time.sleep(0.2)
            self.update_board()
            time.sleep(0.5)

            player2.start()
            self.update_turn_label()
            player2.join()
            time.sleep(0.2)
            self.update_board()
            time.sleep(0.5)

            if self.game and self.game.win_event.is_set():
                if self.game.winning_numbers:
                    self.handle_win()
                else:
                    self.handle_tie()
                break

    def start(self):
        self.root.mainloop()

    def update_turn_label(self):
        if self.game:
            self.state_label.config(text=f"{self.game.player_turn}'s turn")

    def finish_game(self):
        self.state_label.config(text='Press start to run again!')
        self.start_button.config(state='normal')
        if self.game:
            self.game.get_win_event().set()
            self.game = None
        for row in range(10):
            for col in range(10):
                self.board_labels[row][col].config(text="", background="lightblue")


if __name__ == "__main__":
    app = GUIApplication()
    app.start()
