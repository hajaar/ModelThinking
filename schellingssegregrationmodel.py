__author__ = 'kartikn'


import pygame
from pygame.locals import  *
import sys
import random

LEFT = 0
TOP = 0
WIDTH = 50
HEIGHT = 50
ROW_MAX = 10
COLUMN_MAX = 10
WINDOW_WIDTH = ROW_MAX*WIDTH
WINDOW_HEIGHT = COLUMN_MAX*HEIGHT
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
MINIMUM_HAPPINESS = 0.25
OVERALL_HAPPINESS = 0.8


class Cell(pygame.Rect):
    def __init__(self, left, top, width, height, position, society_group, occupied, unique_id):
        super(Cell, self).__init__(left, top, width, height)
        self.position = position
        self.society_group = society_group
        self.occupied = occupied
        self.unique_id = unique_id
        self.setHappiness()
        self.setColor()


    def setColor(self):
        if self.occupied == 0:
            self.color = WHITE
        elif self.society_group == 0:
            self.color = RED
        else:
            self.color = BLUE

    def setHappiness(self):
        self.happiness = 0


    def __str__(self):
        return str(' id ' + str(self.unique_id) + ' society_group ' + str(self.society_group) + ' happiness ' + str(self.happiness))


def createInitialMap(cell_map):
    count = 0
    for i in range(0, ROW_MAX):
        column_list = []
        for j in range(0, COLUMN_MAX):
            occupied = random.randrange(0,2)
            society_group = random.randrange(0,2)
            new_cell = Cell(LEFT + i * WIDTH, TOP + j * HEIGHT, WIDTH, HEIGHT, (j,i), society_group, occupied, count)
            column_list.append(new_cell)
            count+=1
        cell_map.append(column_list)
    updateHappinessAll(cell_map)
    calculateOverallHappiness(cell_map)

def updateHappinessAll(cell_map):
    for i in range(0, ROW_MAX):
        for j in range(0, COLUMN_MAX):
            cell_map[i][j].happiness = calculateHappinessForOneCell(cell_map[i][j],cell_map[i][j])



def calculateHappinessForOneCell(one_cell, another_cell):
    i = another_cell.position[0]
    j = another_cell.position[1]
    sum = 0
    count = 0
    for x in range(i - 1, i + 2):
        if 0 <= x < ROW_MAX:
            for y in range(j - 1, j + 2):
                if 0 <= y < COLUMN_MAX:
                    if x != i or y != j:
                        if cell_map[x][y].occupied == 1:
                            if cell_map[x][y].society_group == one_cell.society_group:
                                sum += 1
                            count += 1
    sum = float(sum)
    count = float(count)
    if count != 0:
        happiness = sum/count
    else:
        happiness = 0
    return happiness


def calculateOverallHappiness(cell_map):
    sum = 0
    count = 0
    for i in range(0, ROW_MAX):
        for j in range(0, COLUMN_MAX):
            if cell_map[i][j].occupied == 1:
                sum += cell_map[i][j].happiness
                count += 1
    print sum/float(count)


def startMigration(cell_map):
    for i in range(0, ROW_MAX):
        for j in range(0,COLUMN_MAX):
            if cell_map[i][j].occupied == 1 and cell_map[i][j].happiness < MINIMUM_HAPPINESS:
                first_available_cell = findFirstAvailableCell(cell_map[i][j])
                migrateOneCell(cell_map[i][j], first_available_cell)



def findFirstAvailableCell(one_cell):
    i = one_cell.position[0]
    j = one_cell.position[1]
    continue_loop = True
    while continue_loop:
        for m in range(0,ROW_MAX):
            for n in range(0,COLUMN_MAX):
                another_cell = cell_map[m][n]
                if another_cell.occupied == 0:
                    potential_happiness = calculateHappinessForOneCell(one_cell,another_cell)
                    if potential_happiness > 0.25:
                        continue_loop = False
                        print potential_happiness
                        return another_cell
        if m == ROW_MAX - 1 and n == COLUMN_MAX - 1:
            return one_cell
            continue_loop = False


def migrateOneCell(one_cell, first_available_cell):
    i1 = one_cell.position[0]
    j1 = one_cell.position[1]
    i2 = first_available_cell.position[0]
    j2 = first_available_cell.position[1]
    tmp_id = first_available_cell.unique_id
    cell_map[i2][j2].society_group = one_cell.society_group
    cell_map[i2][j2].unique_id = one_cell.unique_id
    cell_map[i2][j2].occupied = 1
    cell_map[i2][j2].setColor()
    cell_map[i2][j2].happiness = calculateHappinessForOneCell(cell_map[i2][j2],cell_map[i2][j2])
    cell_map[i1][j1].unique_id = tmp_id
    cell_map[i1][j1].occupied = 0
    cell_map[i1][j1].setColor()
    cell_map[i1][j1].happiness = calculateHappinessForOneCell(cell_map[i1][j1],cell_map[i1][j1])


pygame.init()
pygame.time.set_timer(USEREVENT+1,100)
windowSurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT),0,0)
basicFont = pygame.font.SysFont(None, 15)
cell_map = []
createInitialMap(cell_map)
windowSurface.fill(WHITE)
startMigration(cell_map)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == USEREVENT + 1:
            for i in range(0, ROW_MAX):
                for j in range(0, COLUMN_MAX):
                    one_cell = cell_map[i][j]
                    if one_cell.occupied == 1 and one_cell.happiness < MINIMUM_HAPPINESS:
                        first_available_cell = findFirstAvailableCell(one_cell)
                        migrateOneCell(one_cell, first_available_cell)
                    text = basicFont.render(str(one_cell.unique_id) + str(one_cell.position), True, BLACK)
                    pygame.draw.rect(windowSurface,one_cell.color,one_cell,0)
                    windowSurface.blit(text,one_cell)
                    pygame.display.update()
#            updateCellMap(cell_map)






