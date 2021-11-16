import numpy as np

import numpy as np
import copy as cp

chosen_file = input("Which file would you like to solve?\nEasy: s01a, s01b, s01c, s02a, s02b, s02c, s06a, s06b, s06c, "
                    "s10a. s10b, s10c, s13a, s13b, s13c\nMedium: s03a, s03b, s03c, s04a, s04b, s04c, s07a, s07b, "
                    "s07c, s11a, s11b, s11c, s14a, s14b, s14c\nHard: s05a, s05b, s05c, s08a, s08b, s08c, s09a s09b, "
                    "s09c "
                    "s12a, s12b, s12c, s15a, s15b, s15c, s16\nPlease enter your choice here: ")
file = open(chosen_file + ".txt")
grid = []
for line in file:
    grid.append(line.split())
for i in range(len(grid)):
    for j, string in enumerate(grid[i]):
        grid[i][j] = int(string)
file.close()


def possible(y, x, n):
    global grid
    for i in range(0, 9):
        if grid[y][i] == n:
            return False
    for i in range(0, 9):
        if grid[i][x] == n:
            return False
    x0 = (x // 3) * 3
    y0 = (y // 3) * 3
    for i in range(0, 3):
        for j in range(0, 3):
            if grid[y0 + i][x0 + j] == n:
                return False
    return True


def solve():
    global grid
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1, 10):
                    if possible(y, x, n):
                        grid[y][x] = n
                        solve()
                        grid[y][x] = 0  # <<--- Question 1
                return
    for row in grid:
        print(" ".join(map(str, row)))


solve()
