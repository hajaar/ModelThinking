__author__ = 'kartikn'

import pygame
from pygame.locals import  *
import sys
import random

LEFT = 0
TOP = 0
WIDTH = 5
HEIGHT = 5
ROW_MAX = 100
COLUMN_MAX = 100
WINDOW_WIDTH = ROW_MAX*WIDTH
WINDOW_HEIGHT = COLUMN_MAX*HEIGHT
BLACK = (255,255,255)
WHITE = (0,0,0)


class Cell(pygame.Rect):
    def __init__(self, left, top, width, height, position, alive):
        super(Cell, self).__init__(left, top, width, height)
        self.alive = alive
        assert 0<=self.alive<=1, 'Possible values for Alive status are only 0 or 1'
        self.position = position
        self.setColor()

    def setAlive(self, alive):
        self.alive = alive
        self.setColor()

    def setColor(self):
        if self.alive == 0:
            self.color = BLACK
        else:
            self.color = WHITE

    def __str__(self):
        return str('alive: ' + str(self.alive) + ' position ' + str(self.position))


def createInitialMap(cell_map):
    for i in range(0, ROW_MAX):
        column_list = []
        for j in range(0, COLUMN_MAX):
            column_list.append(Cell(LEFT + i * WIDTH, TOP + j * HEIGHT, WIDTH, HEIGHT, (i,j), 0))
        cell_map.append(column_list)


def updateCellMap(cell_map):
    change_dict = {}
    for i in range(0,ROW_MAX):
        for j in range(0,COLUMN_MAX):
            sum = 0
            for x in range(i - 1, i + 2):
                if 0 <= x < ROW_MAX:
                    for y in range(j - 1, j + 2):
                        if 0 <= y < COLUMN_MAX:
                            if x != i or y != j:
                                sum += cell_map[x][y].alive
            if cell_map[i][j].alive == 0 and sum == 3:
                change_dict[i,j] = 1
            elif cell_map[i][j].alive == 1 and 2<=sum <= 3:
                change_dict[i, j] = 1
            else:
                change_dict[i, j] = 0
    for i in range(0,ROW_MAX):
        for j in range(0,COLUMN_MAX):
            cell_map[i][j].setAlive(change_dict[i,j])


def defineStartingFigure(cell_map):

    for i in range(0,ROW_MAX):
        for j in range(0,COLUMN_MAX):
            cell_map[i][j].setAlive(random.randrange(0,2))


pygame.init()
pygame.time.set_timer(USEREVENT+1,100)
windowSurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT),0,0)
cell_map = []
createInitialMap(cell_map)
defineStartingFigure(cell_map)
windowSurface.fill((0, 0, 255))


while True:
    for event in pygame.event.get():
         if event.type == QUIT:
                pygame.quit()
                sys.exit()
         if event.type == USEREVENT + 1:
            for one_row in cell_map:
                for one_cell in one_row:
                    pygame.draw.rect(windowSurface,one_cell.color,one_cell,0)
            pygame.display.update()
            updateCellMap(cell_map)






