import tkinter as tk
from tkinter import filedialog, messagebox
import re
class Segment:
    def __init__(self, x1=0, y1=0, x2=0, y2=0, color="black"):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
    def segmentate(self, parts):
        """Разделение отрезка на равные части"""
        if parts <= 1:
            return [self]
        segments = []
        dx = (self.x2 - self.x1) / parts
        dy = (self.y2 - self.y1) / parts
        for i in range(parts):
            seg = Segment(
                self.x1 + i * dx,
                self.y1 + i * dy,
                self.x1 + (i + 1) * dx,
                self.y1 + (i + 1) * dy,
                self.color
            )
            segments.append(seg)
        return segments
    def move(self, dx, dy):
        """Перемещение отрезка на плоскости"""
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
    def recolor(self, new_color):
        """Изменение цвета отрезка"""
        self.color = new_color
    def length(self):
        """Вычисление длины отрезка"""
        return ((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2) ** 0.5
    def __str__(self):
        return f"{self.x1},{self.y1},{self.x2},{self.y2},{self.color}"
class SegmentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление отрезками")
        self.segments = []
        self.selected_segment = None
        # Создание холста для отрисовки
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.select_segment)
        # Панель управления
        control_frame = tk.Frame(root, padx=10, pady=10)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        # Кнопки управления
        tk.Button(control_frame, text="Загрузить из файла", command=self.load_from_file).pack(fill=tk.X, pady=5)
        tk.Button(control_frame, text="Сохранить в файл", command=self.save_to_file).pack(fill=tk.X, pady=5)
        tk.Button(control_frame, text="Добавить отрезок", command=self.add_segment_dialog).pack(fill=tk.X, pady=5)
        tk.Button(control_frame, text="Сегментировать", command=self.segmentate_dialog).pack(fill=tk.X, pady=5)
        tk.Button(control_frame, text="Переместить", command=self.move_dialog).pack(fill=tk.X, pady=5)
        tk.Button(control_frame, text="Изменить цвет", command=self.recolor_dialog).pack(fill=tk.X, pady=5)
        tk.Button(control_frame, text="Очистить все", command=self.clear_all).pack(fill=tk.X, pady=5)
        # Информационная панель
        self.info_label = tk.Label(control_frame, text="Выберите отрезок", wraplength=200)
        self.info_label.pack(fill=tk.X, pady=10)
        # Отрисовка осей координат
        self.draw_axes()
    def draw_axes(self):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        # Ось X
        self.canvas.create_line(0, height // 2, width, height // 2, fill="gray", dash=(2, 2))
        # Ось Y
        self.canvas.create_line(width // 2, 0, width // 2, height, fill="gray", dash=(2, 2))
        # Подписи осей
        self.canvas.create_text(width - 10, height // 2 - 10, text="X", fill="gray")
        self.canvas.create_text(width // 2 + 10, 10, text="Y", fill="gray")
    def redraw_segments(self):
        self.canvas.delete("segment")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        # Центр координат
        center_x = width // 2
        center_y = height // 2
        for i, segment in enumerate(self.segments):
            # Преобразование координат (центр холста - начало координат)
            x1 = center_x + segment.x1
            y1 = center_y - segment.y1
            x2 = center_x + segment.x2
            y2 = center_y - segment.y2
            # Отрисовка отрезка
            line = self.canvas.create_line(x1, y1, x2, y2, fill=segment.color, width=2, tags="segment")
            # Если это выбранный отрезок, выделяем его
            if segment == self.selected_segment:
                self.canvas.itemconfig(line, width=4)
                self.canvas.create_oval(x1 - 3, y1 - 3, x1 + 3, y1 + 3, fill="red", outline="red", tags="segment")
                self.canvas.create_oval(x2 - 3, y2 - 3, x2 + 3, y2 + 3, fill="red", outline="red", tags="segment")
        # Обновление информации о выбранном отрезке
        self.update_segment_info()
    def select_segment(self, event):
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width // 2
        center_y = height // 2
        # Преобразование координат клика в систему координат отрезков
        click_x = event.x - center_x
        click_y = center_y - event.y
        min_distance = float('inf')
        selected = None
        for segment in self.segments:
            # Проверка расстояния от точки до отрезка
            distance = self.point_to_segment_distance(click_x, click_y, segment)
            if distance < min_distance and distance < 10:  # 10 пикселей - радиус выбора
                min_distance = distance
                selected = segment
        self.selected_segment = selected
        self.redraw_segments()
    def point_to_segment_distance(self, x, y, segment):
        """Вычисление расстояния от точки до отрезка"""
        x1, y1, x2, y2 = segment.x1, segment.y1, segment.x2, segment.y2
        # Если отрезок вырожден в точку
        if x1 == x2 and y1 == y2:
            return ((x - x1) ** 2 + (y - y1) ** 2) ** 0.5
        # Параметрическое представление отрезка: (x1 + t*(x2-x1), y1 + t*(y2-y1)), t ∈ [0,1]
        # Находим t, соответствующее проекции точки на прямую
        t = ((x - x1) * (x2 - x1) + (y - y1) * (y2 - y1)) / ((x2 - x1) ** 2 + (y2 - y1) ** 2)
        # Ограничиваем t интервалом [0,1]
        t = max(0, min(1, t))
        proj_x = x1 + t * (x2 - x1)
        proj_y = y1 + t * (y2 - y1)
        return ((x - proj_x) ** 2 + (y - proj_y) ** 2) ** 0.5
    def update_segment_info(self):
        if self.selected_segment:
            info = f"Отрезок:\n"
            info += f"Начало: ({self.selected_segment.x1:.1f}, {self.selected_segment.y1:.1f})\n"
            info += f"Конец: ({self.selected_segment.x2:.1f}, {self.selected_segment.y2:.1f})\n"
            info += f"Длина: {self.selected_segment.length():.1f}\n"
            info += f"Цвет: {self.selected_segment.color}"
        else:
            info = "Отрезок не выбран"
        self.info_label.config(text=info)
    def load_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt")])
        if not file_path:
            return
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                new_segments = []
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    # Разделяем строку по запятым или пробелам
                    parts = re.split(r'[, \t]+', line)
                    if len(parts) < 4:
                        continue  # Недостаточно данных для отрезка
                    try:
                        x1 = float(parts[0])
                        y1 = float(parts[1])
                        x2 = float(parts[2])
                        y2 = float(parts[3])
                        color = parts[4] if len(parts) > 4 else "black"
                        new_segments.append(Segment(x1, y1, x2, y2, color))
                    except ValueError:
                        continue  # Пропускаем строки с некорректными данными
                if new_segments:
                    self.segments = new_segments
                    self.selected_segment = None
                    self.redraw_segments()
                    messagebox.showinfo("Успех", f"Загружено {len(new_segments)} отрезков")
                else:
                    messagebox.showwarning("Предупреждение", "Файл не содержит корректных данных об отрезках")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")
    def save_to_file(self):
        if not self.segments:
            messagebox.showwarning("Предупреждение", "Нет отрезков для сохранения")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt")])
        if not file_path:
            return
        try:
            with open(file_path, 'w') as file:
                for segment in self.segments:
                    file.write(f"{segment.x1},{segment.y1},{segment.x2},{segment.y2},{segment.color}\n")
            messagebox.showinfo("Успех", f"Сохранено {len(self.segments)} отрезков")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")
    def add_segment_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить отрезок")
        tk.Label(dialog, text="X начальная:").grid(row=0, column=0, padx=5, pady=5)
        x1_entry = tk.Entry(dialog)
        x1_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(dialog, text="Y начальная:").grid(row=1, column=0, padx=5, pady=5)
        y1_entry = tk.Entry(dialog)
        y1_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(dialog, text="X конечная:").grid(row=2, column=0, padx=5, pady=5)
        x2_entry = tk.Entry(dialog)
        x2_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Label(dialog, text="Y конечная:").grid(row=3, column=0, padx=5, pady=5)
        y2_entry = tk.Entry(dialog)
        y2_entry.grid(row=3, column=1, padx=5, pady=5)
        tk.Label(dialog, text="Цвет:").grid(row=4, column=0, padx=5, pady=5)
        color_var = tk.StringVar(value="black")
        color_menu = tk.OptionMenu(dialog, color_var, "black", "red", "green", "blue", "yellow", "purple")
        color_menu.grid(row=4, column=1, padx=5, pady=5, sticky="ew")
        def add_segment():
            try:
                x1 = float(x1_entry.get())
                y1 = float(y1_entry.get())
                x2 = float(x2_entry.get())
                y2 = float(y2_entry.get())
                color = color_var.get()
                self.segments.append(Segment(x1, y1, x2, y2, color))
                self.redraw_segments(),
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректные числовые значения")
        tk.Button(dialog, text="Добавить", command=add_segment).grid(row=5, column=0, columnspan=2, pady=10)
    def segmentate_dialog(self):
        if not self.selected_segment:
            messagebox.showwarning("Предупреждение", "Выберите отрезок для сегментации")
            return
        dialog = tk.Toplevel(self.root)
        dialog.title("Сегментировать отрезок")
        tk.Label(dialog, text="Количество частей:").pack(padx=10, pady=5)
        parts_entry = tk.Entry(dialog)
        parts_entry.pack(padx=10, pady=5)
        def segmentate():
            try:
                parts = int(parts_entry.get())
                if parts < 2:
                    raise ValueError("Количество частей должно быть больше 1")
                # Находим индекс выбранного отрезка
                index = self.segments.index(self.selected_segment)
                # Удаляем выбранный отрезок
                self.segments.pop(index)
                # Добавляем новые отрезки
                new_segments = self.selected_segment.segmentate(parts)
                for seg in reversed(new_segments):
                    self.segments.insert(index, seg)
                self.selected_segment = None
                self.redraw_segments()
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Ошибка", str(e))
        tk.Button(dialog, text="Сегментировать", command=segmentate).pack(padx=10, pady=10)
    def move_dialog(self):
        if not self.selected_segment:
            messagebox.showwarning("Предупреждение", "Выберите отрезок для перемещения")
            return
        dialog = tk.Toplevel(self.root)
        dialog.title("Переместить отрезок")
        tk.Label(dialog, text="Смещение по X:").grid(row=0, column=0, padx=5, pady=5)
        dx_entry = tk.Entry(dialog)
        dx_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(dialog, text="Смещение по Y:").grid(row=1, column=0, padx=5, pady=5)
        dy_entry = tk.Entry(dialog)
        dy_entry.grid(row=1, column=1, padx=5, pady=5)
        def move():
            try:
                dx = float(dx_entry.get())
                dy = float(dy_entry.get())
                self.selected_segment.move(dx, dy)
                self.redraw_segments()
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Введите корректные числовые значения")
        tk.Button(dialog, text="Переместить", command=move).grid(row=2, column=0, columnspan=2, pady=10)
    def recolor_dialog(self):
        """Диалог изменения цвета выбранного отрезка"""
        if not self.selected_segment:
            messagebox.showwarning("Предупреждение", "Выберите отрезок для изменения цвета")
            return
        dialog = tk.Toplevel(self.root)
        dialog.title("Изменить цвет отрезка")
        tk.Label(dialog, text="Выберите новый цвет:").pack(padx=10, pady=5)
        color_var = tk.StringVar(value=self.selected_segment.color)
        colors = ["black", "red", "green", "blue", "yellow", "purple", "orange", "brown", "pink"]
        color_menu = tk.OptionMenu(dialog, color_var, *colors)
        color_menu.pack(padx=10, pady=5)
        def recolor():
            self.selected_segment.recolor(color_var.get())
            self.redraw_segments()
            dialog.destroy()
        tk.Button(dialog, text="Изменить", command=recolor).pack(padx=10, pady=10)
    def clear_all(self):
        if messagebox.askyesno("Подтверждение", "Удалить все отрезки?"):
            self.segments = []
            self.selected_segment = None
            self.redraw_segments()
if __name__ == "__main__":
    root = tk.Tk()
    app = SegmentApp(root)
    root.mainloop()