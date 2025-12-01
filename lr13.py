import tkinter as tk
from tkinter import messagebox
import random

COLS, ROWS = 21, 15
CELL_SIZE = 33
MAZE_BG = "#332f2c"
WALL_COLOR = "#000000"
PLAYER_COLOR = "#e74c3c"
EXIT_COLOR = "#27ae60"
VISITED_COLOR = "#3498db"
PATH_COLOR = "#9b59b6"
BUTTON_COLOR = "#e67e22"

walls = []
player = (1, 1)
exit_cells = []
player_item = None
exit_items = []
game_over = False
running_search = False
canvas = None
current_direction = "E"
visited_cells = set()
path_history = []

POSSIBLE_EXIT_POSITIONS = [
    (1, 1),
    (COLS - 2, 1),
    (1, ROWS - 2),
    (COLS - 2, ROWS - 2)
]

DIRECTIONS = {
    "N": (0, -1, 0),
    "E": (1, 0, 1),
    "S": (0, 1, 2),
    "W": (-1, 0, 3)
}


def generate_maze():
    global walls
    walls = [[[True, True, True, True] for _ in range(COLS)] for _ in range(ROWS)]
    visited = [[False for _ in range(COLS)] for _ in range(ROWS)]

    def neighbors(cx, cy):
        dirs = [("N", (0, -2), 0, 2), ("S", (0, 2), 2, 0), ("W", (-2, 0), 3, 1), ("E", (2, 0), 1, 3)]
        random.shuffle(dirs)
        for _, (dx, dy), wall_dir, opposite in dirs:
            nx, ny = cx + dx, cy + dy
            if 1 <= nx < COLS - 1 and 1 <= ny < ROWS - 1 and not visited[ny][nx]:
                yield nx, ny, dx, dy

    stack = [(1, 1)]
    visited[1][1] = True
    while stack:
        cx, cy = stack[-1]
        advanced = False
        for nx, ny, dx, dy in neighbors(cx, cy):
            wx, wy = cx + dx // 2, cy + dy // 2
            walls[wy][wx] = [False, False, False, False]
            if dy == -2:
                walls[cy][cx][0] = False
                walls[ny][nx][2] = False
            elif dy == 2:
                walls[cy][cx][2] = False
                walls[ny][nx][0] = False
            elif dx == -2:
                walls[cy][cx][3] = False
                walls[ny][nx][1] = False
            elif dx == 2:
                walls[cy][cx][1] = False
                walls[ny][nx][3] = False
            visited[ny][nx] = True
            stack.append((nx, ny))
            advanced = True
            break
        if not advanced:
            stack.pop()
    for x in range(COLS):
        walls[0][x][0] = True
        walls[ROWS - 1][x][2] = True
    for y in range(ROWS):
        walls[y][0][3] = True
        walls[y][COLS - 1][1] = True


def generate_exits():
    global exit_cells
    exit_cells = random.sample(POSSIBLE_EXIT_POSITIONS, 2)
    for exit_cell in exit_cells:
        ex, ey = exit_cell
        for d in range(4):
            walls[ey][ex][d] = False


def get_random_start_position():
    max_attempts = 100
    for _ in range(max_attempts):
        x = random.randint(1, COLS - 2)
        y = random.randint(1, ROWS - 2)
        if not is_wall_cell(x, y) and (x, y) not in exit_cells:
            return (x, y)
    return (1, 1)


def draw_maze():
    canvas.delete("all")
    canvas.create_rectangle(0, 0, COLS * CELL_SIZE, ROWS * CELL_SIZE, fill=MAZE_BG, outline="")

    for y in range(ROWS):
        for x in range(COLS):
            cx, cy = x * CELL_SIZE, y * CELL_SIZE
            wN, wE, wS, wW = walls[y][x]

            if wN:
                canvas.create_line(cx, cy, cx + CELL_SIZE, cy, fill=WALL_COLOR, width=3)
            if wE:
                canvas.create_line(cx + CELL_SIZE, cy, cx + CELL_SIZE, cy + CELL_SIZE, fill=WALL_COLOR, width=3)
            if wS:
                canvas.create_line(cx, cy + CELL_SIZE, cx + CELL_SIZE, cy + CELL_SIZE, fill=WALL_COLOR, width=3)
            if wW:
                canvas.create_line(cx, cy, cx, cy + CELL_SIZE, fill=WALL_COLOR, width=3)


