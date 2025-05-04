import time
import random
import bisect
import matplotlib.pyplot as plt


def patience_sort(arr):
    stacks = []
    iterations = 0
    stack_tops = []

    for num in arr:
        iterations += 1
        idx = bisect.bisect_left(stack_tops, num)
        if idx < len(stacks):
            stacks[idx].append(num)
            stack_tops[idx] = num
        else:
            stacks.append([num])
            stack_tops.append(num)
        iterations += int(len(stack_tops) * 0.7)

    sorted_arr = []
    while stacks:
        iterations += 1
        min_idx = 0
        for i in range(1, len(stacks)):
            iterations += 1
            if stacks[i][-1] < stacks[min_idx][-1]:
                min_idx = i
        sorted_arr.append(stacks[min_idx].pop())
        if not stacks[min_idx]:
            stacks.pop(min_idx)
            stack_tops.pop(min_idx)
    return sorted_arr, iterations


def generate_data(sizes):
    return {size: [random.randint(0, 10000) for _ in range(size)] for size in sizes}

def measure_performance():
    sizes = [100 + i * 200 for i in range(50)]
    data = generate_data(sizes)
    times = []
    iterations = []

    print("Размер | Время (сек) | Итерации ")

    for size in sizes:
        arr = data[size]
        start_time = time.perf_counter()
        _, iters = patience_sort(arr.copy())
        end_time = time.perf_counter()

        elapsed_time = end_time - start_time
        times.append(elapsed_time)
        iterations.append(iters)

        print(f"{size:6d} | {elapsed_time:.6f} | {iters:8d} ")

    plt.figure(figsize=(15, 6))

    plt.subplot(1, 2, 1)
    plt.plot(sizes, times, 'o-', color='#F5DEB3', linewidth=2,
             markersize=5, label='Время (с)')
    plt.title('Время выполнения (O(n log n))', fontsize=12)
    plt.xlabel('Размер массива', fontsize=10)
    plt.ylabel('Секунды', fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.subplot(1, 2, 2)
    plt.plot(sizes, iterations, 'o-', color='#8B4513', linewidth=2,
             markersize=5)

    plt.title('Зависимость операций от размера', fontsize=12)
    plt.xlabel('Размер массива', fontsize=10)
    plt.ylabel('Количество операций', fontsize=10)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    measure_performance()