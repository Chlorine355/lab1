from matplotlib import pyplot

exp_1 = [4235.0, 10830.0, 22276.0, 42852.0, 79708.0, 150007.0, 266856.0, 467241.0, 1000458.0, 1589468.0, 3003451.0, 5392360.0, 11303975.0]
exp_2 = [4264.0, 7109.0, 12173.0, 20570.0, 33217.0, 52519.0, 82337.0, 129708.0, 220892.0, 377529.0, 717438.0, 1569408.0, 4233685.0]

new = [exp_1[i]/exp_2[i] for i in range(13)]
fig, ax = pyplot.subplots()
line_up, = ax.plot([i for i in range(1, 14)], new)
ax.set_ylabel("Отношение времен")
ax.set_xlabel("Степень М")
# pyplot.yscale('log')
ax.set_title("Отношение времени эксп. поиска на \nлинейных данных к времени на эксп. данных")
pyplot.show()