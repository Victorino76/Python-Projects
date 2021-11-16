# playfair cipher
f_list = []
f = 0
k = 0
keytext = input("First, lets start with the key. Enter it here please with no spaces: ")
keytext = keytext.upper()
for i in range(65, 91):
    if chr(i) not in f_list:
        if i == 73 and chr(74) not in f_list:
            f_list.append("I")
            f = 1
        elif f == 0 and i == 73 or i == 74:
            pass
        else:
            f_list.append(chr(i))
for c in keytext:
    if c not in f_list:
        if c == 'J':
            f_list.append('I')
        else:
            f_list.append(c)
def matrixgen(x, y, start):
    return [[start for i in range(x)] for j in range(y)]
my_matrix = matrixgen(5, 5, 0)
for i in range(0, 5):
    for j in range(0, 5):
        my_matrix[i][j] = f_list[k]
        k += 1
def locindex(c):
    loc = []
    if c == 'J':
        c = 'I'
    for i, j in enumerate(my_matrix):
        for k, l in enumerate(j):
            if c == l:
                loc.append(i)
                loc.append(k)
                return loc
def playfair():
    prompt = str(input("Please enter your plaintext here with no spaces: "))
    prompt = prompt.upper()
    i = 0
    for s in range(0, len(prompt) + 1, 2):
        if s < len(prompt) - 1:
            if prompt[s] == prompt[s + 1]:
                prompt = prompt[:s + 1] + 'X' + prompt[s + 1:]
    if len(prompt) % 2 != 0:
        prompt = prompt[:] + 'X'
    print("Here is your Cipher Text: ", end=' ')
    while i < len(prompt):
        loc = locindex(prompt[i])
        loc1 = locindex(prompt[i + 1])
        if loc[1] == loc1[1]:
            print("{}{}".format(my_matrix[(loc[0] + 1) % 5][loc[1]], my_matrix[(loc1[0] + 1) % 5][loc1[1]]), end=' ')
        elif loc[0] == loc1[0]:
            print("{}{}".format(my_matrix[loc[0]][(loc[1] + 1) % 5], my_matrix[loc1[0]][(loc1[1] + 1) % 5]), end=' ')
        else:
            print("{}{}".format(my_matrix[loc[0]][loc1[1]], my_matrix[loc1[0]][loc[1]]), end=' ')
        i = i + 2


playfair()
