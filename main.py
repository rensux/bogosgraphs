import csv
import scipy.signal as sig
import matplotlib.pyplot as plt

margin = 100  # minimum distance between graphs
N = 2  # probably don't touch
Wn = .05  # play with this <0, 1>
butter = sig.butter(N, Wn, output='sos')


def readxy(title: str):
    x = []
    y = []
    with open(title + ".csv", 'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=' ')
        for row in plots:
            x.append(float(row[0]))
            y.append(float(row[1]))
    return x, y


def denoise(y: [float]):
    return sig.sosfiltfilt(butter, y)


def aggregate(titles: [str], separate):
    top = 0
    plt.xlabel("2θ")
    plt.ylabel("Intensity")
    plt.yticks([])
    for title in titles:
        x, y = readxy(title)
        yi = denoise(y)
        if separate:  # separate the graphs above each other
            bottom = min(yi)
            yi += top - bottom + margin
            top = max(yi)
        plt.plot(x, yi)


def export(titles: [str], separate: bool, out: str = None):
    fig = plt.figure()
    if out is None:
        out = f'{"+".join(titles)}'
    out += f'_N={N}_Wn={Wn}{"_sep" if separate else ""}'
    aggregate(titles, separate)
    plt.savefig(out + '.svg', bbox_inches='tight')
    plt.close(fig)


export(["test1", "test2", "test3", "test3", "test3"], True)
export(["test1", "test2", "test3", "test3", "test3"], False)
# export(["test2", "test3"], "easdasd")


# export(["file1", "file2", "file3"])
