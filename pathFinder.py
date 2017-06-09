board = [[0 for y in xrange(11)] for x in range(11)]
auxBoard = [[0 for y in xrange(11)] for x in range(11)]


def print_board():
    for y in xrange(len(board[0])):
        for x in xrange(len(board)):
            print board[x][y],
            if x >= len(board) - 1:
                print
    print


def path_finder(x, y, xf, yf):
    board[x][y] = 's'
    board[xf][yf] = 1
    path_builder(xf, yf)
    print path_tracker(x, y)


def path_builder(xf, yf):
    if yf - 1 >= 0:
        if board[xf][yf - 1] != 'W':
            if board[xf][yf - 1] > board[xf][yf] or board[xf][yf - 1] == 0:
                v = board[xf][yf] + 1
                board[xf][yf - 1] = v
                path_builder(xf, yf - 1)
    if yf + 1 <= 10:
        if board[xf][yf + 1] != 'W':
            if board[xf][yf + 1] > board[xf][yf] or board[xf][yf + 1] == 0:
                v = board[xf][yf] + 1
                board[xf][yf + 1] = v
                path_builder(xf, yf + 1)
    if xf - 1 >= 0:
        if board[xf - 1][yf] != 'W':
            if board[xf - 1][yf] > board[xf][yf] or board[xf - 1][yf] == 0:
                v = board[xf][yf] + 1
                board[xf - 1][yf] = v
                path_builder(xf - 1, yf)
    if xf + 1 <= 10:
        if board[xf + 1][yf] != 'W':
            if board[xf + 1][yf] > board[xf][yf] or board[xf + 1][yf] == 0:
                v = board[xf][yf] + 1
                board[xf + 1][yf] = v
                path_builder(xf + 1, yf)
    return


def path_tracker(x, y):
    cords = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))
    for cord in cords:
        if x + cord[0] >= 0 and y + cord[1] <= 10 and x + cord[0] <= 10 and y + cord[1] >= 0 and board[x + cord[0]][
                    y + cord[1]] != 'W' and board[x + cord[0]][y + cord[1]] != 's':
            min = (x + cord[0], y + cord[1])
    for cord in cords:
        if x + cord[0] >= 0 and y + cord[1] <= 10 and x + cord[0] <= 10 and y + cord[1] >= 0:
            if board[x + cord[0]][y + cord[1]] < board[min[0]][min[1]] and board[x + cord[0]][y + cord[1]] != 'W' and \
                            board[x + cord[0]][y + cord[1]] != 's':
                min = (x + cord[0], y + cord[1])
    return min


for y in xrange(9):
    board[4][y] = 'W'
for x in xrange(1, 10):
    board[x][4] = 'W'
print_board()
path_finder(3, 3, 5, 5)
print_board()
