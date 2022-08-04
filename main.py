import csv
import math

import numpy as np
import scipy.signal as sig
import matplotlib.pyplot as plt

margin = 100  # minimum distance between graphs
N = 2  # probably don't touch
Wn = .05  # play with this <0, 1>
butter = sig.butter(N, Wn, output='sos')


def readxy(path: str, title: str, ext: str = '.xy', delim: str = ' ', cols: [int] = [0, 1]):
    x = []
    y = []
    with open(path + title + ext, 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=delim)
        for row in plots:
            x.append(float(row[cols[0]]))
            y.append(float(row[cols[1]]))
    return x, y


def readcsv(path: str, title: str):
    return readxy(path, title, '.csv', ',')


def readReflectance(path: str, title: str):
    x, y = readxy(path, title, '.csv', ',', [1, 2])
    for i in range(len(x)):
        R = y[i] / 100
        Ri = 1 - R
        R2 = R * 2
        y[i] = math.sqrt(x[i] * Ri * Ri / R2)
    return x, y


def denoise(y: [float]):
    return sig.sosfiltfilt(butter, y)


def aggregate(path: str, titles: [str], separate: bool):
    bottom = 0
    plt.xlabel("2θ")
    plt.ylabel("Intensity")
    plt.yticks([])
    for title in titles:
        x, y = readxy(path, title)
        yi = denoise(y)
        if separate:  # separate the graphs above each other
            top = max(yi)
            yi += -top + bottom - margin
            bottom = min(yi)
        plt.plot(x, yi)


def exportgroup(titles: [str], separate: bool, group: str = None, out: str = None):
    fig = plt.figure()
    if out is None:
        out = f'{"+".join(titles)}'
    out += f'_N={N}_Wn={Wn}{"_sep" if separate else ""}'
    path = f'data/{"" if group is None else group + "/"}'
    aggregate(path, titles, separate)
    plt.legend(titles, bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left", mode="expand", ncol=len(titles))
    plt.savefig(f'img/{out}.svg')
    plt.close(fig)


def exportreflect(title: str):
    exportcsv(title, readReflectance, True)


def exportcsv(title: str, read=readcsv, minorTicks=False):
    fig = plt.figure()
    out = f'{title}_N={N}_Wn={Wn}'
    x, y = read('data/', title)
    yi = denoise(y)
    line, = plt.plot(x, yi)
    line.set_color('black')
    if minorTicks:
        ticks, labels = calcTicks(min(x), max(x), 9)
        plt.xticks(ticks, labels)
    plt.savefig(f'img/{out}.svg')
    plt.close(fig)


def calcTicks(xmin, xmax, steps):
    ticks = np.arange(math.floor(xmin), xmax + (1 / steps), 1 / steps)
    labels = np.full(len(ticks), "")
    for i in range(0, len(ticks), steps):
        labels[i] = f'{int(round(ticks[i]))}'
    return ticks, labels


exportgroup(["CAT-3", "CAT-2", "CAT-1", "TiO2-P25", "ZIF-8-MK"], True, "group1")

exportreflect("cat-1-ref")
exportreflect("cat-2-ref")
exportreflect("cat-3-ref")
exportreflect("zif-8-mk-ref")

exportcsv("cat-1")
exportcsv("cat-2")
exportcsv("cat-3")
exportcsv("zif-8-mk")
