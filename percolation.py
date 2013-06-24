__author__ = 'kartikn'


import pygame
from pygame.locals import  *
import sys
import random
import math

LEFT = 0
TOP = 0
WIDTH = 5
HEIGHT = 5
ROW_MAX = 100
COLUMN_MAX = 100
WINDOW_WIDTH = ROW_MAX*WIDTH
WINDOW_HEIGHT = COLUMN_MAX*HEIGHT
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)
DENSITY = 0.42


class Cell(pygame.Rect):
    def __init__(self, left, top, width, height, position, occupied):
        super(Cell, self).__init__(left, top, width, height)
        self.position = position
        self.occupied = occupied
        self.burnt = 0
        self.neighbours = set([])
        self.setColor()
        self.setNeighbours()


    def setColor(self):
        if self.occupied == 0:
            self.color = WHITE
        if self.occupied == 1:
            if self.burnt == 0:
                self.color = GREEN
            else :
                self.color = RED


    def setNeighbours(self):
        i = self.position[0]
        j = self.position[1]
        for x in range(i - 1, i + 2):
            if 0 <= x < ROW_MAX:
                for y in range(j - 1, j + 2):
                    if 0 <= y < COLUMN_MAX:
                        if x != i or y != j:
                            self.neighbours.add((x,y))


    def startBurning(self, burnt):
        is_burning = False
        if self.occupied == 1:
            if burnt == 1:
                self.burnt = burnt
                self.setColor()
                is_burning = True
        return is_burning



    def __str__(self):
        return str(' id ' + str(self.unique_id) + ' position ' + str(self.position) +  ' burnt ' + str(self.burnt))


class Forest():
    def __init__(self):
        self.ListofCells = []
        self.BurningCells = set([])



    def createInitialForest(self):
        for i in range(0, ROW_MAX):
            column_list = []
            for j in range(0, COLUMN_MAX):
                rate = random.randrange(0, 100)
                occupied = 1
                if rate > DENSITY * 100:
                    occupied = 0
                new_cell = Cell(LEFT + i * WIDTH, TOP + j * HEIGHT, WIDTH, HEIGHT, (i, j), occupied, )
                column_list.append(new_cell)
            self.ListofCells.append(column_list)


    def drawForest(self):
        for one_row in self.ListofCells:
            for one_cell in one_row:
                pygame.draw.rect(windowSurface, one_cell.color, one_cell, 0)
            pygame.display.update()


    def startBurningTheForest(self):
        for one_cell in self.ListofCells[0]:
            one_cell.startBurning(random.randrange(0,2))
        self.continueBurningtheForest()

    def continueBurningtheForest(self):
        for one_row in self.ListofCells:
            for one_cell in one_row:
                if one_cell.burnt == 1:
                    for cell_pos in one_cell.neighbours:
                        self.ListofCells[cell_pos[0]][cell_pos[1]].startBurning(1)


pygame.init()
game_time = pygame.time.get_ticks()
pygame.time.set_timer(USEREVENT+1,100)
windowSurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT),0,0)
informationSurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT+100),0,0)
basicFont = pygame.font.SysFont(None, 20)
aForest = Forest()
aForest.createInitialForest()
windowSurface.fill(BLACK)
informationSurface.fill(WHITE)
aForest.drawForest()
aForest.startBurningTheForest()
aForest.drawForest()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()


