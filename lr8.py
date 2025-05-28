import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re
import math
from collections import defaultdict
class HousingContract:
    def __init__(self, contract_id="", property_type="", manager="", price=0, date=""):
        self.contract_id = contract_id
        self.property_type = property_type
        self.manager = manager
        self.price = price
        self.date = date
    def __str__(self):
        return f"{self.contract_id},{self.property_type},{self.manager},{self.price},{self.date}"
class HousingContractApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление договорами на продажу жилья")
        self.contracts = []
        # Создание главного фрейма
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        # Создание холста для отрисовки диаграмм
        self.canvas = tk.Canvas(self.main_frame, width=500, height=400, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # Панель управления
        control_frame = tk.Frame(self.main_frame, padx=10, pady=10)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        # Кнопки управления
        tk.Button(control_frame, text="Загрузить из файла", command=self.load_from_file).pack(fill=tk.X, pady=5)
        tk.Button(control_frame, text="Сохранить в файл", command=self.save_to_file).pack(fill=tk.X, pady=5)
        tk.Button(control_frame, text="Добавить договор", command=self.add_contract_dialog).pack(fill=tk.X, pady=5)
        tk.Button(control_frame, text="Сегментировать по видам жилья", command=self.segment_by_property_type).pack(fill=tk.X, pady=5)
        tk.Button(control_frame, text="Сегментировать по менеджерам", command=self.segment_by_manager).pack(fill=tk.X,pady=5)
        tk.Button(control_frame, text="Очистить все", command=self.clear_all).pack(fill=tk.X, pady=5)
        # Таблица для отображения договоров
        self.tree = ttk.Treeview(self.main_frame, columns=("ID", "Type", "Manager", "Price", "Date"), show="headings")
        self.tree.heading("ID", text="ID договора")
        self.tree.heading("Type", text="Тип жилья")
        self.tree.heading("Manager", text="Менеджер")
        self.tree.heading("Price", text="Цена")
        self.tree.heading("Date", text="Дата")
        self.tree.pack(fill=tk.BOTH, expand=True)
        # Информационная метка
        self.info_label = tk.Label(control_frame, text="Всего договоров: 0", wraplength=200)
        self.info_label.pack(fill=tk.X, pady=10)
    def update_info_label(self):
        self.info_label.config(text=f"Всего договоров: {len(self.contracts)}")
    def update_treeview(self):
        # Очищаем текущее содержимое таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        # Заполняем таблицу данными
        for contract in self.contracts:
            self.tree.insert("", "end", values=(
                contract.contract_id,
                contract.property_type,
                contract.manager,
                contract.price,
                contract.date
            ))
    def load_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt")])
        if not file_path:
            return
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                new_contracts = []
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    # Разделяем строку по запятым или точкам с запятой
                    parts = re.split(r'[,;]', line)
                    if len(parts) < 5:
                        continue  # Недостаточно данных для договора
                    try:
                        contract_id = parts[0].strip()
                        property_type = parts[1].strip()
                        manager = parts[2].strip()
                        price = float(parts[3].strip())
                        date = parts[4].strip()
                        new_contracts.append(HousingContract(contract_id, property_type, manager, price, date))
                    except ValueError:
                        continue  # Пропускаем строки с некорректными данными
                if new_contracts:
                    self.contracts = new_contracts
                    self.update_treeview()
                    self.update_info_label()
                    self.canvas.delete("all")
                    messagebox.showinfo("Успех", f"Загружено {len(new_contracts)} договоров")
                else:
                    messagebox.showwarning("Предупреждение", "Файл не содержит корректных данных о договорах")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")
    def save_to_file(self):
        if not self.contracts:
            messagebox.showwarning("Предупреждение", "Нет договоров для сохранения")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt")]
        )
        if not file_path:
            return
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                for contract in self.contracts:
                    file.write(
                        f"{contract.contract_id},{contract.property_type},{contract.manager},{contract.price},{contract.date}\n")
            messagebox.showinfo("Успех", f"Сохранено {len(self.contracts)} договоров")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")
    def add_contract_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить договор")
        # Поля ввода
        tk.Label(dialog, text="ID договора:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        id_entry = tk.Entry(dialog)
        id_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(dialog, text="Тип жилья:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        type_var = tk.StringVar()
        type_combobox = ttk.Combobox(dialog, textvariable=type_var,                                    values=["Квартира", "Дом", "Таунхаус", "Комната", "Апартаменты"])
        type_combobox.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(dialog, text="Менеджер:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        manager_entry = tk.Entry(dialog)
        manager_entry.grid(row=2, column=1, padx=5, pady=5)
        tk.Label(dialog, text="Цена (В рублях):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        price_entry = tk.Entry(dialog)
        price_entry.grid(row=3, column=1, padx=5, pady=5)
        tk.Label(dialog, text="Дата (ДД.ММ.ГГГГ):").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        date_entry = tk.Entry(dialog)
        date_entry.grid(row=4, column=1, padx=5, pady=5)
        def add_contract():
            try:
                contract_id = id_entry.get().strip()
                property_type = type_var.get().strip()
                manager = manager_entry.get().strip()
                price = float(price_entry.get().strip())
                date = date_entry.get().strip()
                if not contract_id or not property_type or not manager or not date:
                    raise ValueError("Все поля должны быть заполнены")
                # Проверка формата даты (упрощенная)
                if not re.match(r'\d{2}\.\d{2}\.\d{4}', date):
                    raise ValueError("Дата должна быть в формате ДД.ММ.ГГГГ")
                self.contracts.append(HousingContract(contract_id, property_type, manager, price, date))
                self.update_treeview()
                self.update_info_label()
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Ошибка", f"Некорректные данные: {str(e)}")
        tk.Button(dialog, text="Добавить", command=add_contract).grid(row=5, column=0, columnspan=2, pady=10)
    def segment_by_property_type(self):
        if not self.contracts:
            messagebox.showwarning("Предупреждение", "Нет договоров для анализа")
            return
        # Собираем статистику по типам жилья
        type_stats = defaultdict(int)
        for contract in self.contracts:
            type_stats[contract.property_type] += 1
        # Рисуем круговую диаграмму
        self.draw_pie_chart(type_stats, "Распределение договоров по типам жилья")
    def segment_by_manager(self):
        if not self.contracts:
            messagebox.showwarning("Предупреждение", "Нет договоров для анализа")
            return
        # Собираем статистику по менеджерам
        manager_stats = defaultdict(int)
        for contract in self.contracts:
            manager_stats[contract.manager] += 1
        # Рисуем круговую диаграмму
        self.draw_pie_chart(manager_stats, "Распределение договоров по менеджерам")
    def draw_pie_chart(self, data, title):
        self.canvas.delete("all")
        if not data:
            return
        # Размеры холста
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        center_x = width // 2
        center_y = height // 2
        radius = min(center_x, center_y) * 0.8
        # Цвета для сегментов
        colors = [
            "#FF9999", "#66B2FF", "#99FF99", "#FFCC99", "#FF99FF",
            "#FFFF99", "#99FFFF", "#C2C2F0", "#FF6666", "#66FF66"
        ]
        # Общее количество (для расчета процентов)
        total = sum(data.values())
        # Начальный угол
        start_angle = 0
        # Рисуем сегменты
        for i, (label, value) in enumerate(data.items()):
            # Вычисляем угол для текущего сегмента
            angle = 360 * value / total
            # Вычисляем конечный угол
            end_angle = start_angle + angle
            # Рисуем сектор
            self.canvas.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=start_angle, extent=angle,
                fill=colors[i % len(colors)], outline="black"
            )
            # Вычисляем середину угла для подписи
            mid_angle = start_angle + angle / 2
            mid_angle_rad = math.radians(mid_angle)
            # Позиция для подписи (немного внутри от края)
            label_radius = radius * 0.7
            label_x = center_x + label_radius * math.cos(mid_angle_rad)
            label_y = center_y - label_radius * math.sin(mid_angle_rad)
            # Подпись (значение и процент)
            percent = value / total * 100
            self.canvas.create_text(
                label_x, label_y,
                text=f"{label}\n{value} ({percent:.1f}%)",
                font=("Arial", 8)
            )
            # Обновляем начальный угол для следующего сегмента
            start_angle = end_angle
        # Заголовок диаграммы
        self.canvas.create_text(
            center_x, 20,
            text=title,
            font=("Arial", 12, "bold")
        )
    def show_all_contracts(self):
        self.canvas.delete("all")
        self.update_treeview()
    def clear_all(self):
        if messagebox.askyesno("Подтверждение", "Удалить все договоры?"):
            self.contracts = []
            self.update_treeview()
            self.update_info_label()
            self.canvas.delete("all")
if __name__ == "__main__":
    root = tk.Tk()
    app = HousingContractApp(root)
    root.geometry("900x600")
    root.mainloop()
