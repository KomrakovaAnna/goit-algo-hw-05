import timeit


# Функція для виконання пошуку підрядка за допомогою алгоритму Боєра-Мура
def boyer_moore_search(text, pattern):
    def bad_character_rule(pattern):
        bad_char = {}
        for i in range(len(pattern)):
            bad_char[pattern[i]] = i
        return bad_char

    bad_char = bad_character_rule(pattern)
    s = 0
    while s <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s
        else:
            s += max(1, j - bad_char.get(text[s + j], -1))
    return -1


# Реалізація алгоритму Кнута-Морріса-Пратта
def knuth_morris_pratt(text, pattern):
    def compute_lps_array(pattern):
        length = 0
        lps = [0] * len(pattern)
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    lps = compute_lps_array(pattern)
    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            return i - j
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1


# Реалізація алгоритму Рабіна-Карпа
def rabin_karp_search(text, pattern):
    d = 256
    q = 101
    M = len(pattern)
    N = len(text)
    i = j = 0
    p = t = 0
    h = 1
    for i in range(M - 1):
        h = (h * d) % q
    for i in range(M):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q
    for i in range(N - M + 1):
        if p == t:
            for j in range(M):
                if text[i + j] != pattern[j]:
                    break
            j += 1
            if j == M:
                return i
        if i < N - M:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + M])) % q
            if t < 0:
                t = t + q
    return -1


# Завантаження текстового файлу
with open("article1.txt", "r") as file:
    article1_text = file.read()

# Завантаження текстового файлу
with open("article2.txt", "r") as file:
    article2_text = file.read()


# Підрядок, який дійсно існує в тексті
pattern_existing_article1 = (
    "Також, у теорії алгоритмів жадібні алгоритми відіграють важливу роль."
)

pattern_existing_article2 = "Все частіше для зберігання даних рекомендаційних систем та інших додатків починають використовувати графові моделі"

# Вигаданий підрядок
pattern_random = (
    "Алгоритми пошуку відіграють вирішальну роль в повсякденному програмуванні."
)

time_existing_bms1 = timeit.timeit(
    lambda: boyer_moore_search(article1_text, pattern_existing_article1), number=1000
)
time_existing_bms2 = timeit.timeit(
    lambda: boyer_moore_search(article2_text, pattern_existing_article2), number=1000
)
time_random_bms = timeit.timeit(
    lambda: boyer_moore_search(article1_text, pattern_random), number=1000
)

# Вимірювання часу виконання для алгоритму Кнута-Морріса-Пратта
time_existing_kmp1 = timeit.timeit(
    lambda: knuth_morris_pratt(article1_text, pattern_existing_article1), number=1000
)
time_existing_kmp2 = timeit.timeit(
    lambda: knuth_morris_pratt(article2_text, pattern_existing_article2), number=1000
)
time_random_kmp = timeit.timeit(
    lambda: knuth_morris_pratt(article1_text, pattern_random), number=1000
)

# Вимірювання часу виконання для алгоритму Рабіна-Карпа
time_existing_rks1 = timeit.timeit(
    lambda: rabin_karp_search(article1_text, pattern_existing_article1), number=1000
)
time_existing_rks2 = timeit.timeit(
    lambda: rabin_karp_search(article2_text, pattern_existing_article2), number=1000
)
time_random_rks = timeit.timeit(
    lambda: rabin_karp_search(article1_text, pattern_random), number=1000
)

# Виведення результатів
print("Boyer-Moore:")
print("Existing pattern in article 1:", time_existing_bms1)
print("Existing pattern in article 2:", time_existing_bms2)
print("Random pattern:", time_random_bms)

print("Knuth-Morris-Pratt:")
print("Existing pattern in article 1:", time_existing_kmp1)
print("Existing pattern in article 2:", time_existing_kmp2)
print("Random pattern:", time_random_kmp)

print("Rabin-Karp:")
print("Existing pattern in article 1:", time_existing_rks1)
print("Existing pattern in article 2:", time_existing_rks2)
print("Random pattern:", time_random_rks)
