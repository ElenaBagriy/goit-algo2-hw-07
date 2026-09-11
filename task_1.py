import random
import time
from lru_cache import LRUCache


n = 100_000      # розмір масиву
q = 50_000       # кількість запитів у тесті
hot_pool = 30    # кількість часто використовуваних діапазонів
p_hot = 0.95     # ймовірність вибору «гарячого» діапазону
p_update = 0.03  # частка запитів типу Update


def measure_time(func, *args):
    """Вимірює час виконання переданої функції."""
    start = time.perf_counter()
    result = func(*args)
    end = time.perf_counter()
    elapsed = end - start
    return result, elapsed


def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):
    """Генерує послідовність запитів Range та Update."""
    hot = [(random.randint(0, n//2), random.randint(n//2, n-1))
           for _ in range(hot_pool)]
    queries = []
    for _ in range(q):
        # Близько 3% запитів — оновлення елемента.
        if random.random() < p_update:
            idx = random.randint(0, n-1)
            val = random.randint(1, 100)
            queries.append(("Update", idx, val))
        else:                   
            # Близько 97% запитів — обчислення суми діапазону.
            if random.random() < p_hot:  
                # 95% Range-запитів використовують «гарячі» діапазони.
                left, right = random.choice(hot)
            else:                           
                # 5% Range-запитів використовують випадкові діапазони.
                left = random.randint(0, n-1)
                right = random.randint(left, n-1)
            queries.append(("Range", left, right))
    return queries


def range_sum_no_cache(array, left, right):
    """Повертає суму елементів діапазону без кешування."""
    return sum(array[left:right + 1])


def update_no_cache(array, index, value):
    """Оновлює значення елемента без кешування."""
    array[index] = value


def range_sum_with_cache(array, left, right):
    """ Повертає суму діапазону з використанням LRU-кешу.
    Якщо результат є в кеші, повертає збережене значення.
    Якщо результату немає, обчислює суму та додає її до кешу. """
    cached_sum = cache.get((left, right))
    if cached_sum == -1:
        arr_sum = sum(array[left:right + 1])
        cache.put((left, right), arr_sum)
        return arr_sum
    return cached_sum


def update_with_cache(array, index, value):
    """ Оновлює елемент масиву та інвалідує застарілі записи кешу. 
    Видаляються всі діапазони, які містять змінений індекс. 
    Інвалідація виконується лінійним проходом по ключах кешу. """
    array[index] = value
    keys_to_delete = []

    # Знаходимо всі діапазони, які містять змінений індекс.
    for key in cache.cache:
        left, right = key
        if left <= index <= right:
            keys_to_delete.append(key)

    # Видаляємо знайдені записи з кешу.
    for key in keys_to_delete:
        node = cache.cache[key]
        cache.list.remove(node)
        del cache.cache[key]


def process_queries(array, queries, mode = "with_cache"):
    """Виконує послідовність запитів у вибраному режимі."""
    if mode == "with_cache":
        range_func = range_sum_with_cache
        update_func = update_with_cache
    elif mode == "no_cache":
        range_func = range_sum_no_cache
        update_func = update_no_cache
    for query in queries:
        if query[0] == "Range":
            range_func(array, query[1], query[2])
        elif query[0] == "Update":
            update_func(array, query[1], query[2])


# Створюємо початковий масив.
array = [random.randint(1, 100) for _ in range(n)]

# Створюємо окремі копії для двох тестів,
# щоб обидва варіанти починали з однакового стану масиву.
array_no_cache = array.copy()
array_with_cache = array.copy()

# Створюємо LRU-кеш місткістю 1000 записів.
cache = LRUCache(1000)

# Генеруємо одну послідовність запитів для обох тестів.
queries = make_queries(n, q)


# ---------- БЕЗ КЕШУ ----------
_, time_no_cache = measure_time(
    process_queries,
    array_no_cache,
    queries,
    "no_cache"
)


# ---------- З КЕШЕМ ----------
_, time_with_cache = measure_time(
    process_queries,
    array_with_cache,
    queries,
    "with_cache",
)


# ---------- РЕЗУЛЬТАТ ----------
# Обчислюємо, у скільки разів кешування прискорило виконання.
speedup = time_no_cache / time_with_cache

print(f"Без кешу: {time_no_cache:.2f} c")
print(f"LRU-кеш:  {time_with_cache:.2f} c  (прискорення: ×{speedup:.2f})")