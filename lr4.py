import numpy as np
import matplotlib.pyplot as plt
def read_matrix_from_file(filename):
    with open(filename, 'r') as f:
        return np.array([list(map(int, line.split())) for line in f])
def main():
    k = int(input("Введите k: "))
    n = int(input("Введите размер матрицы N: "))
    with open('matrix.txt') as f: #!!!Главное чтобы размер матрицы в файле была равна вводу k и n.
        A = np.array([list(map(int, line.split()))[:n] for line in f][:n])
    print("Исходная матрица A:\n", A)
    F = A.copy()
    half = n // 2
    C = F[:half, half:] if n % 2 == 0 else F[:half, half + 1:] # Выделяем подматрицу C
    zero_count = sum(1 for i in range(C.shape[0]) # Подсчет нулей с четной суммой индексов
                     for j in range(C.shape[1])
                     if (i + j) % 2 == 0 and C[i, j] == 0)
    perimeter = [] # Произведение по периметру C
    if C.size > 0:
        perimeter.extend(C[0, :])  # Верхняя строка
        if C.shape[0] > 1:
            perimeter.extend(C[-1, :])  # Нижняя строка
        if C.shape[1] > 1:
            perimeter.extend(C[1:-1, 0])  # Левый столбец
            perimeter.extend(C[1:-1, -1])  # Правый столбец
    perimeter_product = np.prod(perimeter) if perimeter else 0
    if zero_count > perimeter_product: # Преобразование матрицы F
        if n % 2 == 0: #Меняем B и C симметрично
            B = F[half:, half:].copy()
            F[half:, half:] = np.fliplr(C.T)
            F[:half, half:] = np.fliplr(B.T)
        else:
            B = F[half + 1:, half + 1:].copy()
            F[half + 1:, half + 1:] = np.fliplr(C.T)
            F[:half, half + 1:] = np.fliplr(B.T)
    else:
        if n % 2 == 0: #Меняем C и E несимметрично
            E = F[half:, :half].copy()
            F[:half, half:] = E
            F[half:, :half] = C
        else:
            E = F[half + 1:, :half + 1].copy()
            F[:half, half + 1:] = E
            F[half + 1:, :half + 1] = C
    print("\nПреобразованная матрица F:\n", F)
    det_A = np.linalg.det(A)
    trace_F = np.trace(F)
    if det_A > trace_F:
        A_inv = np.linalg.inv(A)
        F_inv = np.linalg.inv(F)
        result = A_inv @ A.T - k * F_inv
    else:
        G = np.tril(A)
        result = (A + G - F) * k
    print("\nРезультат вычислений (A + tril(A) - F) * K:\n", result)
    plt.figure(figsize=(15, 5))
    plt.subplot(131) # 1. Визуализация матрицы F
    plt.imshow(F, cmap='viridis')
    plt.colorbar()
    plt.title("Матрица F")
    plt.subplot(132) # 2. Сумма элементов по строкам
    plt.plot(F.sum(axis=1), 'o-')
    plt.title("Сумма по строкам")
    plt.grid(True)
    plt.subplot(133) # 3. Сумма элементов по столбцам
    plt.plot(F.sum(axis=0), 's-')
    plt.title("Сумма по столбцам")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    main()