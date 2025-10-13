import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_winner = None
        self.window = tk.Tk()
        self.window.title("Крестики-нолики")
        self.window.resizable(False, False)
        self.center_window()

        self.bg_color = "#f0f0f0"
        self.button_color = "#ffffff"
        self.x_color = "#ff6b6b"
        self.o_color = "#4ecdc4"
        self.font = ("Arial", 20, "bold")

        self.window.configure(bg=self.bg_color)
        self.buttons = []
        self.current_player = "X"
        self.create_widgets()

    def center_window(self):
        self.window.update_idletasks()
        w, h = 300, 400
        x = (self.window.winfo_screenwidth() - w) // 2
        y = (self.window.winfo_screenheight() - h) // 2
        self.window.geometry(f'{w}x{h}+{x}+{y}')

    def create_widgets(self):
        game_frame = tk.Frame(self.window, bg=self.bg_color)
        game_frame.pack(pady=20)

        for i in range(9):
            btn = tk.Button(game_frame, text=" ", font=self.font, width=4, height=2,
                            bg=self.button_color, command=lambda idx=i: self.human_move(idx))
            btn.grid(row=i // 3, column=i % 3, padx=2, pady=2)
            self.buttons.append(btn)

        tk.Button(self.window, text="Новая игра", font=("Arial", 12),
                  command=self.reset_game, bg="#6c5ce7", fg="white").pack(pady=10)

        self.status_label = tk.Label(self.window, text="Ваш ход (X)", font=("Arial", 14),
                                     bg=self.bg_color, fg="#2d3436")
        self.status_label.pack(pady=5)

    def reset_game(self):
        self.board = [' '] * 9
        self.current_winner = None
        self.current_player = "X"
        for btn in self.buttons:
            btn.config(text=" ", bg=self.button_color, state=tk.NORMAL)
        self.status_label.config(text="Ваш ход (X)")

    def human_move(self, square):
        if self.board[square] == ' ' and not self.current_winner and self.current_player == "X":
            self.make_move(square, "X")
            if not self.current_winner and any(cell == ' ' for cell in self.board):
                self.window.after(300, self.ai_move)

    def ai_move(self):
        if not self.current_winner and any(cell == ' ' for cell in self.board) and self.current_player == "O":
            square = self.get_ai_move()
            if square is not None:
                self.make_move(square, "O")

    def make_move(self, square, letter):
        self.board[square] = letter
        color = self.x_color if letter == "X" else self.o_color
        self.buttons[square].config(text=letter, fg=color, state=tk.DISABLED)

        if self.check_winner(square, letter):
            self.current_winner = letter
            self.highlight_winner()
            self.show_winner()
        elif ' ' not in self.board:
            self.show_draw()
        else:
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_label.config(text="Ваш ход (X)" if self.current_player == "X" else "Ход ИИ (O)")

    def check_winner(self, square, letter):
        row = square // 3
        col = square % 3
        if all(self.board[row * 3 + i] == letter for i in range(3)) or \
                all(self.board[col + i * 3] == letter for i in range(3)):
            return True
        if square % 2 == 0:
            if all(self.board[i] == letter for i in [0, 4, 8]) or \
                    all(self.board[i] == letter for i in [2, 4, 6]):
                return True
        return False

    def highlight_winner(self):
        lines = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        for line in lines:
            if self.board[line[0]] == self.board[line[1]] == self.board[line[2]] != ' ':
                for idx in line: self.buttons[idx].config(bg="#ffeaa7")
                break

    def get_ai_move(self):
        # Минимакс алгоритм
        best_score = float('-inf')
        best_move = None
        for i in range(9):
            if self.board[i] == ' ':
                self.board[i] = 'O'
                score = self.minimax(self.board, 0, False)
                self.board[i] = ' '
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def minimax(self, board, depth, is_maximizing):
        # Проверка терминальных состояний
        if self.check_game_over(board, 'O'): return 1
        if self.check_game_over(board, 'X'): return -1
        if ' ' not in board: return 0

        if is_maximizing:
            best_score = float('-inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'O'
                    score = self.minimax(board, depth + 1, False)
                    board[i] = ' '
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == ' ':
                    board[i] = 'X'
                    score = self.minimax(board, depth + 1, True)
                    board[i] = ' '
                    best_score = min(score, best_score)
            return best_score

    def check_game_over(self, board, player):
        # Проверка победы для любого игрока
        wins = [[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]]
        return any(all(board[i] == player for i in line) for line in wins)

    def show_winner(self):
        for btn in self.buttons: btn.config(state=tk.DISABLED)
        winner = "Вы победили!" if self.current_winner == "X" else "ИИ победил!"
        messagebox.showinfo("Игра окончена", winner)

    def show_draw(self):
        for btn in self.buttons: btn.config(state=tk.DISABLED)
        messagebox.showinfo("Игра окончена", "Ничья!")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()
