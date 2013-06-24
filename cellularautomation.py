__author__ = 'kartikn'

import pygame
from pygame.locals import  *
import sys
import math
import random


cell_status = {1:'000', 2:'001',4:'010',8:'011',16:'100',32:'101',64:'110',128:'111'}
cell_rule = {}
LENGTH = 100
LEFT = 20
TOP = 20
WIDTH = 2
HEIGHT = 2
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
RULE_NO = 46


def generateCellRule():
    global cell_rule
    rule_no = RULE_NO

    #while (rule_no < 1 or rule_no > 255):
    #    rule_no = input('Enter the rule')

    key_range = []
    rule_dict = {}
    cell_rule = {}
    [key_range.append(int(math.pow(2,i))) for i in range(0,8)]
    for i in range(0,8):
        rule_dict[key_range[i]] = 0
    while rule_no > 0:
        if rule_no < key_range[-1]:
            for i in range(0, len(key_range)):
                if key_range[i] > rule_no:
                    rule_dict[key_range[i - 1]] = 1
                    rule_no -= key_range[i - 1]
                    break
        else:
            rule_dict[key_range[-1]] = 1
            rule_no -= key_range[-1]
    for i in cell_status:
        cell_rule[cell_status[i]] = rule_dict[i]
    print cell_rule


class Cell(pygame.Rect):
    def __init__(self, left, top, width, height, position, length, alive):
        super(Cell, self).__init__(left, top, width, height)
        self.alive = alive
        assert 0<=self.alive<=1, 'Possible values for Alive status are only 0 or 1'
        self.length = length
        assert self.length >= 3, 'Cellular Automation requires at least 3 cells'
        self.position = position
        assert 0<=self.position <=self.length, 'Position has to be between 0 and value of length'

    def setAlive(self, alive):
        self.alive = alive

    def __str__(self):
        return str(self.alive)


def printList(name, tmp_list):
    list_value = ''
    for cell in tmp_list:
        list_value += str(cell)
    print name, list_value


def generateNewCells(tmp_list, top):
    new_cell_list = []
    [new_cell_list.append(Cell(LEFT + i * WIDTH, TOP+top*HEIGHT, WIDTH, HEIGHT, i, LENGTH, 0)) for i in range(0, LENGTH)]
    new_cell_list[0].alive = tmp_list[0].alive
    [new_cell_list[i].setAlive(cell_rule[str(tmp_list[i - 1].alive) + str(tmp_list[i].alive) + str(tmp_list[i + 1].alive)]) for i in range(1, len(new_cell_list) - 1)]
    new_cell_list[-1].alive = tmp_list[-1].alive
    return new_cell_list


def createInitialRow(cell_list):
    [cell_list.append(Cell(LEFT + i * WIDTH, TOP, WIDTH, HEIGHT, i, LENGTH, random.randrange(0, 2))) for i in
     range(0, LENGTH)]
    return cell_list

pygame.init()
windowSurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT),0,0)
generateCellRule()
cell_list = []
cell_rows = []
cell_rows.append(createInitialRow(cell_list))
pygame.time.set_timer(USEREVENT+1,100)
tick = 1
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == USEREVENT + 1:
            one_row = generateNewCells(cell_rows[tick-1],tick)
            for one_cell in one_row:
                if one_cell.alive == 0:
                    color = (0,0,255)
                else:
                    color = (255,0,0)
                pygame.draw.rect(windowSurface,color,one_cell,0)
            cell_rows.append(one_row)
            tick += 1
            pygame.display.update()






