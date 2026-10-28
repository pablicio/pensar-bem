import matplotlib.pyplot as plt

fig, (esq, dir_) = plt.subplots(1, 2)
esq.bar(["2026", "2027"], [686.4, 707.2])
plt.title("eixo a partir de 680")
dir_.bar(["2026", "2027"], [686.4, 707.2])
plt.title("eixo a partir de zero")
print([ax.get_title() for ax in fig.axes])
