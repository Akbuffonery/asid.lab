import tkinter as tk
from tkinter import messagebox
import random
from typing import List, Tuple, Optional


class Ship:
    def __init__(self, size: int):
        self.size = size
        self.hits = 0
        self.positions = []
        self.horizontal = True

    def is_sunk(self) -> bool:
        return self.hits >= self.size


class Board:
    def __init__(self, size: int = 10):
        self.size = size
        self.grid = [['~' for _ in range(size)] for _ in range(size)]
        self.ships = []
        self.ship_positions = set()

    def place_ship(self, ship: Ship, row: int, col: int, horizontal: bool) -> bool:
        positions = []

        if horizontal:
            if col + ship.size > self.size:
                return False
            for i in range(ship.size):
                if self.grid[row][col + i] != '~' or self.has_adjacent_ships(row, col + i):
                    return False
                positions.append((row, col + i))
        else:
            if row + ship.size > self.size:
                return False
            for i in range(ship.size):
                if self.grid[row + i][col] != '~' or self.has_adjacent_ships(row + i, col):
                    return False
                positions.append((row + i, col))

        # Размещаем корабль
        for r, c in positions:
            self.grid[r][c] = 'S'
            self.ship_positions.add((r, c))

        ship.positions = positions
        ship.horizontal = horizontal
        self.ships.append(ship)
        return True

    def has_adjacent_ships(self, row: int, col: int) -> bool:
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                r, c = row + dr, col + dc
                if 0 <= r < self.size and 0 <= c < self.size:
                    if self.grid[r][c] == 'S':
                        return True
        return False

    def receive_attack(self, row: int, col: int) -> Tuple[bool, bool]:
        """Возвращает (попал, потопил)"""
        if self.grid[row][col] == 'S':
            self.grid[row][col] = 'X'  # Попадание

            # Находим корабль и обновляем hits
            for ship in self.ships:
                if (row, col) in ship.positions:
                    ship.hits += 1
                    return True, ship.is_sunk()

        elif self.grid[row][col] == '~':
            self.grid[row][col] = 'O'  # Промах

        return False, False


