__author__ = 'kartikn'


import pygame
from pygame.locals import  *
import sys
import random
import math

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
YELLOW = (255,255,0)
MINIMUM_HAPPINESS = 0.5
OVERALL_HAPPINESS = 70
OCCUPANCY = 0.75


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
            elif self.society_group == 1:
                self.color = BLUE
            else:
                self.color = YELLOW


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


    def lookForNewLocation(self):
        max_happiness = True
        max_pos = []
        for cell_pos in unoccupied_cells:
            another_cell = cell_map[cell_pos[0]][cell_pos[1]]
            potential_happiness = another_cell.calculatePotentialHappiness(self.society_group)
            if potential_happiness >= MINIMUM_HAPPINESS:
                self.switchCells(another_cell)
                return another_cell.position
            if potential_happiness > self.happiness and max_happiness == True:
                max_pos = (cell_pos[0], cell_pos[1])
                max_happiness = False
        if max_happiness == False:
            self.switchCells(cell_map[max_pos[0]][max_pos[1]])
            return max_pos



    def switchCells(self,another_cell):
        i2 = another_cell.position[0]
        j2 = another_cell.position[1]
        tmp_id = another_cell.unique_id
        tmp_sg = another_cell.society_group
        cell_map[i2][j2].society_group = self.society_group
        cell_map[i2][j2].unique_id = self.unique_id
        cell_map[i2][j2].occupied = 1
        cell_map[i2][j2].setColor()
        cell_map[i2][j2].calculateMyHappiness()
        i1 = self.position[0]
        j1 = self.position[1]
        self.society_group = tmp_sg
        self.unique_id = tmp_id
        self.occupied = 0
        self.setColor()
        self.calculateMyHappiness()
        occupied_cells.add((i2, j2))
        occupied_cells.remove((i1, j1))
        unoccupied_cells.add((i1, j1))
        unoccupied_cells.remove((i2, j2))
        for cell_pos in self.neighbours:
            cell_map[cell_pos[0]][cell_pos[1]].calculateMyHappiness()
        for cell_pos in cell_map[i2][j2].neighbours:
            cell_map[cell_pos[0]][cell_pos[1]].calculateMyHappiness()
        return 1


    def __str__(self):
        return str(' id ' + str(self.unique_id) + ' position ' + str(self.position) + ' society_group ' + str(self.society_group) + ' happiness ' + str(self.happiness))


def createInitialMap(cell_map):
    print 'Creating the Initial Map'
    count1 = 0
    count2 = 0
    count3 = 0
    count4 = 0
    for i in range(0, ROW_MAX):
        column_list = []
        for j in range(0, COLUMN_MAX):
            rate = random.randrange(1,11)
            occupied = 1
            if rate>OCCUPANCY*10:
                occupied = 0
            society_group = random.randrange(0,3)
            if occupied == 1:
                if society_group == 0:
                    count1 += 1
                    unique_id = 'R'+str(count1)
                if society_group == 1:
                    count2 += 1
                    unique_id = 'B'+str(count2)
                if society_group == 2:
                    count4 == 'Y'+str(count4)
                occupied_cells.add((i,j))
            else:
                unoccupied_cells.add((i,j))
                count3 += 1
                unique_id = 'N' +str(count3)
            new_cell = Cell(LEFT + i * WIDTH, TOP + j * HEIGHT, WIDTH, HEIGHT, (i,j), society_group, occupied, unique_id)
            column_list.append(new_cell)
        cell_map.append(column_list)
    print 'Creation of Initial Map Done!'
    [cell_map[i][j].calculateMyHappiness() for i in range(0,ROW_MAX) for j in range(0,COLUMN_MAX )]
    print 'Calculation of Happiness for every cell done!'
    print 'Calculation of Overall Happiness Done', calculateOverallHappiness(cell_map)


def calculateOverallHappiness(cell_map):
    count = 0
    count2 = 0
    for cell_pos in occupied_cells:
        count += 1
        if cell_map[cell_pos[0]][cell_pos[1]].happiness >= MINIMUM_HAPPINESS:
            count2 += 1
    return count2*100/float(count)


def startMigration(cell_map):
    pass

def countByType():
    sum_unoccupied = 0
    sum_red = 0
    sum_blue = 0
    for one_row in cell_map:
        for one_cell in one_row:
            if one_cell.occupied == 0:
                sum_unoccupied += 1
            if one_cell.occupied == 1:
                if one_cell.color == RED:
                    sum_red += 1
                if one_cell.color == BLUE:
                    sum_blue += 1
    print sum_unoccupied, sum_red, sum_blue

pygame.init()
pygame.time.set_timer(USEREVENT+1,100)
windowSurface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT),0,0)
basicFont = pygame.font.SysFont(None, 20)
cell_map = []
unoccupied_cells = set([])
occupied_cells = set([])
createInitialMap(cell_map)
windowSurface.fill(BLACK)
happiness_percentile = calculateOverallHappiness(cell_map)
happiness_percentile_new = happiness_percentile + 1
iteration = 0
for one_row in cell_map:
    for one_cell in one_row:
        pygame.draw.rect(windowSurface, one_cell.color, one_cell, 0)
#        text = basicFont.render(str(one_cell.unique_id), True, BLACK)
#        windowSurface.blit(text, one_cell)
pygame.display.update()
countByType()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if math.fabs(happiness_percentile_new - happiness_percentile) > 0.01:
            happiness_percentile = calculateOverallHappiness(cell_map)
            for cell_pos in occupied_cells:
                one_cell = cell_map[cell_pos[0]][cell_pos[1]]
    #            print 'Looking at cell ', str(one_cell)
                if one_cell.happiness < MINIMUM_HAPPINESS:
                    another_cell_pos = one_cell.lookForNewLocation()
                    pygame.draw.rect(windowSurface, GREEN, one_cell, 0)
    #                text = basicFont.render(str(one_cell.unique_id), True, BLACK)
    #                windowSurface.blit(text, one_cell)
                    if another_cell_pos != None:
                        another_cell = cell_map[another_cell_pos[0]][another_cell_pos[1]]
                        pygame.draw.rect(windowSurface, GREEN, another_cell, 0)
    #                    text = basicFont.render(str(another_cell.unique_id), True, BLACK)
    #                    windowSurface.blit(text, another_cell)
                        pygame.display.update()
                        pygame.time.delay(100)
                        pygame.draw.rect(windowSurface, another_cell.color, another_cell, 0)
                    pygame.draw.rect(windowSurface, one_cell.color, one_cell, 0)
                    pygame.display.update()
    #        countByType()
            happiness_percentile_new = calculateOverallHappiness(cell_map)
            print ' iteration ', iteration, '% happy ', calculateOverallHappiness(cell_map)
            iteration += 1


