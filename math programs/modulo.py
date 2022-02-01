import time
import matplotlib.pyplot as plt

# this is a way to realize a "stair" function, where x gets rounded to the last integer

def f(max, step):
    start =time.time()
    i = 0
    x = []
    y = []
    while i < max:
        #print(str(i) + ": " + str( i-(i%1) ))
        y.append(i - (i%1))
        x.append(i)
        i += step

    print("It took " + str(time.time() - start) + " seconds")

    plt.scatter(x,y)
    plt.grid(True)
    plt.show()

f(10, 0.001)