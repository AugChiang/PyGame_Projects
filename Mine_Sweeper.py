import pygame
import random
import time
import math

fps = 60
black = (0, 0, 0) # landmine
white = (255, 255, 255) # default color
red = (255, 0, 0) # Flag
grey = (100, 100, 100) # grid line
blue = (0, 0, 200) # number of periphery landmines
d_grey = (210, 210, 210) # visited cube color

win_width = 800 # x
#win_length = 800 # y
window = pygame.display.set_mode((win_width, win_width))
pygame.display.set_caption("Landmine mini game")

class Cube:
    def __init__(self, row, col, width, total_rows):
        # cubes in grid list indices
        self.row = row
        self.col = col

        # cube width
        self.width = width

        # cube |vectors|
        self.cube_x = row * width
        self.cube_y = col * width

        self.total_rows = total_rows

        self.num = 0 # landmines in the periphery
        self.neighbors=[] # cube neighbors max = 8

        self.color = white
        self.font_size = self.width
    ''' not visited = while, num = 0, not closed
        visited = grey, num = self.num, closed
        landmine = black, num = -1, not closed
        hint cube = white, num = how many landmines near themselves, not closed if not visited
    '''

    def is_landmine(self):
        return self.num == -1

    def is_flag(self):
        return self.color == red

    def is_closed(self):
        return self.color == d_grey

    def make_landmine(self):
        self.num = -1
        #self.color = black

    def make_flag(self):
        self.color = red

    def make_closed(self):
        self.color = d_grey

    def reset(self):
        self.color = white

    def draw_cube(self, window):
        pygame.draw.rect(window, self.color, (self.cube_x, self.cube_y, self.width, self.width))
        pygame.font.init()
        if self.num > 0 and self.is_closed():
            font = pygame.font.SysFont("Arial", self.font_size, bold=True)
            num = font.render(str(self.num), True, blue)
            window.blit(num, (self.cube_x + 0.3 * self.width, self.cube_y))

    # add neighbors nodes into self.neighbors list
    ''' Seems that it can't get the down-left cube
        7/25 fixed, but found another problem of cross-edge neighbors.
        7/25 fixed, it was the condition problem.
    '''
    def get_neighbors(self, grid):
        self.neighbors = []
        # Check the down cube
        if self.row < self.total_rows - 1 and\
                not grid[self.row + 1][self.col].is_landmine():
            self.neighbors.append(grid[self.row + 1][self.col])

        # Check the up cube
        if self.row > 0 and\
                not grid[self.row - 1][self.col].is_landmine():
            self.neighbors.append(grid[self.row - 1][self.col])

        # Check the right cube
        if self.col < self.total_rows - 1 and\
                not grid[self.row][self.col + 1].is_landmine():
            self.neighbors.append(grid[self.row][self.col + 1])

        # Check the left cube
        if self.col > 0 and\
            not grid[self.row][self.col - 1].is_landmine():
                self.neighbors.append(grid[self.row][self.col - 1])

        # Check the up-right cube
        if self.row > 0 and\
            self.col < self.total_rows - 1 and\
            not grid[self.row - 1][self.col +1].is_landmine():
                self.neighbors.append(grid[self.row - 1][self.col + 1])

        # Check the up-left cube
        if self.row > 0 and\
            self.col > 0 and\
            not grid[self.row - 1][self.col -1].is_landmine():
                self.neighbors.append(grid[self.row - 1][self.col -1])

        # Check the down-right cube
        if self.col < self.total_rows - 1 and\
            self.row < self.total_rows - 1 and\
            not grid[self.row +1][self.col + 1].is_landmine():
                self.neighbors.append(grid[self.row +1][self.col + 1])

        # Check the down-left cube
        if self.col > 0 and\
            self.row < self.total_rows-1 and\
            not grid[self.row +1][self.col-1].is_landmine():
                self.neighbors.append(grid[self.row +1][self.col-1])

        return self.neighbors

def reveal(grid, cube, window, landmine_pos):
    if cube.is_closed() or cube.is_flag():
        return True

    if cube.is_landmine():
        for pos in landmine_pos:
            if not grid[pos[0]][pos[1]].is_flag():
                grid[pos[0]][pos[1]].color = black
        return False

    cube.make_closed()
    # reveal neighbors' number
    if cube.num == 0:
        for neighbor_cube in cube.get_neighbors(grid):
            # reveal neighbors
            reveal(grid, neighbor_cube, window, landmine_pos)
    # else, reveal only self number
    return True

def window_draw(window, grid, total_rows):
    window.fill(white)

    # draw the cubes.
    for row in grid:
        for cube in row:
            cube.draw_cube(window)

    draw_line(window, total_rows)
    pygame.display.update()

