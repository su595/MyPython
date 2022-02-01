from matplotlib import colors
import matplotlib.pyplot as plt

def f(x):
    return x**2 -1


def g(x):
    return 100*x - x**2

    """"
    if x == 1: return 3
    if x == 2: return -3
    if x == 3: return 4
    if x == 4: return -1

    return None # Undefined
    """

def stretch(x):
    pass



def graph_function(function, min, max, step):

    x = []
    f_of_x = []
    for i in range(min, max, step):
        x.append(i)
        f_of_x.append(function(i))
    
    plt.plot(x, f_of_x)
    plt.show()


graph_function(f, 0, 50, 1)