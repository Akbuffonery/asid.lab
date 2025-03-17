digit_words = {0: 'ноль', 1: 'один', 2: 'два', 3: 'три', 4: 'четыре', 5: 'пять', 6: 'шесть', 7: 'семь', 8: 'восемь', 9: 'девять'}
def num2words(num):
    return ' '.join(digit_words[int(digit)] for digit in str(num))
minzn, maxzn = float('inf'), float('-inf')
with open('input.txt', 'r') as f:
    for line in f:
        for word in line.split():
            if word.isdigit():
                num = int(word)
                if num < minzn:
                    minzn = num
                if num > maxzn:
                    maxzn = num
                if 10_000_000 > num > 10 and str(num).startswith('77'):
                    print(str(num)[2:])
print('Среднее число =', num2words((minzn + maxzn) // 2))