def win_msg(window, win_width = 800):
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 100, bold=True)
    num = font.render("YOU WIN!!!", True, (200,0,200))
    window.blit(num, (190, win_width //2 - 100))
    pygame.display.update()

def lose_msg(window, win_width = 800):
    pygame.font.init()
    font = pygame.font.SysFont("Arial", 100, bold=True)
    num = font.render("YOU LOSE!!!", True, (200,0,200))
    window.blit(num, (190, win_width //2 - 100))
    pygame.display.update()


def make_grid(width,  total_rows):
    grid = []
    gap  = width // total_rows
    for i in range(total_rows):
        grid.append([])
        for j in range(total_rows):
            cube = Cube(i, j, gap, total_rows)
            grid[i].append(cube)
    return grid

def draw_line(window, total_rows):
    gap = win_width // total_rows
    grid_length = gap * total_rows
    for i in range(total_rows +1):
        # horizontal line
        pygame.draw.line(window, grey, (0, i*gap),(grid_length, i*gap))
        for j in range(total_rows +1):
            # vertical line
            pygame.draw.line(window, grey, (j*gap, 0), (j*gap, grid_length))

# A function transfrom the mouse position in to the node position.
def get_click_pos(mouse_pos, win_width, total_rows):
    gap = win_width // total_rows

    cube_row = mouse_pos[1] // gap
    cube_col = mouse_pos[0] // gap

    return cube_row, cube_col

def gen_landmine_pos(grid, num = 10): # non-repeated pos of landmines generator
    landmine_pos = set([])
    while len(landmine_pos) < num:
        land_row = random.randint(0, len(grid)-1)
        land_col = random.randint(0, len(grid[0])-1)
        landmine_pos.add((land_row, land_col))
    for pos in landmine_pos:
        landmine = grid[pos[0]][pos[1]]
        landmine.make_landmine()
    return landmine_pos

''' Update_num part needs to fix the index problem that exceed the grid
    >>> 7/25 fixed
'''
def update_num(landmine_pos, grid): # after generating landmines, update cube number
    for pos in landmine_pos:
        if grid[pos[0]][pos[1]].is_landmine():
            landmine = grid[pos[0]][pos[1]]
            if landmine.row > 0 and\
                not grid[landmine.row - 1][landmine.col].is_landmine(): # up
                grid[landmine.row - 1][landmine.col].num += 1

            if landmine.row < (len(grid)-1) and\
                not grid[landmine.row + 1][landmine.col].is_landmine(): # down
                grid[landmine.row + 1][landmine.col].num += 1

            if landmine.col > 0 and\
                not grid[landmine.row][landmine.col - 1].is_landmine(): # left
                grid[landmine.row][landmine.col - 1].num += 1

            if landmine.col < (len(grid[0]) - 1) and\
                not grid[landmine.row][landmine.col + 1].is_landmine(): # right
                grid[landmine.row][landmine.col + 1].num += 1

            if landmine.row > 0 and landmine.col > 0 and\
                not grid[landmine.row - 1][landmine.col - 1].is_landmine(): # up left
                grid[landmine.row - 1][landmine.col - 1].num += 1

            if landmine.row > 0 and landmine.col < (len(grid[0])-1) and\
                not grid[landmine.row - 1][landmine.col + 1].is_landmine(): # up right
                grid[landmine.row - 1][landmine.col + 1].num += 1

            if landmine.row < (len(grid) -1) and landmine.col > 0 and\
                not grid[landmine.row + 1][landmine.col - 1].is_landmine(): # down left
                grid[landmine.row + 1][landmine.col -1].num += 1

            if landmine.row < (len(grid)-1) and landmine.col < (len(grid[0])-1) and\
                not grid[landmine.row + 1][landmine.col + 1].is_landmine(): # down right
                grid[landmine.row + 1][landmine.col + 1].num += 1


def main(window, win_width, total_rows = 20):
    # init
    grid = make_grid(win_width, total_rows)
    landmine_num = round(0.2 * total_rows ** 2)
    landmine_pos = gen_landmine_pos(grid, landmine_num)
    update_num(landmine_pos, grid)


    clock = pygame.time.Clock() #limit the fps
    run = True
    end = False

    while run:
        clock.tick(fps)  # fps control
        # Game ending condition
        while end:
            if landmine_num == 0:
                win_msg(window, win_width)
            else:
                lose_msg(window,win_width)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        # init
                        end = None
                        grid = make_grid(win_width, total_rows)
                        landmine_num = round(0.2 * total_rows ** 2)
                        landmine_pos = gen_landmine_pos(grid, landmine_num)
                        update_num(landmine_pos, grid)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    # init
                    end = None
                    grid = make_grid(win_width, total_rows)
                    landmine_num = round(0.2 * total_rows ** 2)
                    landmine_pos = gen_landmine_pos(grid, landmine_num)
                    update_num(landmine_pos, grid)

            # end boolean to control whether player can continue playing.
            if not end:
                # Set the mouse click interaction, assigning the node colors
                if pygame.mouse.get_pressed()[0]:  # left click
                    mouse_pos = pygame.mouse.get_pos()  # return the mouse click pos
                    pos = get_click_pos(mouse_pos, win_width, total_rows)
                    selected_cube = grid[pos[1]][pos[0]]
                    if not reveal(grid, selected_cube, window, landmine_pos): # click on landmines
                        end = True

                if pygame.mouse.get_pressed()[2]:  # right click
                    mouse_pos = pygame.mouse.get_pos()  # return the mouse click pos
                    pos = get_click_pos(mouse_pos, win_width, total_rows)
                    flag_cube = grid[pos[1]][pos[0]]


                    if not flag_cube.is_closed():
                        if flag_cube.is_flag():
                            flag_cube.reset() # reset color back to white
                            if flag_cube.num == -1:
                                landmine_num += 1
                            #print(landmine_num)
                        # MAX num of flags = num of landmines.
                        # if exceed max num, then can't put flag anymore.
                        else:
                            flag_cube.make_flag()
                            if flag_cube.num == -1:
                                landmine_num -= 1
                            #print(landmine_num)
                    #print(landmine_num)

        window_draw(window, grid, total_rows)
    pygame.quit()



main(window, win_width, 20)