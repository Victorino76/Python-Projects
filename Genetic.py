import math
import random
import sys


# student name: Christopher Ransom
# This python file is run using one of these two formats:
# a) python tsp.py dj38.tsp
# b) python tsp.py dj39.tsp 1000 100 .5 .1
# In version b the parameters following the tsp file are as follows:
# 1. number of generations
# 2. population size
# 3. crossover rate
# 4. mutation rate

# 0) Getting the tsp data into a list called cities
def get_tsp():  # getting the list of coordinates corresponding to cities
    infile = open('dj38.tsp', 'r')
    full = infile.readlines()
    cities = []
    for line in full:
        try:
            float(line.strip().split()[0])
        except ValueError:  # ignoring all lines of tsp file that cannot be converted to int
            pass
        except IndexError:
            break
        else:
            x, y = line.strip().split()[1:]  # storing int values as a x and y
            cities.append((float(x), float(y)))  # appending those x and y values in a tuple (x, y)
    infile.close()
    return cities


# 1) Generating N random tours of the list of cities
def population(L, n):  # generate population aka n permutations of original list of cities
    if len(L) <= 1:
        return L
    pop = []
    for _ in range(n):
        tmp = L.copy()
        random.shuffle(tmp)
        pop.append(tmp)
    return pop


# 2) Defining a way to compute the total cost of each tour using Euclidean distance
def cost(L=[]):  # returns total of edges weights for a tour
    if L is float:
        raise TypeError(" this shit is not a list %s", L)
    c = 0  # cost value initialized to 0
    for i in range(len(L) - 1):  # includes distance between every vertex and its successor except the last
        c += math.sqrt(
            (((L[i + 1][0]) - (L[i][0])) ** 2) + ((L[i + 1][1]) - (L[i][1])) ** 2)  # Euclidean distance
    c += math.sqrt(
        (((L[-1][0]) - (L[0][0])) ** 2) + ((L[-1][1]) - (L[0][1])) ** 2)
    return int(c)  # returns total cost of tour


# 3) Selecting members of the population using stochastic universal sampling
def selection(L=[]):  # L is a list of lists, namely tours that are unique
    c = []  # cost of each tour in a list, preserving original order
    for path in L:
        c.append(cost(path))
    f = []  # fitness values for each tour
    for weight in c:
        f.append(weight / sum(c))  # fitness calculated using (cost of one tour) / (total cost of all tours)
    s = []  # list of selected tours, not costs or fitness
    g = random.uniform(0.0, (1.0 / len(L)))
    for t in f:
        if t > g:
            s.append(L[f.index(t)])
            g += 1.0 / len(L)
            break
    while len(s) != len(L):
        s.append(random.choices(L, weights=[j + g for j in f], k=1)[0])
        g += 1.0 / len(L)
    return s


# 4) Performing crossover on the selected parents using order crossover
def order_crossover(L=[], L2=[]):
    if set(L) != set(L2) or len(L) != len(L2):  # check to see if tours are permutations of one another
        raise ValueError("These two tours are not permutations of one another")
    if L == L2:
        return L, L2
    p1 = random.randint(1, len(L) - 2)  # one of the cross section endpoints, can be right or left
    p2 = random.randint(1, len(L) - 2)  # one of the cross section endpoints, can be right or left
    cross1 = []  # top portion of crossover section (L)
    cross2 = []  # bottom portion of crossover section (L2)
    c1 = []  # child 1
    c2 = []  # child 2
    q1 = []  # queue 1 (L)
    q2 = []  # queue 2 (L2)
    while p1 == p2:  # making sure the endpoints cover at least one column of integers by ensuring p1 != p2
        p2 = random.randint(1, len(L) - 2)
    for i in L[min(p1, p2):max(p1, p2)]:  # building upper cross section
        cross1.append(i)
    for j in L2[min(p1, p2):max(p1, p2)]:  # building lower cross section
        cross2.append(j)
    for i in L:
        if i not in cross2:
            q1.append(i)  # building q1 for L
    for j in L2:
        if j not in cross1:
            q2.append(j)  # building q2 for L2
    for i in list(q1[-len(L[:(min(p1, p2))]):] + cross2 + q1[:-len(L[:(min(p1, p2))])]):  # forming c1
        c1.append(i)
    for j in list(q2[-len(L[:(min(p2, p1))]):] + cross1 + q2[:-len(L[:(min(p2, p1))])]):  # forming c2
        c2.append(j)
    return c1, c2


# 5) Performing mutation on the tours remaining from crossover using block swap mutation
def block_swap(L=[]):
    p1 = random.randint(0, len(L) - 2)  # left or right endpoint of block 1
    p2 = random.randint(0, len(L) - 2)  # left or right endpoint of block 1
    while p1 == p2:
        p2 = random.randint(0, len(L) - 2)  # making sure block is of at least length 1
    p3 = random.randint(L.index(L[max(p1, p2) + 1]), len(L))  # left or right endpoint of block 2, starts after block 1
    p4 = random.randint(L.index(L[max(p1, p2) + 1]), len(L))  # left or right endpoint of block 2, starts after block 1
    while p3 == p4 or min(p3, p4) == max(p1, p2):
        p4 = random.randint(L.index(L[min(p1, p2):(max(p1, p2) + 1)][-1]), len(L))  # block 2 at least length 1
    R = list(L[:L.index(L[min(p1, p2):(max(p1, p2) + 1)][0])] + L[min(p3, p4):(max(p3, p4) + 1)] +
             L[L.index(L[min(p1, p2):(max(p1, p2) + 1)][-1]) + 1:L.index(L[min(p3, p4):(max(p3, p4) + 1)][0])] +
             L[min(p1, p2):(max(p1, p2) + 1)] +
             L[L.index(L[min(p3, p4):(max(p3, p4) + 1)][-1]) + 1:])
    # This last part appends everything from the beginning of L to the beginning of block 1's original position,
    # then appends block 2 in its entirety onto that position, then appends L's values from the end of block 1's
    # original position to the beginning of block 2's original position, then appends block 1 there.
    # After that it appends everything in L that came after the last element in block 2's original position.
    return R


# 6) Putting it all together with the basic GA
def genetic(gen_limit=100, pop_size=100, c_rate=.5, m_rate=.1):
    gens = 0
    best = None
    t = selection(population(get_tsp(), pop_size))  # list of tours with length pop_size
    while gens < gen_limit:
        c = []  # list of tour costs, indices match those of t
        for i in range(0, len(t), 2):
            r = random.random()  # trying to save resources by using the same random number for crossover and mutation
            if r < c_rate:
                t[i], t[i + 1] = order_crossover(t[i], t[i + 1])  # performing order_crossover
            if r < m_rate:
                t[i], t[i + 1] = block_swap(t[i]), block_swap(t[i + 1])  # performing block-swap mutation
        for z in t:
            c.append(cost(z))  # gathering costs of all tours
        if best is None or cost(best) > min(c):
            best = t[c.index(min(c))]  # c's indices still match those of t
        m_rate *= .9  # decrementing mutation rate as gens increase
        gens += 1  # increasing gen count
        t = selection(t)  # selecting members from t with weighted choice based on fitness
    return best, int(cost(best))


if __name__ == '__main__':
    tour = []
    if len(sys.argv) == 6:
        d = genetic(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]))
    else:
        d = genetic()
    print(d[1])
    for i in d[0]:
        tour.append(get_tsp().index(i) + 1)
    for i in tour:
        print(i, end=' ')
