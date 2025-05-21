import itertools
import tkinter as tk
from tkinter import scrolledtext, messagebox
class TeamOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Оптимизатор команды")
        self.root.geometry("800x600")
        # Переменные для хранения данных
        self.candidates = {}
        self.min_mid_avg = tk.DoubleVar(value=7.0)
        self.min_jun_avg = tk.DoubleVar(value=5.0)
        self.create_widgets()
    def create_widgets(self):
        # Фрейм для ввода данных
        input_frame = tk.LabelFrame(self.root, text="Ввод данных", padx=10, pady=10)
        input_frame.pack(padx=10, pady=5, fill=tk.X)
        # Поля для ввода минимальных средних значений
        tk.Label(input_frame, text="Минимальный средний уровень мидлов:").grid(row=0, column=0, sticky=tk.W)
        tk.Entry(input_frame, textvariable=self.min_mid_avg, width=10).grid(row=0, column=1, sticky=tk.W)
        tk.Label(input_frame, text="Минимальный средний уровень джунов:").grid(row=1, column=0, sticky=tk.W)
        tk.Entry(input_frame, textvariable=self.min_jun_avg, width=10).grid(row=1, column=1, sticky=tk.W)
        # Текстовое поле для ввода кандидатов
        tk.Label(input_frame, text="Введите кандидатов в формате 'ID:уровень' (по одному на строку):").grid(row=2, column=0, columnspan=2, sticky=tk.W)
        self.candidates_text = tk.Text(input_frame, height=10, width=40)
        self.candidates_text.grid(row=3, column=0, columnspan=2, sticky=tk.W)
        self.candidates_text.insert(tk.END, "1:8\n2:10\n3:7\n4:6\n5:9\n6:4")
        # Кнопка для запуска оптимизации
        tk.Button(input_frame, text="Найти оптимальную команду", command=self.optimize_team).grid(row=4, column=0, columnspan=2, pady=10)
        # Фрейм для вывода результатов
        output_frame = tk.LabelFrame(self.root, text="Результаты", padx=10, pady=10)
        output_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        # Поле с прокруткой для вывода результатов
        self.output_area = scrolledtext.ScrolledText(output_frame, width=70, height=20)
        self.output_area.pack(fill=tk.BOTH, expand=True)
    def parse_candidates(self):
        self.candidates = {}
        text = self.candidates_text.get("1.0", tk.END).strip()
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
            try:
                cid, level = line.split(':')
                self.candidates[int(cid)] = int(level)
            except ValueError:
                messagebox.showerror("Ошибка", f"Неправильный формат строки: {line}")
                return False
        return True
    def team_score(self, team):
        mids, juns = team
        return sum(self.candidates[m] for m in mids) + sum(self.candidates[j] for j in juns)
    def get_possible_roles(self):
        # Кандидаты, которые могут быть мидлами (уровень ≥ 6)
        possible_mids = [cid for cid, lvl in self.candidates.items() if lvl >= 6]
        # Кандидаты, которые могут быть джунами (уровень ≥ 4)
        possible_juns = [cid for cid, lvl in self.candidates.items() if lvl >= 4]
        return possible_mids, possible_juns
    def optimize_team(self):
        if not self.parse_candidates():
            return
        min_mid = self.min_mid_avg.get()
        min_jun = self.min_jun_avg.get()
        possible_mids, possible_juns = self.get_possible_roles()
        results = []
        # Очищаем поле вывода
        self.output_area.delete('1.0', tk.END)
        # Перебираем возможных мидлов
        for mids in itertools.combinations(possible_mids, 2):
            mid_avg = sum(self.candidates[m] for m in mids) / 2
            if mid_avg < min_mid:
                continue
            # Оставшиеся кандидаты (кроме выбранных мидлов)
            remaining = [cid for cid in possible_juns if cid not in mids]
            # Перебираем возможных джунов
            for juns in itertools.combinations(remaining, 2):
                jun_avg = sum(self.candidates[j] for j in juns) / 2
                if jun_avg >= min_jun:
                    results.append((mids, juns))
        if not results:
            self.output_area.insert(tk.END, "Не найдено подходящих команд с заданными параметрами.")
            return
        # Находим оптимальную команду
        optimal_team = max(results, key=self.team_score)
        optimal_score = self.team_score(optimal_team)
        # Выводим результаты
        self.output_area.insert(tk.END, "=== Оптимальная команда ===\n")
        self.output_area.insert(tk.END,
                                f"Мидлы: {optimal_team[0]} (уровни: {[self.candidates[m] for m in optimal_team[0]]}, " +
                                f"средний: {sum(self.candidates[m] for m in optimal_team[0]) / 2:.1f})\n")
        self.output_area.insert(tk.END,
                                f"Джуны: {optimal_team[1]} (уровни: {[self.candidates[j] for j in optimal_team[1]]}, " +
                                f"средний: {sum(self.candidates[j] for j in optimal_team[1]) / 2:.1f})\n")
        self.output_area.insert(tk.END, f"Общий уровень команды: {optimal_score}\n")
        self.output_area.insert(tk.END, f"Средний уровень: {optimal_score / 4:.2f}\n\n")
        self.output_area.insert(tk.END, f"=== Все подходящие варианты ({len(results)}) ===\n")
        for idx, (mids, juns) in enumerate(results, 1):
            score = self.team_score((mids, juns))
            self.output_area.insert(tk.END,
                                    f"{idx}. Мидлы: {mids} (ср. {sum(self.candidates[m] for m in mids) / 2:.1f}), " +
                                    f"Джуны: {juns} (ср. {sum(self.candidates[j] for j in juns) / 2:.1f}), " +
                                    f"Общий: {score}\n")
if __name__ == "__main__":
    root = tk.Tk()
    app = TeamOptimizerApp(root)
    root.mainloop()