def draw_player():
    global player_item
    if player_item:
        canvas.delete(player_item)
    x, y = player
    cx = x * CELL_SIZE + CELL_SIZE // 2
    cy = y * CELL_SIZE + CELL_SIZE // 2

    radius = CELL_SIZE * 0.3
    player_item = canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, fill=PLAYER_COLOR, outline="#c0392b", width=2)

    small_radius = radius * 0.3
    canvas.create_oval(cx - radius / 2 - small_radius / 2, cy - radius / 2 - small_radius / 2, cx - radius / 2 + small_radius / 2, cy - radius / 2 + small_radius / 2, fill="white", outline="")
    canvas.create_oval(cx + radius / 2 - small_radius / 2, cy - radius / 2 - small_radius / 2, cx + radius / 2 + small_radius / 2, cy - radius / 2 + small_radius / 2, fill="white", outline="")

def draw_exits():
    global exit_items
    for exit_item in exit_items:
        canvas.delete(exit_item)
    exit_items = []

    for exit_cell in exit_cells:
        x, y = exit_cell
        cx = x * CELL_SIZE + CELL_SIZE // 2
        cy = y * CELL_SIZE + CELL_SIZE // 2

        door_width = CELL_SIZE * 0.6
        door_height = CELL_SIZE * 0.8

        exit_item = canvas.create_rectangle(cx - door_width / 2, cy - door_height / 2, cx + door_width / 2, cy + door_height / 2, fill=EXIT_COLOR, outline="#219652", width=2)
        exit_items.append(exit_item)

        handle_size = CELL_SIZE * 0.08
        canvas.create_oval(cx + door_width / 4 - handle_size / 2, cy - handle_size / 2, cx + door_width / 4 + handle_size / 2, cy + handle_size / 2, fill="#f1c40f", outline="")

        canvas.create_text(cx, cy, text="EXIT", font=("Arial", 8, "bold"), fill="white", tags="exit")

def reset_game():
    global player, game_over, running_search, current_direction, visited_cells, path_history
    if running_search:
        return
    generate_maze()
    generate_exits()
    player = get_random_start_position()
    current_direction = random.choice(["N", "E", "S", "W"])
    game_over = False
    running_search = False
    visited_cells = set()
    path_history = []
    draw_maze()
    draw_exits()
    draw_player()
    canvas.delete("search_vis")
    canvas.delete("path")
def get_right_hand_directions(current_dir):
    if current_dir == "N":
        return ["E", "N", "W", "S"]
    elif current_dir == "E":
        return ["S", "E", "N", "W"]
    elif current_dir == "S":
        return ["W", "S", "E", "N"]
    elif current_dir == "W":
        return ["N", "W", "S", "E"]
def can_move(x, y, direction):
    dx, dy, wall_idx = DIRECTIONS[direction]
    nx, ny = x + dx, y + dy
    if not (0 <= nx < COLS and 0 <= ny < ROWS):
        return False
    if walls[y][x][wall_idx]:
        return False
    if is_wall_cell(nx, ny):
        return False
    return True
def is_wall_cell(x, y):
    return all(walls[y][x])
def start_right_hand():
    global running_search, game_over, current_direction, visited_cells, path_history
    if running_search or game_over:
        return
    canvas.delete("search_vis")
    canvas.delete("path")
    running_search = True
    visited_cells = set()
    path_history = [(player, current_direction)]
    run_right_hand_step()
