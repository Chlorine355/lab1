from time import perf_counter_ns
from matplotlib import pyplot
import matplotlib.patches as mpatches


def binsearch(ind, low, high):
    mid = 0
    while low <= high:
        mid = (low + high) // 2
        if a[ind][mid] < target:
            low = mid + 1

        elif a[ind][mid] > target:
            high = mid - 1

        else:
            return -1

    return (low + high) // 2


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


def ladder_exp():
    global a, target, m
    x = 8191
    y = 0
    while y < m and x >= 0:
        if a[y][x] == target:
            return True

        elif a[y][x] < target:
            y += 1

        elif a[y][x] > target:
            step = 1
            start = j

            while start >= 0 and a[y][x] > target:
                start -= step
                step *= 2

            if start < 0:
                start = 0

            x = binsearch(y, start, x)
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
