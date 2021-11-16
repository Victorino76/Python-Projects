from multiprocessing import Pool, Array
import random
import math
from timeit import timeit




def piMonteCarlo(n):
    """Computes and returns an estimation of pi
    using Monte Carlo simulation.

    Keyword arguments:
    n - The number of samples.
    """

    bl = []
    for i in range(n):
        r = random.random()
        bl.append(math.sqrt((1 - (r ** 2))))
    sbl = sum(bl)
    b = (4 / n) * sbl
    return b


def piParallelMonteCarlo(n, p=4):
    """Computes and returns an estimation of pi
    using a parallel Monte Carlo simulation.

    Keyword arguments:
    n - The total number of samples.
    p - The number of processes to use.
    """
    with Pool(p) as pool:
        j = [pool.apply_async(piMonteCarlo, (n // p,)) for _ in range(p)]
        total = 0
        for i in j:
            total += i.get()

    return total / p

def generateTable():
    """This function generates and prints a table
    of results to demonstrate that both versions
    compute increasingly accurate estimations of pi
    as n is increased.  It uses the following
    values of n = {12, 24, 48, ..., 12582912}. That is,
    the first value of n is 12, and then each subsequent
    n is 2 times the previous.  The reason for starting at 12
    is so that n is always divisible by 1, 2, 3, and 4.
    The first
    column represents n, the second column represents 
    the result of calling piMonteCarlo(n), and the remaining 
    4 columns represent the parallel
    version with 1, 2, 3, and 4 processes in the Pool."""
    n = 12
    print('pi values:')
    print('{0:10}\t{1:8}\t{2:8}\t{3:8}\t{4:8}\t{5:8}'.format('n', 'sequential', 'p1', 'p2',
                                                             'p3', 'p4'))
    while n <= 12582912:
        print(
            '{0:10}\t{1:.8f}\t{2:.8f}\t{3:.8f}\t{4:.8f}\t{5:.8f}'.format(n, piMonteCarlo(n), piParallelMonteCarlo(n, 1),
                                                                         piParallelMonteCarlo(n, 2),
                                                                         piParallelMonteCarlo(n, 3),
                                                                         piParallelMonteCarlo(n, 4)))
        n *= 2


def time():
    """This function generates a table of runtimes
    using timeit.  It uses the same columns and values of
    n as in the generateTable() function."""
    n = 12

    print('runtimes')
    print('{0:10}\t{1:8}\t{2:8}\t{3:8}\t{4:8}\t{5:8}'.format('n', 'sequential', 'p1', 'p2',
                                                             'p3', 'p4'))
    while n <= 12582912:
        print('{0:10}\t{1:.8f}\t{2:.8f}\t{3:.8f}\t{4:.8f}\t{5:.8f}'.format(n, timeit(lambda: piMonteCarlo(n), number=1),
                                                                           timeit(lambda: piParallelMonteCarlo(n, 1),
                                                                                  number=1),
                                                                           timeit(lambda: piParallelMonteCarlo(n, 2),
                                                                                  number=1),
                                                                           timeit(lambda: piParallelMonteCarlo(n, 3),
                                                                                  number=1),
                                                                           timeit(lambda: piParallelMonteCarlo(n, 4),
                                                                                  number=1)))
        n *= 2


if __name__ == '__main__':

    generateTable()
    time()


