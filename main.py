import csv
import scipy.signal as sig
import matplotlib.pyplot as plt

N = 2
Wn = .05 #play with this <0, 1>
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


def aggregate(titles: [str], offset=True):
    plt.xlabel("2θ")
    plt.ylabel("Intensity")
    plt.yticks([])
    for title in titles:
        x, y = readxy(title)
        plt.plot(x, denoise(y))

def export(titles: [str], o: str = None):
    fig = plt.figure()
    if o is None:
        o = f'{"+".join(titles)}'
    o += f'_N={N}_Wn={Wn}'
    aggregate(titles)
    plt.savefig(o + '.svg', bbox_inches='tight')
    plt.close(fig)


# export(["test1", "test2", "test3"])
# export(["test2", "test3"], "easdasd")


export(["file1", "file2", "file3"])