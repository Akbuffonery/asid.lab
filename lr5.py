import itertools
import time
# Список претендентов
candidates = [1, 2, 3, 4, 5, 6]
# 1. Алгоритмический подход
def algorithmic_approach(candidates):
    def generate_combinations(start, mid_selected, jun_selected, current, results):
        if len(mid_selected) == 2 and len(jun_selected) == 2:
            results.append((tuple(mid_selected), tuple(jun_selected)))
            return
        if start >= len(candidates):
            return
        # Вариант 1: не берем текущего кандидата
        generate_combinations(start + 1, mid_selected.copy(), jun_selected.copy(), current, results)
        # Вариант 2: берем как мидла (если еще есть места)
        if len(mid_selected) < 2:
            new_mid = mid_selected.copy()
            new_mid.append(candidates[start])
            generate_combinations(start + 1, new_mid, jun_selected.copy(), current, results)
        # Вариант 3: берем как юниора (если еще есть места)
        if len(jun_selected) < 2:
            new_jun = jun_selected.copy()
            new_jun.append(candidates[start])
            generate_combinations(start + 1, mid_selected.copy(), new_jun, current, results)
    results = []
    generate_combinations(0, [], [], [], results)
    return results
# 2. Подход с использованием itertools
def itertools_approach(candidates):
    # Все возможные комбинации 2 мидлов из 6 кандидатов
    mid_combinations = itertools.combinations(candidates, 2)
    results = []
    for mids in mid_combinations:
        # Оставшиеся кандидаты (не выбранные в мидлы)
        remaining = [c for c in candidates if c not in mids]
        # Все возможные комбинации 2 юниоров из оставшихся 4
        jun_combinations = itertools.combinations(remaining, 2)
        for juns in jun_combinations:
            results.append((mids, juns))
    return results
# Замер времени выполнения
start_time = time.time()
alg_result = algorithmic_approach(candidates)
alg_time = time.time() - start_time
start_time = time.time()
itertools_result = itertools_approach(candidates)
itertools_time = time.time() - start_time
# Проверка, что результаты совпадают
assert len(alg_result) == len(itertools_result)
assert set(alg_result) == set(itertools_result)
# Вывод результатов
print(f"Алгоритмический подход: {len(alg_result)} вариантов, время: {alg_time:.6f} сек")
print(f"Подход с itertools: {len(itertools_result)} вариантов, время: {itertools_time:.6f} сек")
print(f"Разница во времени: {abs(alg_time - itertools_time):.6f} сек")