import tkinter as tk
from tkinter import messagebox
import random


class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
        self.window = tk.Tk()
        self.window.title("Крестики-нолики")
        self.window.resizable(False, False)

        # Центрирование окна
        self.center_window()

        # Настройка цветов
        self.bg_color = "#f0f0f0"
        self.button_color = "#ffffff"
        self.x_color = "#ff6b6b"
        self.o_color = "#4ecdc4"
        self.font = ("Arial", 20, "bold")

        self.window.configure(bg=self.bg_color)
        self.buttons = []
        self.create_widgets()

        # Настройки игры
        self.x_player = "human"  # human или ai
        self.o_player = "ai"  # human или ai
        self.current_player = "X"

    def center_window(self):
        """Центрирует окно на экране"""
        self.window.update_idletasks()
        width = 400
        height = 500
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        # Фрейм для кнопок игры
        game_frame = tk.Frame(self.window, bg=self.bg_color)
        game_frame.pack(pady=20)

        # Создание кнопок 3x3
        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                btn = tk.Button(game_frame, text=" ", font=self.font, width=4, height=2,
                                bg=self.button_color, command=lambda idx=index: self.human_move(idx))
                btn.grid(row=i, column=j, padx=2, pady=2)
                self.buttons.append(btn)

        # Фрейм для управления
        control_frame = tk.Frame(self.window, bg=self.bg_color)
        control_frame.pack(pady=10)

        # Кнопка новой игры
        new_game_btn = tk.Button(control_frame, text="Новая игра", font=("Arial", 12),
                                 command=self.reset_game, bg="#6c5ce7", fg="white")
        new_game_btn.pack(side=tk.LEFT, padx=5)

        # Кнопка смены режима
        mode_btn = tk.Button(control_frame, text="Сменить режим", font=("Arial", 12),
                             command=self.change_mode, bg="#00b894", fg="white")
        mode_btn.pack(side=tk.LEFT, padx=5)

        # Метка статуса
        self.status_label = tk.Label(self.window, text="Ваш ход (X)", font=("Arial", 14),
                                     bg=self.bg_color, fg="#2d3436")
        self.status_label.pack(pady=10)

    def change_mode(self):
        # Окно выбора режима
        mode_window = tk.Toplevel(self.window)
        mode_window.title("Выбор режима")
        mode_window.resizable(False, False)
        mode_window.configure(bg=self.bg_color)
        mode_window.transient(self.window)
        mode_window.grab_set()

        # Центрирование окна выбора режима
        mode_window.update_idletasks()
        width = 250
        height = 150
        x = (mode_window.winfo_screenwidth() // 2) - (width // 2)
        y = (mode_window.winfo_screenheight() // 2) - (height // 2)
        mode_window.geometry(f'{width}x{height}+{x}+{y}')

        tk.Label(mode_window, text="Выберите режим игры:", font=("Arial", 12),
                 bg=self.bg_color).pack(pady=10)

        # Только два режима (без ИИ vs ИИ)
        modes = [
            ("Человек vs ИИ", "human", "ai"),
            ("Человек vs Человек", "human", "human")
        ]

        for text, x_mode, o_mode in modes:
            btn = tk.Button(mode_window, text=text, font=("Arial", 10),
                            command=lambda x=x_mode, o=o_mode: self.set_mode(x, o, mode_window),
                            bg=self.button_color, width=20)
            btn.pack(pady=5)

    def set_mode(self, x_mode, o_mode, mode_window):
        self.x_player = x_mode
        self.o_player = o_mode
        mode_window.destroy()
        self.reset_game()
        messagebox.showinfo("Режим изменен",
                            f"Установлен режим: {'Человек' if x_mode == 'human' else 'ИИ'} vs {'Человек' if o_mode == 'human' else 'ИИ'}")

    def reset_game(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
        self.current_player = "X"

        for btn in self.buttons:
            btn.config(text=" ", bg=self.button_color, state=tk.NORMAL)

        self.update_status()

        # Если ИИ ходит первым
        if self.x_player == "ai" and self.current_player == "X":
            self.window.after(500, self.ai_move)

    def human_move(self, square):
        if self.board[square] == ' ' and not self.current_winner:
            current_player_type = self.x_player if self.current_player == "X" else self.o_player

            if current_player_type == "human":
                self.make_move(square, self.current_player)

                if not self.current_winner and self.empty_squares():
                    self.window.after(300, self.ai_move)

    def ai_move(self):
        if not self.current_winner and self.empty_squares():
            current_player_type = self.x_player if self.current_player == "X" else self.o_player

            if current_player_type == "ai":
                square = self.get_ai_move()
                if square is not None:
                    self.make_move(square, self.current_player)

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter

            # Обновление кнопки
            color = self.x_color if letter == "X" else self.o_color
            self.buttons[square].config(text=letter, fg=color, state=tk.DISABLED)

            if self.winner(square, letter):
                self.current_winner = letter
                self.highlight_winning_line()
                self.show_winner()
            elif not self.empty_squares():
                self.show_draw()
            else:
                self.switch_player()
                self.update_status()

    def switch_player(self):
        self.current_player = "O" if self.current_player == "X" else "X"

    def update_status(self):
        player_name = "Ваш ход" if (
                (self.current_player == "X" and self.x_player == "human") or
                (self.current_player == "O" and self.o_player == "human")
        ) else "Ход ИИ"

        self.status_label.config(text=f"{player_name} ({self.current_player})")

    def empty_squares(self):
        return ' ' in self.board

    def winner(self, square, letter):
        # Проверка строки
        row_ind = square // 3
        row = self.board[row_ind * 3:(row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            return True

        # Проверка столбца
        col_ind = square % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # Проверка диагоналей
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True

        return False

    def highlight_winning_line(self):
        # Поиск выигрышной линии
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # строки
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # столбцы
            [0, 4, 8], [2, 4, 6]  # диагонали
        ]

        for line in lines:
            if self.board[line[0]] == self.board[line[1]] == self.board[line[2]] != ' ':
                for idx in line:
                    self.buttons[idx].config(bg="#ffeaa7")  # Подсветка желтым
                break

    def get_ai_move(self):
        # Упрощенный минимакс для скорости
        best_score = -float('inf')
        best_move = None

        # Если поле пустое, случайный ход для разнообразия
        if self.board.count(' ') == 9:
            return random.choice([i for i in range(9) if self.board[i] == ' '])

        for move in range(9):
            if self.board[move] == ' ':
                self.board[move] = 'O'
                score = self.minimax(False)
                self.board[move] = ' '

                if score > best_score:
                    best_score = score
                    best_move = move

        return best_move

    def minimax(self, is_maximizing, depth=0):
        # Упрощенный минимакс с ограниченной глубиной для скорости
        if self.current_winner == 'O':
            return 10 - depth
        elif self.current_winner == 'X':
            return depth - 10
        elif not self.empty_squares():
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for move in range(9):
                if self.board[move] == ' ':
                    self.board[move] = 'O'
                    if self.winner(move, 'O'):
                        self.current_winner = 'O'
                    score = self.minimax(False, depth + 1)
                    self.board[move] = ' '
                    self.current_winner = None
                    best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for move in range(9):
                if self.board[move] == ' ':
                    self.board[move] = 'X'
                    if self.winner(move, 'X'):
                        self.current_winner = 'X'
                    score = self.minimax(True, depth + 1)
                    self.board[move] = ' '
                    self.current_winner = None
                    best_score = min(best_score, score)
            return best_score

    def show_winner(self):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)

        winner_text = "Вы победили!" if (
                (self.current_winner == "X" and self.x_player == "human") or
                (self.current_winner == "O" and self.o_player == "human")
        ) else "ИИ победил!" if (
                (self.current_winner == "X" and self.x_player == "ai") or
                (self.current_winner == "O" and self.o_player == "ai")
        ) else f"Игрок {self.current_winner} победил!"

        messagebox.showinfo("Игра окончена", winner_text)

    def show_draw(self):
        for btn in self.buttons:
            btn.config(state=tk.DISABLED)
        messagebox.showinfo("Игра окончена", "Ничья!")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = TicTacToe()
    game.run()