class IntelligentBot:
    def __init__(self, board_size: int = 10):
        self.board_size = board_size
        self.hits = []
        self.misses = set()
        self.potential_targets = []
        self.last_hit = None
        self.hunting_mode = False

    def place_ships_intelligently(self, ships: List[int]) -> Board:
        """Интеллектуальная расстановка кораблей"""
        board = Board(self.board_size)

        for ship_size in sorted(ships, reverse=True):
            placed = False
            attempts = 0

            while not placed and attempts < 100:
                row = random.randint(0, self.board_size - 1)
                col = random.randint(0, self.board_size - 1)
                horizontal = random.choice([True, False])

                ship = Ship(ship_size)
                if board.place_ship(ship, row, col, horizontal):
                    placed = True

                attempts += 1

            if not placed:
                # Если не удалось разместить, пробуем другой подход
                for r in range(self.board_size):
                    for c in range(self.board_size):
                        for hor in [True, False]:
                            ship = Ship(ship_size)
                            if board.place_ship(ship, r, c, hor):
                                placed = True
                                break
                        if placed:
                            break
                    if placed:
                        break

        return board

    def make_attack(self) -> Tuple[int, int]:
        """Интеллектуальная атака бота"""
        if self.hunting_mode and self.last_hit:
            return self._hunt_around_hit()
        else:
            return self._probability_attack()

    def _hunt_around_hit(self) -> Tuple[int, int]:
        """Охота вокруг попадания"""
        if not self.potential_targets:
            self._generate_potential_targets()

        if self.potential_targets:
            return self.potential_targets.pop(0)
        else:
            self.hunting_mode = False
            return self._probability_attack()

    def _generate_potential_targets(self):
        """Генерация потенциальных целей вокруг попадания"""
        row, col = self.last_hit
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if (0 <= r < self.board_size and 0 <= c < self.board_size and
                    (r, c) not in self.misses and (r, c) not in self.hits):
                self.potential_targets.append((r, c))

    def _probability_attack(self) -> Tuple[int, int]:
        """Атака на основе вероятностной карты"""
        # Создаем вероятностную карту
        probability_map = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]

        for ship_size in [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]:  # Стандартные корабли
            for row in range(self.board_size):
                for col in range(self.board_size):
                    # Проверяем горизонтальное размещение
                    if col + ship_size <= self.board_size:
                        valid = True
                        for i in range(ship_size):
                            if (row, col + i) in self.misses or (row, col + i) in self.hits:
                                valid = False
                                break
                        if valid:
                            for i in range(ship_size):
                                probability_map[row][col + i] += 1

                    # Проверяем вертикальное размещение
                    if row + ship_size <= self.board_size:
                        valid = True
                        for i in range(ship_size):
                            if (row + i, col) in self.misses or (row + i, col) in self.hits:
                                valid = False
                                break
                        if valid:
                            for i in range(ship_size):
                                probability_map[row + i][col] += 1

        # Находим клетку с максимальной вероятностью
        max_prob = -1
        best_moves = []

        for row in range(self.board_size):
            for col in range(self.board_size):
                if (row, col) not in self.misses and (row, col) not in self.hits:
                    if probability_map[row][col] > max_prob:
                        max_prob = probability_map[row][col]
                        best_moves = [(row, col)]
                    elif probability_map[row][col] == max_prob:
                        best_moves.append((row, col))

        return random.choice(best_moves) if best_moves else self._random_attack()

    def _random_attack(self) -> Tuple[int, int]:
        """Случайная атака, если нет хороших вариантов"""
        while True:
            row = random.randint(0, self.board_size - 1)
            col = random.randint(0, self.board_size - 1)
            if (row, col) not in self.misses and (row, col) not in self.hits:
                return (row, col)

    def record_result(self, row: int, col: int, hit: bool, sunk: bool):
        """Запись результата атаки"""
        if hit:
            self.hits.append((row, col))
            self.last_hit = (row, col)
            self.hunting_mode = True

            if sunk:
                # Если корабль потоплен, очищаем потенциальные цели и переходим в режим поиска
                self.potential_targets = []
                self.hunting_mode = False
                # Помечаем все клетки вокруг потопленного корабля как промахи
                for r, c in self.hits[-4:]:  # Предполагаем максимальный размер корабля 4
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            nr, nc = r + dr, c + dc
                            if (0 <= nr < self.board_size and 0 <= nc < self.board_size and
                                    (nr, nc) not in self.hits):
                                self.misses.add((nr, nc))
        else:
            self.misses.add((row, col))

    def reset(self):
        """Сброс состояния бота для новой игры"""
        self.hits = []
        self.misses = set()
        self.potential_targets = []
        self.last_hit = None
        self.hunting_mode = False


