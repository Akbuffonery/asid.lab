import numpy as np
import timeit
import matplotlib.pyplot as plt
import math
def F(n):
    if n < 1:
        raise ValueError("n должно быть положительным")
    if n == 1:
        return -1
    return math.factorial(2 * n - 1) - G(n - 1)
def G(n):
    if n < 1:
        raise ValueError("n должно быть положительным")
    if n == 1:
        return -1
    return F(n - 1)
def iterative(n):
    if n < 1:
        raise ValueError("n должно быть положительным целым числом")
    if n == 1:
        return (1, 1)
    F_prev, G_prev = 1, 1
    sign = 1  # Начинаем с n=2, (-1)^2 = 1
    for i in range(2, n + 1):
        sign *= -1
        fact = math.factorial(2 * i - 1)
        F_current = sign * fact - G_prev
        G_current = F_prev
        F_prev, G_prev = F_current, G_current
        fact *= (2 * i) * (2 * i + 1)
    return (F_prev, G_prev)
def measure_time(func, n, number=1):
    from functools import partial
    test_func = partial(func, n)
    t = timeit.timeit(test_func, number=number)
    return t / number
def main():
    ns = np.arange(1, 21)
    f_recursive_times = []
    g_recursive_times = []
    f_iterative_times = []
    g_iterative_times = []
    max_n_recursive = 0
    for n in ns:
        try:
            t = measure_time(F, n)
            f_recursive_times.append(t)
            t = measure_time(G, n)
            g_recursive_times.append(t)
            max_n_recursive = n
        except (RecursionError, OverflowError, ValueError) as e:
            f_recursive_times.append(np.nan)
            g_recursive_times.append(np.nan)
        # Для итеративного метода
        t = measure_time(lambda x: iterative(x)[0], n)
        f_iterative_times.append(t)
        t = measure_time(lambda x: iterative(x)[1], n)
        g_iterative_times.append(t)
    print("\n n | F_rec_time | G_rec_time | F_iter_time | G_iter_time")
    for i in range(len(ns)):
        print(
            f"{ns[i]:2d} | {f_recursive_times[i]:10.6f} | {g_recursive_times[i]:10.6f} | {f_iterative_times[i]:11.6f} | {g_iterative_times[i]:11.6f}")
    # Строим графики только для тех n, где рекурсивные методы работали
    valid_ns = ns[:max_n_recursive]
    valid_f_rec = f_recursive_times[:max_n_recursive]
    valid_g_rec = g_recursive_times[:max_n_recursive]
    plt.figure(figsize=(12, 6))
    plt.plot(valid_ns, valid_f_rec, 'r--', label='F rec')
    plt.plot(valid_ns, valid_g_rec, 'b--', label='G rec')
    plt.plot(ns, f_iterative_times, 'r-', label='F iter')
    plt.plot(ns, g_iterative_times, 'b-', label='G iter')
    plt.xlabel('n')
    plt.ylabel('Time (seconds)')
    plt.title('Сравнение времени выполнения для рекуррентных формул')
    plt.legend()
    plt.grid(True)
    plt.yscale('log')
    plt.show()
if __name__ == "__main__":
    main()