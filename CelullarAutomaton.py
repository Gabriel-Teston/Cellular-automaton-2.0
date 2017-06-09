import pygame
from pygame.locals import *
from random import randint
import math

# Pygame setup
resolution = (1297, 733)
pygame.init()
windowSurface = pygame.display.set_mode(resolution, HWSURFACE | DOUBLEBUF | RESIZABLE)
pygame.display.set_caption("Runnig!")

# Collors setup
collors = [(192, 192, 192), (0, 0, 0), (0, 255, 0), (255, 255, 255)]

# Board setup
xO = (resolution[0] - 1) / 12  # --->The number of positions on the X-axis is equal to the window X-resolution minus the
# initial margin (1 pixel), divided by the cell size (7 pixels) plus the margin between the cells (1 pixel)
yO = (resolution[1] - 1) / 12
iO = 4
board = [[[0, 0, 0, 0] for y in xrange(yO)] for x in xrange(xO)]  # --->Define a 3d matrix [x][y][info]
auxBoard = [[[0, 0, 0, 0] for y in xrange(yO)] for x in xrange(xO)]

# Window drawing
windowSurface.fill(collors[3])


def print_cells(x, y):  # --->Receives the position of the cell
    collor = collors[auxBoard[x][y][1]]
    x += 6 + (x * 11)  # --->Adds the initial margin and the margin between the previous cell
    y += 6 + (y * 11)
    pygame.draw.polygon(windowSurface, collor, ((x - 5, y - 5), (x + 5, y - 5), (x + 5, y + 5),
                                                (x - 5, y + 5)))  # --->Draws a square around the received coordinate


for x in xrange(xO):
    for y in xrange(yO):
        print_cells(x, y)

# Global game variables setup
running = True
paused = False
# cords = ((-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1))
cords = ((0, -1), (-1, 0), (1, 0), (0, 1))
type = 1
collor = 1


# Game functions
def update():
    for x in xrange(xO):
        for y in xrange(yO):
            print_cells(x, y)
    for x in xrange(xO):
        for y in xrange(yO):
            for i in xrange(iO):
                aux = auxBoard[x][y][i]
                board[x][y][i] = aux


def entity_rules(x, y):
    if board[x][y][2] == 0:
        board[x][y][2] = find_food(x, y)
    if board[x][y][2] != 0:
        path_finder(x, y)

def walk(x, y, x1, y1):
    for i in xrange(iO):
        if auxBoard[x1][y1][i] != 'W' and auxBoard[x1][y1][i] != 1:
            auxBoard[x1][y1][i] = board[x][y][i]
            auxBoard[x][y][i] = 0

def path_finder(x, y):
    for x1 in xrange(xO):
        for y1 in xrange(yO):
            board[x1][y1][3] = 0
    target = board[x][y][2]
    board[target[0]][target[1]][3] = 1
    path_builder(target[0], target[1], x, y, 0)
    move = path_tracker(x, y)
    walk(x, y, move[0], move[1])


def path_builder(xt, yt, x, y, i):
    for cord in cords:
        if xt + cord[0] >= 0 and xt + cord[0] <= xO - 1 and yt + cord[1] >= 0 and yt + cord[1] <= yO - 1:
            if board[xt + cord[0]][yt + cord[1]][0] != 'W' and (
                            board[xt + cord[0]][yt + cord[1]][3] > board[xt][yt][3] or
                            board[xt + cord[0]][yt + cord[1]][
                                3] == 0):
                k = board[xt][yt][3]
                board[xt + cord[0]][yt + cord[1]][3] = k + 1
                if ((xt + cord[0] == x and yt + cord[1] == y) and i > 1) or k >= 10 or \
                                board[xt + cord[0]][yt + cord[1]][0] == 1:
                    return
                path_builder(xt + cord[0], yt + cord[1], x, y, i + 1)
            elif board[xt + cord[0]][yt + cord[1]][0] == 'W':
                board[xt + cord[0]][yt + cord[1]][3] = 'W'
        else:
            return
    return


