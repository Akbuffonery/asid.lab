import re
digit_words = {0: 'ноль', 1: 'один', 2: 'два', 3: 'три', 4: 'четыре', 5: 'пять', 6: 'шесть', 7: 'семь', 8: 'восемь', 9: 'девять'}
def num2words(num): return ' '.join(digit_words[int(d)] for d in str(num))
with open('input.txt', 'r') as f:
    numbers = re.findall(r'\b\d{0,5}\b', f.read())
    minzn, maxzn = min(map(int, numbers)), max(map(int, numbers))
    for num_str in numbers:
        if num_str.startswith('77') and len(num_str) > 2:
            print(num_str[2:])
print('Среднее число =', num2words((minzn + maxzn) // 2))