def run_right_hand_step():
    global player, game_over, running_search, current_direction, visited_cells, path_history
    if game_over or not running_search:
        return
    x, y = player
    if (x, y) in exit_cells:
        draw_correct_path()
        game_over = True
        running_search = False
        messagebox.showinfo("Победа", f"Паучок нашёл выход")
        return
    visited_cells.add((x, y))
    directions_to_try = get_right_hand_directions(current_direction)
    moved = False
    for new_direction in directions_to_try:
        if can_move(x, y, new_direction):
            dx, dy, _ = DIRECTIONS[new_direction]
            new_x, new_y = x + dx, y + dy
            if (new_x, new_y) not in visited_cells:
                player = (new_x, new_y)
                current_direction = new_direction
                path_history.append((player, current_direction))
                moved = True
                break
    if not moved:
        if len(path_history) > 1:
            path_history.pop()
            player, current_direction = path_history[-1]
        else:
            running_search = False
            messagebox.showinfo("Поиск завершен", "Паучок зашел в тупик")
            return
    # Сначала рисуем лабиринт и выходы
    draw_maze()
    draw_exits()
    # Затем рисуем посещенные клетки
    for visited_cell in visited_cells:
        vx, vy = visited_cell
        vcx = vx * CELL_SIZE + CELL_SIZE // 2
        vcy = vy * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE * 0.15
        canvas.create_oval(vcx - radius, vcy - radius, vcx + radius, vcy + radius, fill=VISITED_COLOR, outline="", tags="search_vis")
    # И только потом рисуем игрока поверх всего
    draw_player()
    speed_ms = 150
    canvas.after(speed_ms, run_right_hand_step)

def draw_correct_path():
    unique_path_cells = []
    seen = set()
    for cell, _ in path_history:
        if cell not in seen:
            unique_path_cells.append(cell)
            seen.add(cell)

    for i, (x, y) in enumerate(unique_path_cells):
        cx = x * CELL_SIZE + CELL_SIZE // 2
        cy = y * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE * 0.18
        canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius, fill=PATH_COLOR, outline="#8e44ad", width=1, tags="path")


def main():
    global canvas, player
    root = tk.Tk()
    root.title("Лабиринт")
    root.configure(bg="white")

    header = tk.Frame(root, bg="white")
    header.pack(fill=tk.X, pady=10)

    title_label = tk.Label(header, text="🐛 Лабиринт с паучком",font=("Arial", 16, "bold"),fg=WALL_COLOR, bg="white")
    title_label.pack()

    canvas = tk.Canvas(root, width=COLS * CELL_SIZE, height=ROWS * CELL_SIZE, bg=MAZE_BG, highlightthickness=2, highlightbackground=WALL_COLOR)
    canvas.pack(pady=15)

    bottom = tk.Frame(root, bg="white")
    bottom.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    start_btn = tk.Button(bottom, text="🚀 Запуск паучка", command=start_right_hand,font=("Arial", 12, "bold"), bg=BUTTON_COLOR, fg="white",relief="raised", padx=20, pady=8, bd=0,cursor="hand2")
    start_btn.pack(side=tk.LEFT, padx=20)

    reset_btn = tk.Button(bottom, text="🔄 Новый лабиринт", command=reset_game,font=("Arial", 12, "bold"), bg=BUTTON_COLOR, fg="white",relief="raised", padx=20, pady=8, bd=0,cursor="hand2")
    reset_btn.pack(side=tk.LEFT, padx=20)

    legend = tk.Frame(root, bg="white")
    legend.pack(side=tk.BOTTOM, pady=5)
    legend_text = "🐛 Паучок 🔵 Посещенные клетки  🟣 Найденный путь"
    legend_label = tk.Label(legend, text=legend_text, font=("Arial", 10),fg=WALL_COLOR, bg="white")
    legend_label.pack()
    generate_maze()
    generate_exits()
    player = get_random_start_position()
    draw_maze()
    draw_exits()
    draw_player()
    root.mainloop()

if __name__ == "__main__":
    main()