def path_tracker(x, y):
    possiblemin = []
    min = board[x][y][3]
    for cord in cords:
        if x + cord[0] >= 0 and x + cord[0] <= xO - 1 and y + cord[1] >= 0 and y + cord[1] <= yO - 1:
            if board[x + cord[0]][y + cord[1]][3] <= min and board[x + cord[0]][y + cord[1]][0] != 'W' and \
                            board[x + cord[0]][y + cord[1]][3] != 0:
                min = board[x + cord[0]][y + cord[1]][3]
                possiblemin.append((x + cord[0], y + cord[1]))

    for y1 in xrange(yO):
        for x1 in xrange(xO):
            board[x][y][3] = 0
    if len(possiblemin) > 0:
        return possiblemin[randint(0, len(possiblemin) - 1)]
    else:
        return (x, y)


def food_rules(x, y):
    # grow(x,y)
    pass


def grow(x, y):
    cord = cords[randint(0, len(cords) - 1)]
    if x + cord[0] >= 0 and x + cord[0] <= xO - 1 and y + cord[1] >= 0 and y + cord[1] <= yO - 1:
        if auxBoard[x + cord[0]][y + cord[1]][0] != 'W' and auxBoard[x + cord[0]][y + cord[1]][0] != 1 and \
                        auxBoard[x + cord[0]][y + cord[1]][0] != 'F' and board[x + cord[0]][y + cord[1]][0] != 'F':
            for i in range(iO):
                auxBoard[x + cord[0]][y + cord[1]][i] = board[x][y][i]
                auxBoard[x][y][i] = 0


def read():
    for x in xrange(xO):
        for y in xrange(yO):
            if board[x][y][0] == 1:
                entity_rules(x, y)
            elif board[x][y][0] == 'F' and auxBoard[x][y][0] != 1:
                food_rules(x, y)
            elif board[x][y][0] == 0 and auxBoard[x][y][0] != 1 and auxBoard[x][y][0] != 'F':
                for i in xrange(iO):
                    aux = board[x][y][i]
                    auxBoard[x][y][i] = aux
    for s in xrange(1):
        xr = randint(0, xO - 1)
        yr = randint(0, yO - 1)
        if auxBoard[xr][yr][0] != 1:
            auxBoard[xr][yr][0] = 'F'
            auxBoard[xr][yr][1] = 2
    update()


def find_food(x, y):
    possibletargets = []
    m = 13
    for x1 in xrange(x - 11, x + 11):
        for y1 in xrange(y - 11, y + 11):
            if x1 >= 0 and x1 <= xO - 1 and y1 >= 0 and y1 <= yO - 1:
                if board[x1][y1][0] == 'F' and math.sqrt(pow((x1 - x), 2) + pow((y1 - y), 2)) <= m:
                    possibletargets.append((x1, y1))
    if len(possibletargets) > 0:
        return possibletargets[randint(0, len(possibletargets) - 1)]
    else:
        return 0


# Execution loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX, mouseY) = pygame.mouse.get_pos()
            auxBoard[(mouseX - 3) / 12][(mouseY - 3) / 12][0] = type
            auxBoard[(mouseX - 3) / 12][(mouseY - 3) / 12][1] = collor
            update()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = (True, False)[paused]
                if paused == True:
                    pygame.display.set_caption("Paused...")
                else:
                    pygame.display.set_caption("Running!")
            if event.key == pygame.K_c:
                for x in xrange(xO):
                    for y in xrange(yO):
                        for i in xrange(iO):
                            auxBoard[x][y][i] = 0
                            board[x][y][i] = 0
                update()
            if event.key == pygame.K_0:
                type = 0
                collor = 0
            if event.key == pygame.K_1:
                type = 1
                collor = 1
            if event.key == pygame.K_f:
                type = 'F'
                collor = 2
            if event.key == pygame.K_w:
                type = 'W'
                collor = 3
    if not paused:
        read()
    pygame.display.update()
