import copy
def read_matrix(filename):
    with open(filename) as f:
        return [list(map(int, line.split())) for line in f]
k = int(input("K: "))
n = int(input("n: "))
A = read_matrix('matrix.txt')
F = copy.deepcopy(A)
# Считаем условия для F
count = 0
product = 1
for i in range(n):
    for j in range(n):
        if i > j and j > (n-1-i) and (j+1) % 2 == 0 and F[i][j] > k:
            count += 1
        if i < j and j < (n-1-i) and (i+1) % 2 == 1 and F[i][j] % 2 == 0:
            product *= F[i][j]
# Меняем F по условию
if count < product:
    # Меняем нижний правый треугольник с транспонированным
    for i in range(n):
        for j in range(n):
            if i > j and j > (n-1-i):
                F[i][j], F[j][i] = F[j][i], F[i][j]
else:
    # Меняем верхний правый треугольник с повёрнутым
    for i in range(n):
        for j in range(n):
            if i < j and j > (n-1-i):
                F[i][j], F[n-1-j][n-1-i] = F[n-1-j][n-1-i], F[i][j]
# Транспонируем A
AT = [[A[j][i] for j in range(n)] for i in range(n)]
# Вычисляем k*A*F
kAF = [[0]*n for _ in range(n)]
for i in range(n):
    for j in range(n):
        for m in range(n):
            kAF[i][j] += k * A[i][m] * F[m][j]
# Вычисляем k*AT
kAT = [[k*AT[i][j] for j in range(n)] for i in range(n)]
# Итоговый результат
result = [[kAF[i][j] - kAT[i][j] for j in range(n)] for i in range(n)]
# Вывод
print("A:"); [print(row) for row in A]
print("F:"); [print(row) for row in F]
print("AT:"); [print(row) for row in AT]
print("k*A*F:"); [print(row) for row in kAF]
print("k*AT:"); [print(row) for row in kAT]
print("Result:"); [print(row) for row in result]
