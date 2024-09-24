# iPyParallel - Intro to Parallel Programming
from ipyparallel import Client
import numpy as np
import time
import matplotlib.pyplot as plt

def initialize():
    """
    Write a function that initializes a Client object, creates a Direct
    View with all available engines, and imports scipy.sparse as spar on
    all engines.
    """
    client = Client()
    dview = client[:]
    dview.execute("import scipy.sparse as sparse")

def variables(dx):
    """
    Write a function that accepts a dictionary of variables. Create a Client
    object, a Direct View, and distribute the variables. Then, pull the
    variables in both a blocking and non-blocking format.
    :param dx: Dictionary of variables
    :return: (list of results, list of ASyncResult objects)
    """
    client = Client()
    dview = client[:]
    dview.push(dx)
    return dview

def prob3(n, print_=True):
    """
    Write a function that accepts an integer n. Instruct each engine to make n draws
    from the standard normal distribution, then hand back the minimum, maximum, and mean
    draw to the client. Print the results. If you have four engines running, your output should
    resemble the following:
    """
    client = Client()
    dview = client[:]
    dview.push({'n':n})
    dview.execute("import numpy as np")
    def func(n):
        draws = np.random.normal(size=n)
        means = np.mean(draws)
        maxs = np.max(draws)
        mins = np.min(draws)
        return [means, maxs, mins]
    results = dview.apply_sync(func, n)
    if print_:
        print("means =", [r[0] for r in results])
        print("maxs =", [r[1] for r in results])
        print("mins =", [r[2] for r in results])

def prob4():
    """
    Time the function from the previous problem in parallel and serially. Run
    apply_sync() on the function to time in parallel. To time the function
    serially, run the function in a for loop n times, where n is the number
    of engines on your machine. Print the results.
    """
    ns = np.array([1e6, 5e6, 1e7, 1.5e7], dtype=int)
    def _serial(n):
        l = []
        for _ in range(4):
            draws = np.random.normal(size=n)
            means = np.mean(draws)
            maxs = np.max(draws)
            mins = np.min(draws)
            l.append((draws, means, maxs, mins))

    serial = []
    parallel = []
    for n in ns:
        t1 = time.time()
        _serial(n)
        t2 = time.time()
        prob3(n, print_=False)
        t3 = time.time()
        serial.append(t2-t1)
        parallel.append(t3-t2)

    fig = plt.figure()
    plt.plot(ns, serial, label="Serial")
    plt.plot(ns, parallel, label="Parallel")
    plt.xlabel("n")
    plt.ylabel("time (sec)")
    plt.title("Comparison between speed of serial and parallel execution")
    plt.legend()
    plt.show()

def parallel_trapezoidal_rule(f, a, b, n=200):
    """
    Write a function that accepts a function handle, f, bounds of integration,
    a and b, and a number of points to use, n. Split the interval of
    integration evenly among all available processors and use the trapezoidal
    rule to numerically evaluate the integral over the interval [a,b].

    Parameters:
        f (function handle): the function to evaluate
        a (float): the lower bound of integration
        b (float): the upper bound of integration
        n (int): the number of points to use, defaults to 200
    Returns:
        value (float): the approximate integral calculated by the
            trapezoidal rule
    """
    client = Client()
    dview = client[:]
    points = np.linspace(a, b, n)
    
    def trapezoid(f_):
        y = f_(x)
        h = x[1] - x[0]
        m = h*sum(y[1:-1])
        sum_ = m + (h/2)*(y[0] + y[-1])
        print(sum_)
        return sum_

    dview.scatter('x', points)
    results = dview.apply_sync(trapezoid, f)
    return sum(results)










