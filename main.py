import csv
import scipy.signal as sig
import matplotlib.pyplot as plt

margin = 100  # minimum distance between graphs
N = 2  # probably don't touch
Wn = .05  # play with this <0, 1>
butter = sig.butter(N, Wn, output='sos')


def readxy(path: str, title: str):
    x = []
    y = []
    with open(path + title + ".xy", 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=' ')
        for row in plots:
            x.append(float(row[0]))
            y.append(float(row[1]))
    return x, y


def denoise(y: [float]):
    return sig.sosfiltfilt(butter, y)


def aggregate(path: str, titles: [str], separate: bool):
    top = 0
    plt.xlabel("2θ")
    plt.ylabel("Intensity")
    plt.yticks([])
    for title in titles:
        x, y = readxy(path, title)
        yi = denoise(y)
        if separate:  # separate the graphs above each other
            bottom = min(yi)
            yi += top - bottom + margin
            top = max(yi)
        plt.plot(x, yi)


def export(titles: [str], separate: bool, group: str = None, out: str = None):
    fig = plt.figure()
    if out is None and group is None:
        out = f'{"+".join(titles)}'
    if out is None:
        out = group
    out += f'_N={N}_Wn={Wn}{"_sep" if separate else ""}'
    path = f'data/{"" if group is None else group+"/"}'
    aggregate(path, titles, separate)
    plt.legend(titles)
    plt.savefig(out + '.svg', bbox_inches='tight')
    plt.close(fig)


export(["ZIF-8-MK", "TiO2-P25", "CAT-1", "CAT-2", "CAT-3"], True, "group1")