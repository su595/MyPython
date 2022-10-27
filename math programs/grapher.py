import time
import matplotlib.pyplot as plt

# This program can be used to graph any function

def graph(f, min, max, resolution):
    start =time.time()
    i = min
    x = []
    y = []
    while i < max:
        y.append(f(i))
        x.append(i)
        i += resolution

    print("It took {0} seconds".format(time.time() - start))

    plt.scatter(x,y)
    plt.grid(True)
    plt.show()

def g(x):
    return x - (x%1)

graph(g, -20, 20, 0.1)