class BattleshipGame:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Морской Бой")
        self.root.geometry("800x600")

        self.board_size = 10
        self.ship_sizes = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]  # Стандартные корабли

        self.player_board = Board(self.board_size)
        self.bot = IntelligentBot(self.board_size)
        self.bot_board = self.bot.place_ships_intelligently(self.ship_sizes)

        self.current_ship_index = 0
        self.placing_ships = True
        self.current_ship_horizontal = True
        self.game_over = False

        self.setup_ui()

    def setup_ui(self):
        # Основной фрейм
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Фрейм для игровых полей
        boards_frame = tk.Frame(main_frame)
        boards_frame.pack(fill=tk.BOTH, expand=True)

        # Поле игрока
        player_frame = tk.Frame(boards_frame)
        player_frame.pack(side=tk.LEFT, padx=10)

        tk.Label(player_frame, text="Ваше поле", font=("Arial", 12, "bold")).pack()
        self.player_canvas = tk.Canvas(player_frame, width=300, height=300, bg="white")
        self.player_canvas.pack()

        # Поле бота
        bot_frame = tk.Frame(boards_frame)
        bot_frame.pack(side=tk.RIGHT, padx=10)

        tk.Label(bot_frame, text="Поле противника", font=("Arial", 12, "bold")).pack()
        self.bot_canvas = tk.Canvas(bot_frame, width=300, height=300, bg="white")
        self.bot_canvas.pack()
        self.bot_canvas.bind("<Button-1>", self.on_bot_click)

        # Фрейм управления
        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)

        self.status_label = tk.Label(control_frame, text="Расставьте ваши корабли", font=("Arial", 12))
        self.status_label.pack()

        rotate_button = tk.Button(control_frame, text="Повернуть корабль", command=self.rotate_ship)
        rotate_button.pack(side=tk.LEFT, padx=5)

        random_button = tk.Button(control_frame, text="Случайная расстановка", command=self.random_placement)
        random_button.pack(side=tk.LEFT, padx=5)

        new_game_button = tk.Button(control_frame, text="Новая игра", command=self.new_game)
        new_game_button.pack(side=tk.LEFT, padx=5)

        # Привязываем события мыши к полю игрока
        self.player_canvas.bind("<Motion>", self.on_player_mouse_move)
        self.player_canvas.bind("<Button-1>", self.on_player_click)

        self.draw_boards()

    def draw_boards(self):
        self.draw_board(self.player_canvas, self.player_board, True)
        self.draw_board(self.bot_canvas, self.bot_board, False)

    def draw_board(self, canvas, board, show_ships: bool):
        canvas.delete("all")
        cell_size = 30

        # Рисуем сетку
        for i in range(self.board_size + 1):
            canvas.create_line(i * cell_size, 0, i * cell_size, self.board_size * cell_size)
            canvas.create_line(0, i * cell_size, self.board_size * cell_size, i * cell_size)

        # Рисуем клетки
        for row in range(self.board_size):
            for col in range(self.board_size):
                x1 = col * cell_size
                y1 = row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                cell = board.grid[row][col]

                if cell == '~':  # Вода
                    canvas.create_rectangle(x1, y1, x2, y2, fill="lightblue", outline="gray")
                elif cell == 'S' and show_ships:  # Корабль (только на своем поле)
                    canvas.create_rectangle(x1, y1, x2, y2, fill="gray", outline="gray")
                elif cell == 'S' and not show_ships:  # Корабль противника - скрываем (рисуем как воду)
                    canvas.create_rectangle(x1, y1, x2, y2, fill="lightblue", outline="gray")
                elif cell == 'X':  # Попадание
                    canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="gray")
                    canvas.create_line(x1, y1, x2, y2, fill="darkred", width=2)
                    canvas.create_line(x2, y1, x1, y2, fill="darkred", width=2)
                elif cell == 'O':  # Промах
                    canvas.create_rectangle(x1, y1, x2, y2, fill="white", outline="gray")
                    canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="blue")

        # Добавляем буквы и цифры для координат
        for i in range(self.board_size):
            # Буквы сверху
            canvas.create_text(i * cell_size + cell_size // 2, -15, text=chr(65 + i))
            # Цифры слева
            canvas.create_text(-15, i * cell_size + cell_size // 2, text=str(i + 1))

    def on_player_mouse_move(self, event):
        if not self.placing_ships or self.current_ship_index >= len(self.ship_sizes):
            return

        self.draw_boards()

        cell_size = 30
        col = event.x // cell_size
        row = event.y // cell_size

        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            ship_size = self.ship_sizes[self.current_ship_index]
            color = "lightgreen"

            # Проверяем возможность размещения
            can_place = True
            if self.current_ship_horizontal:
                if col + ship_size > self.board_size:
                    can_place = False
                else:
                    for i in range(ship_size):
                        if (self.player_board.grid[row][col + i] != '~' or
                                self.player_board.has_adjacent_ships(row, col + i)):
                            can_place = False
                            break
            else:
                if row + ship_size > self.board_size:
                    can_place = False
                else:
                    for i in range(ship_size):
                        if (self.player_board.grid[row + i][col] != '~' or
                                self.player_board.has_adjacent_ships(row + i, col)):
                            can_place = False
                            break

            if not can_place:
                color = "lightcoral"

            # Рисуем предварительное размещение
            if self.current_ship_horizontal:
                if col + ship_size <= self.board_size:
                    for i in range(ship_size):
                        x1 = (col + i) * cell_size
                        y1 = row * cell_size
                        x2 = x1 + cell_size
                        y2 = y1 + cell_size
                        self.player_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
            else:
                if row + ship_size <= self.board_size:
                    for i in range(ship_size):
                        x1 = col * cell_size
                        y1 = (row + i) * cell_size
                        x2 = x1 + cell_size
                        y2 = y1 + cell_size
                        self.player_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    def on_player_click(self, event):
        if not self.placing_ships or self.current_ship_index >= len(self.ship_sizes):
            return

        cell_size = 30
        col = event.x // cell_size
        row = event.y // cell_size

        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            ship_size = self.ship_sizes[self.current_ship_index]
            ship = Ship(ship_size)

            if self.player_board.place_ship(ship, row, col, self.current_ship_horizontal):
                self.current_ship_index += 1

                if self.current_ship_index >= len(self.ship_sizes):
                    self.placing_ships = False
                    self.status_label.config(text="Игра началась! Атакуйте поле противника!")
                else:
                    next_ship_size = self.ship_sizes[self.current_ship_index]
                    self.status_label.config(text=f"Разместите корабль размером {next_ship_size}")

                self.draw_boards()
            else:
                self.status_label.config(text="Невозможно разместить корабль здесь!")

    def rotate_ship(self):
        self.current_ship_horizontal = not self.current_ship_horizontal
        self.draw_boards()

    def random_placement(self):
        self.player_board = Board(self.board_size)
        self.current_ship_index = 0

        for ship_size in self.ship_sizes:
            placed = False
            attempts = 0

            while not placed and attempts < 100:
                row = random.randint(0, self.board_size - 1)
                col = random.randint(0, self.board_size - 1)
                horizontal = random.choice([True, False])

                ship = Ship(ship_size)
                if self.player_board.place_ship(ship, row, col, horizontal):
                    placed = True

                attempts += 1

        self.placing_ships = False
        self.status_label.config(text="Игра началась! Атакуйте поле противника!")
        self.draw_boards()

    def new_game(self):
        """Начать новую игру"""
        self.player_board = Board(self.board_size)
        self.bot.reset()
        self.bot_board = self.bot.place_ships_intelligently(self.ship_sizes)

        self.current_ship_index = 0
        self.placing_ships = True
        self.current_ship_horizontal = True
        self.game_over = False

        self.status_label.config(text="Расставьте ваши корабли")
        self.draw_boards()

    def on_bot_click(self, event):
        if self.placing_ships or self.game_over:
            return

        cell_size = 30
        col = event.x // cell_size
        row = event.y // cell_size

        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            # Проверяем, не стреляли ли уже в эту клетку
            if self.bot_board.grid[row][col] in ['X', 'O']:
                messagebox.showwarning("Внимание", "Вы уже стреляли в эту клетку!")
                return

            # Игрок атакует
            hit, sunk = self.bot_board.receive_attack(row, col)

            if hit:
                self.status_label.config(text="Попадание!")
                if self.check_win(self.bot_board):
                    self.game_over = True
                    messagebox.showinfo("Победа!", "Вы победили!")
                    self.status_label.config(text="Вы победили! Нажмите 'Новая игра' для повторной игры.")
                    return
                if sunk:
                    self.status_label.config(text="Попадание! Корабль потоплен!")
            else:
                self.status_label.config(text="Промах!")

            self.draw_boards()

            # Ход бота
            self.root.after(1000, self.bot_turn)

    def bot_turn(self):
        if self.game_over:
            return

        row, col = self.bot.make_attack()
        hit, sunk = self.player_board.receive_attack(row, col)
        self.bot.record_result(row, col, hit, sunk)

        if hit:
            self.status_label.config(text="Бот попал в вашу клетку!")
            if self.check_win(self.player_board):
                self.game_over = True
                messagebox.showinfo("Поражение", "Бот победил!")
                self.status_label.config(text="Бот победил! Нажмите 'Новая игра' для повторной игры.")
                return
            if sunk:
                self.status_label.config(text="Бот попал! Ваш корабль потоплен!")
        else:
            self.status_label.config(text="Бот промахнулся!")

        self.draw_boards()

    def check_win(self, board: Board) -> bool:
        for ship in board.ships:
            if not ship.is_sunk():
                return False
        return True

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    game = BattleshipGame()
    game.run()