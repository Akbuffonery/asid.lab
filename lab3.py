import random
def create_matrix(N, values=None): # создание матрицы(-10;10)
    return [[values[i * N + j] if values else random.randint(-10, 10) for j in range(N)] for i in range(N)]
def split_matrix(matrix): #Матрица на 4 части
    mid = len(matrix) // 2
    return [row[:mid] for row in matrix[:mid]], [row[mid:] for row in matrix[:mid]], [row[:mid] for row in matrix[mid:]], [row[mid:] for row in matrix[mid:]]
def count_greater_K(area, K): #подсчета количества чисел, больших K
    return sum(1 for row in area for j in range(1, len(row), 2) if row[j] > K)
def product_even(area): #вычисление произведения четных чисел в нечетных строках
    p = 1
    for row in area[::2]:
        for v in row:
            if v % 2 == 0:
                p *= v
    return p
def form_matrix_F(A, K): #формирования матрицы F
    F = A
    a1, a2, a3, a4 = split_matrix(A)
    if count_greater_K(a2, K) < product_even(a3):
        for i in range(len(A) // 2):
            for j in range(len(A) // 2):
                F[i][len(A)//2 + j], F[len(A)//2 + i][j] = F[len(A)//2 + i][j], F[i][len(A)//2 + j]
    else:
        for i in range(len(A) // 2):
            for j in range(len(A) // 2):
                F[i][j], F[len(A)//2 + i][j] = F[len(A)//2 + i][j], F[i][j]
    return F
def multiply_matrix_by_scalar(matrix, scalar): #Умножение матрицы на скаляр
    return [[scalar * v for v in row] for row in matrix]
def multiply_matrices(A, B): #умножение двух матрицы
    return [[sum(A[i][k] * B[k][j] for k in range(len(A))) for j in range(len(A[0]))] for i in range(len(A))]
def transpose_matrix(matrix): #транспонирование матрицы
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
def subtract_matrices(A, B): #вычитание матрицы
    return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
K = int(input("Введите число K: "))
N = int(input("Введите размер матрицы N: "))
A = create_matrix(N)
F = form_matrix_F(A, K)
A_T = transpose_matrix(A)
result = subtract_matrices(multiply_matrices(multiply_matrix_by_scalar(A, K), F), multiply_matrix_by_scalar(A_T, K))
print("Матрица A:")
for row in A:
    print(row)
print("\nМатрица F:")
for row in F:
    print(row)
print("\nРезультат выражения K * A * F - K * A^T:")
for row in result:
    print(row)