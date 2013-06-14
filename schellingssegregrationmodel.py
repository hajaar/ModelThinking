__author__ = 'kartikn'


import pygame
from pygame.locals import  *
import sys
import random

LEFT = 0
TOP = 0
WIDTH = 10
HEIGHT = 10
ROW_MAX = 50
COLUMN_MAX = 50
WINDOW_WIDTH = ROW_MAX*WIDTH
WINDOW_HEIGHT = COLUMN_MAX*HEIGHT
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
MINIMUM_HAPPINESS = 0.5
OVERALL_HAPPINESS = 0.8
OCCUPANCY = 0.7


class Cell(pygame.Rect):
    def __init__(self, left, top, width, height, position, society_group, occupied, unique_id):
        super(Cell, self).__init__(left, top, width, height)
        self.position = position
        self.society_group = society_group
        self.occupied = occupied
        self.unique_id = unique_id
        self.happiness = 0
        self.neighbours = set([])
        self.setColor()
        self.setNeighbours()


    def setColor(self):
        if self.occupied == 0:
            self.color = WHITE
        if self.occupied == 1:
            if self.society_group == 0:
                self.color = RED
            else:
                self.color = BLUE


    def setNeighbours(self):
        i = self.position[0]
        j = self.position[1]
        for x in range(i - 1, i + 2):
            if 0 <= x < ROW_MAX:
                for y in range(j - 1, j + 2):
                    if 0 <= y < COLUMN_MAX:
                        if x != i or y != j:
                            self.neighbours.add((x,y))


    def calculateMyHappiness(self):
        self.happiness = 0
        if self.occupied == 1:
            self.happiness = self.calculatePotentialHappiness(self.society_group)



    def calculatePotentialHappiness(self,society_group):
        sum = 0
        for cell_pos in self.neighbours:
            if cell_map[cell_pos[0]][cell_pos[1]].occupied == 1 and cell_map[cell_pos[0]][
                cell_pos[1]].society_group == society_group:
                sum += 1
        happiness = sum / float(len(self.neighbours))
        return happiness


    def __str__(self):
        return str(' id ' + str(self.unique_id) + ' society_group ' + str(self.society_group) + ' happiness ' + str(self.happiness))


def createInitialMap(cell_map):
    count1 = 0
    count2 = 0
    count3 = 0
    for i in range(0, ROW_MAX):
        column_list = []
        for j in range(0, COLUMN_MAX):
            rate = random.randrange(1,11)
            occupied = 1
            if rate>OCCUPANCY*10:
                occupied = 1
            society_group = random.randrange(0,2)
            if occupied == 1:
                if society_group == 0:
                    count1 += 1
                    unique_id = 'R'+str(count1)
                if society_group == 1:
                    count2 += 1
                    unique_id = 'B'+str(count2)
            else:
                count3 += 1
                unique_id = 'NO' +str(count3)
            new_cell = Cell(LEFT + i * WIDTH, TOP + j * HEIGHT, WIDTH, HEIGHT, (i,j), society_group, occupied, unique_id)
            column_list.append(new_cell)
        cell_map.append(column_list)
    [cell_map[i][j].calculateMyHappiness() for i in range(0,ROW_MAX) for j in range(0,COLUMN_MAX )]
    calculateOverallHappiness(cell_map)


def calculateOverallHappiness(cell_map):
    sum = 0
    count = 0
    for i in range(0, ROW_MAX):
        for j in range(0, COLUMN_MAX):
            sum += cell_map[i][j].happiness
            count += 1
    return sum/float(count)


def startMigration(cell_map):
    for i in range(0, ROW_MAX):
        for j in range(0,COLUMN_MAX):
            if cell_map[i][j].occupied == 1 and cell_map[i][j].happiness < MINIMUM_HAPPINESS:
                first_available_cell = findFirstAvailableCell(cell_map[i][j])
                migrateOneCell(cell_map[i][j], first_available_cell)


def findFirstAvailableCell(one_cell):
    i = one_cell.position[0]
    j = one_cell.position[1]
    for m in range(0,ROW_MAX):
        for n in range(0,COLUMN_MAX):
            another_cell = cell_map[m][n]
            if another_cell.occupied == 0:
                potential_happiness = another_cell.calculatePotentialHappiness(one_cell.society_group)
                if potential_happiness >= MINIMUM_HAPPINESS:
                    return another_cell
    for m in range(0, ROW_MAX):
        for n in range(0, COLUMN_MAX):
            another_cell = cell_map[m][n]
            if another_cell.occupied == 0:
                potential_happiness = another_cell.calculatePotentialHappiness(one_cell.society_group)
                if potential_happiness > one_cell.happiness:
                    return another_cell
    return one_cell


def migrateOneCell(one_cell, first_available_cell):
    i1 = one_cell.position[0]
    j1 = one_cell.position[1]
    i2 = first_available_cell.position[0]
    j2 = first_available_cell.position[1]
    tmp_id = first_available_cell.unique_id
    tmp_sg = first_available_cell.society_group
    cell_map[i2][j2].society_group = one_cell.society_group
    cell_map[i2][j2].unique_id = one_cell.unique_id
    cell_map[i2][j2].occupied = 1
    cell_map[i2][j2].setColor()
    cell_map[i2][j2].calculateMyHappiness()
    cell_map[i1][j1].society_group = tmp_sg
    cell_map[i1][j1].unique_id = tmp_id
    cell_map[i1][j1].occupied = 0
    cell_map[i1][j1].setColor()
    cell_map[i1][j1].calculateMyHappiness()


pygame.init()
pygame.time.set_timer(USEREVENT+1,100)
windowSurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT),0,0)
basicFont = pygame.font.SysFont(None, 20)
cell_map = []
createInitialMap(cell_map)
print calculateOverallHappiness(cell_map)
windowSurface.fill(GREEN)
iteration = 0
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        is_everyone_happy = True
        for one_row in cell_map:
            for one_cell in one_row:
                pygame.draw.rect(windowSurface,one_cell.color,one_cell,0)
                if one_cell.happiness < MINIMUM_HAPPINESS:
                    is_everyone_happy = False
                #text = basicFont.render(str(one_cell.unique_id), True, BLACK)
                #windowSurface.blit(text,one_cell)
        pygame.display.update()
        if is_everyone_happy == False:
            startMigration(cell_map)
        else:
            print 'All happy'
        print iteration
        iteration += 1

