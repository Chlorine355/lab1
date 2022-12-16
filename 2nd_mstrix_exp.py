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


n = 2 ** 13  # col number
m = 1  # row number (varies)
avg_ladder_exp_list_1 = []
avg_ladder_exp_list_2 = []
gen = 1
for power in range(1, 14):
    # generate matrix
    m = m * 2
    a = [[0 for i in range(n)] for j in range(m)]
    if gen == 1:
        target = 2 * n + 1
        for i in range(m):
            for j in range(n):
                a[i][j] = (n // m * i + j) * 2
    else:
        target = 16 * n + 1
        for i in range(m):
            for j in range(n):
                a[i][j] = (n // m * i * j) * 2

    print(f"M: {m}")
    # matrix generated

    avg_ladder_exp_time = 0
    for timed in range(100):
        t1 = perf_counter_ns()
        ladder_exp()
        avg_ladder_exp_time += perf_counter_ns() - t1
    avg_ladder_exp_time /= 100
    print("Avg ladder_exp time:", avg_ladder_exp_time)
    avg_ladder_exp_list_1.append(avg_ladder_exp_time)
    print()

    # run 3 algorithms 3 times each and measure time

gen = 2
m = 1
for power in range(1, 14):
    # generate matrix
    m = m * 2
    a = [[0 for i in range(n)] for j in range(m)]
    if gen == 1:
        target = 2 * n + 1
        for i in range(m):
            for j in range(n):
                a[i][j] = (n // m * i + j) * 2
    else:
        target = 16 * n + 1
        for i in range(m):
            for j in range(n):
                a[i][j] = (n // m * i * j) * 2

    print(f"M: {m}")
    # matrix generated

    avg_ladder_exp_time = 0
    for timed in range(100):
        t1 = perf_counter_ns()
        ladder_exp()
        avg_ladder_exp_time += perf_counter_ns() - t1
    avg_ladder_exp_time /= 100
    print("Avg ladder_exp time:", avg_ladder_exp_time)
    avg_ladder_exp_list_2.append(avg_ladder_exp_time)
    print()

print("Exponential 1:", avg_ladder_exp_list_1)
print("Exponential 2:", avg_ladder_exp_list_2)

fig, ax = pyplot.subplots()
x_labels = [i for i in range(1, 14)]
exp_line_1 = ax.plot(x_labels, avg_ladder_exp_list_1, label='1st gen', color="green")
exp_line_2 = ax.plot(x_labels, avg_ladder_exp_list_2, label='2nd gen', color="red")
red_patch = mpatches.Patch(color='red', label='Gen 2')
green_patch = mpatches.Patch(color='green', label='Gen 1')
pyplot.legend(handles=[red_patch, green_patch])
pyplot.yscale('log')
ax.set_title("Exponential")
ax.set_ylabel("Время работы, нс")
ax.set_xlabel("Степень М")
ax.set_ylim(1, 10e8)
ax.set_xlim(0, 14)
pyplot.show()
