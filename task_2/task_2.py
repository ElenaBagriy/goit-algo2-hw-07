from functools import lru_cache
from splay_tree import SplayTree
import timeit
import matplotlib.pyplot as plt


# --------------------------------------------------
# Fibonacci with LRU Cache
# --------------------------------------------------
@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n-1) + fibonacci_lru(n-2)


# --------------------------------------------------
# Fibonacci with Splay Tree
# --------------------------------------------------
def fibonacci_splay(n, tree):
    result = tree.find(n)
    if result is not None:
        return result
    if n < 2:
        result = n
    else:
        result = fibonacci_splay(n - 1, tree) + fibonacci_splay(n - 2, tree)
    tree.insert(n, result)
    return result


# --------------------------------------------------
# Функції для вимірювання "чистого" обчислення
# --------------------------------------------------

def measure_lru(n):
    # Перед кожним вимірюванням створюємо порожній кеш
    fibonacci_lru.cache_clear()
    return fibonacci_lru(n)


def measure_splay(n):
    # Перед кожним вимірюванням створюємо порожнє дерево
    tree = SplayTree()
    return fibonacci_splay(n, tree)


# --------------------------------------------------
# Вимірювання часу
# --------------------------------------------------

# Значення n від 0 до 950 з кроком 50
numbers = range(0, 951, 50)
# Кількість повторних вимірювань
repeat = 1000
lru_times = []
splay_times = []


for n in numbers:
    # LRU Cache
    lru_time = timeit.timeit(
        lambda n=n: measure_lru(n),
        number=repeat
    ) / repeat
    lru_times.append(lru_time)

    # Splay Tree
    splay_time = timeit.timeit(
        lambda n=n: measure_splay(n),
        number=repeat
    ) / repeat
    splay_times.append(splay_time)


# --------------------------------------------------
# Таблиця результатів
# --------------------------------------------------

print(
    f"{'n':<10}"
    f"{'LRU Cache Time (s)':<25}"
    f"{'Splay Tree Time (s)':<25}"
)

print("-" * 60)

for n, lru_time, splay_time in zip(numbers, lru_times, splay_times):
    print(
        f"{n:<10}"
        f"{lru_time:<25.10f}"
        f"{splay_time:<25.10f}"
    )


# --------------------------------------------------
# Графік
# --------------------------------------------------

plt.figure(figsize=(10, 6))

plt.plot(
    list(numbers),
    lru_times,
    marker="o",
    label="LRU Cache"
)

plt.plot(
    list(numbers),
    splay_times,
    marker="x",
    label="Splay Tree"
)

plt.xlabel("Числа Фібоначчі(n)")
plt.ylabel("Середній час виконання (секунди)")
plt.title("Порівняння часу виконання для LRU Cache та Splay Tree")
plt.legend()
plt.grid(True)
plt.show()