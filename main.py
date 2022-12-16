from time import perf_counter_ns
from matplotlib import pyplot
import matplotlib.patches as mpatches


def binary_row(row, low, high):
    global a, target
    if high >= low:
        mid = low + (high - low)//2
        if a[row][mid] == target:
            return 1
        elif a[row][mid] > target:
            return binary_row(row, low, mid-1)
        else:
            return binary_row(row, mid + 1, high)
    else:
        elem = max(high, 0)
        return elem


def exp_row(row, start):
    global a, target
    if a[row][start] == target:
        return 1
    i = 1
    n = start - i
    while n > 0 and a[row][n] >= target:
        i = i * 2
        n = start-i
    return binary_row(row, max(n, 0), start - i // 2)


def ladder_exp():
    global n, m, a, target
    x = n-1
    y = 0
    while 0 <= x < n and 0 <= y < m:
        if a[y][x] > target and x >= 1:
            x = exp_row(y, x)
        elif a[y][x] < target and y <= m - 2:
            y += 1
        elif a[y][x] == target:
            return 1

        else:
            return 0
    return 0


def ladder():
    global a, target  # знаю что так не надо делать, но поскольку мы переменные не меняем - да будет так,
                      # чтобы память не выделять дополнительно
    x = 8191
    y = 0
    while a[y][x] != target:
        try:
            while a[y][x] > target:
                x -= 1
            while a[y][x] < target:
                y += 1
        except IndexError:
            return False
    return True


def binary():
    global a, target, m
    for i in range(m):  # по строкам
        low = 0
        high = 8191
        while low <= high:
            mid = (high + low) // 2
            if a[i][mid] < target:
                low = mid + 1
            elif a[i][mid] > target:
                high = mid - 1
            else:
                return True
        continue
    return False


print("Введите 1 для линейных данных, 2 для экспоненциальных")
gen = int(input("Генерация матрицы: "))
n = 2 ** 13  # col number
m = 1  # row number (varies)
avg_ladder_list = []
avg_binary_list = []
avg_ladder_exp_list = []
if gen == 1:
    print("Matrix 1st generation")
else:
    print("Natrix 2nd generation")
for power in range(1, 14):
    # generate matrix
    m = m * 2
    a = [[0 for i in range(n)] for j in range(m)]
    if gen == 1:
        target = 2 * n + 1
        for i in range(m):
            for j in range(n):
                a[i][j] = (n / m * i + j) * 2
    else:
        target = 16 * n + 1
        for i in range(m):
            for j in range(n):
                a[i][j] = (n / m * i * j) * 2

    print(f"M: {m}")
    # matrix generated
    # print(a)

    avg_ladder_time = 0
    for timed in range(100):
        t1 = perf_counter_ns()
        ladder()
        avg_ladder_time += perf_counter_ns() - t1
    avg_ladder_time /= 100
    print("Avg ladder time:", avg_ladder_time)
    avg_ladder_list.append(avg_ladder_time)

    avg_binary_time = 0
    for timed in range(100):
        t1 = perf_counter_ns()
        binary()
        avg_binary_time += perf_counter_ns() - t1
    avg_binary_time /= 100
    print("Avg binary time:", avg_binary_time)
    avg_binary_list.append(avg_binary_time)

    avg_ladder_exp_time = 0
    for timed in range(100):
        t1 = perf_counter_ns()
        ladder_exp()
        avg_ladder_exp_time += perf_counter_ns() - t1
    avg_ladder_exp_time /= 100
    print("Avg ladder_exp time:", avg_ladder_exp_time)
    avg_ladder_exp_list.append(avg_ladder_exp_time)

    print()

    # run 3 algorithms 3 times each and measure time

print("Ladder:", avg_ladder_list)
print("Binary:", avg_binary_list)
print("Exponential:", avg_ladder_exp_list)

fig, ax = pyplot.subplots()
x_labels = [i for i in range(1, 14)]
ladder_line = ax.plot(x_labels, avg_ladder_list, label='Ladder', color="red")
binary_line = ax.plot(x_labels, avg_binary_list, label='Binary', color="blue")
exp_line = ax.plot(x_labels, avg_ladder_exp_list, label='Exponential', color="green")
red_patch = mpatches.Patch(color='red', label='Ladder')
blue_patch = mpatches.Patch(color='blue', label='Binary')
green_patch = mpatches.Patch(color='green', label='Exponential')
pyplot.legend(handles=[red_patch, blue_patch, green_patch])
pyplot.yscale('log')
if gen == 1:
    ax.set_title("1-ая генерация матрицы")
else:
    ax.set_title("2-ая генерация матрицы")
ax.set_ylabel("Время работы, нс")
ax.set_xlabel("Степень М")
ax.set_ylim(1, 10e8)
ax.set_xlim(0, 14)
pyplot.show()
