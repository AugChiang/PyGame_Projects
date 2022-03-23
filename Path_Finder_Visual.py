import pygame
import math
from queue import PriorityQueue

# Set color constant
red = (255, 0, 0) # Visited
green = (0, 255, 0) # Not visited yet
blue = (0, 0, 255)
yellow = (255, 255, 0)
white = (255, 255, 255) # grid color
black = (0, 0, 0) # barrier
purple = (128, 0, 128)
orange = (255, 165, 0) # Start Point
grey = (128, 128, 128) # grid lines
turquoise = (64, 224, 208) # End point

#Set window size, here take a square as example
width = 800
window = pygame.display.set_mode((width, width))  # Display the window with the size 800*800
pygame.display.set_caption("A* Path Finding Algorithm Practice")  # Set the caption

# Node class keeps tracking the node color, type, etc.
class Node:
    def __init__(self, row, col, width, total_rows): # Node's location, size, and total rows(#nodes)
        self.row = row
        self.col = col

        # to draw a box area, need start location(x,y) and square width
        self.x = col * width
        self.y = row * width

        self.width =width
        self.total_rows = total_rows
        self.neighbors = []

        # default color is white
        self.color = white

    def get_pos(self):
        return self.row, self.col

    # Node states represented by colors
    def is_visited(self):
        return self.color == red

    def is_open(self):
        return self.color == green

    def is_barrier(self):
        return self.color == black

    def is_start(self):
        return self.color == orange

    def is_end(self):
        return self.color == turquoise

    # Assign color when mouse clicks
    def reset(self):
         self.color = white

    def make_visited(self):
         self.color = red

    def make_open(self):
         self.color = green

    def make_barrier(self):
         self.color = black

    def make_start(self):
         self.color = orange

    def make_end(self):
         self.color = turquoise

    def make_path(self):
         self.color = purple

    #pygame draw the screen with rectangle size
    def draw(self, window):
        pygame.draw.rect(window, self.color,(self.x, self.y, self.width, self.width))

    # add neighbors nodes into self.neighbors list
    def update_neighbors(self, grid):
        self.neighbors = []
        # Check the down node
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        # Check the up node
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        # Check the right node
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

        # Check the left node
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    # Compare the nodes
    def __lt__(self, other):
        return False

# The width and length distance from two points
def L_distance(p1,p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1-x2) + abs(y1 - y2)

def draw_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

# the finding shortest path algorithm
def algorithm(draw, grid, start, end):
    cnt = 0  # this parameter is used to record when the nodes added into the priority queue
    open_set = PriorityQueue() # priority queue gives us the item that has the smallest attribute we assign.

    # keep track of the passing nodes: use dictionary
    came_from = {}

    # object in queue = (predicted_length, added order, node)
    open_set.put((0, cnt, start)) #put the start point into the queue
    '''
    length_so_far: keep tracking the shortest path length from start to current node.
    before started, all nodes are infinity from start point.
    '''
    length_so_far = {node: float("inf") for row in grid for node in row}
    length_so_far[start] = 0

    '''
    predicted_length: keep tracking the estimated path length from current node to the end point.
    '''
    predicted_length = {node: float("inf") for row in grid for node in row}
    '''
    the statement below: it won't recognize it's shortest path as soon as reaching the end point.
    therefore, take the L-estimated distance as from start to the end point.
    '''
    predicted_length[start] = L_distance(start.get_pos(), end.get_pos())

    # Check if there is anything in the priority queue

    open_set_hash = {start}

    # the algorithm stops when checking all the item in the queue and still can't get path.
    while not open_set.empty():
        for event in pygame.event.get():
            # set the "X" button check so we can halt the algorithm
            # though, we already have one quit-event check in the main(),
            # this for-loop has its own loop.
            if event.type == pygame.QUIT:
                pygame.quit()

        # the index is set to 2, because the open_set stores: predicted_length, cnt, and nodes (line 121)
        current = open_set.get()[2] # we want just the node
        open_set_hash.remove(current) # sync the priority queue when we pop.

        # if the node we pop is the end point, then draw the path
        if current == end:
            draw_path(came_from, current, draw)
            end.make_end() # so that path won't draw onto the end point.
            return True

        for neighbor in current.neighbors:
            # length_so_far from current node to its neighbor is just length_so_far+1.
            temp_weight = length_so_far[current] + 1
            # compare the current path to A neighbor and the historic length_so_far of A neighbor by another path.
            if temp_weight < length_so_far[neighbor]:
                # update the length_so_far (path), since, now we are on the shorter path, comparing to the historic data.
                came_from[neighbor] = current

                # update the length_so_far from current node to its neighbor.
                length_so_far[neighbor] = temp_weight

                # update the estimated path length from current node to end point.
                # remember L_distance need two node position as parameters.
                predicted_length[neighbor] = temp_weight + L_distance(neighbor.get_pos(), end.get_pos())

                # use open_set_hash to check if the neighbor is in or not.
                if neighbor not in open_set_hash:
                    cnt += 1 # added order

                    # since the current has better path than we found before.
                    open_set.put((predicted_length[neighbor], cnt, neighbor))
                    # add to the duplicated priority queue too.
                    open_set_hash.add(neighbor)
                    neighbor.make_open() # make the neighbor to be the next "current" node we want to start with.
        draw()

        # finishing exploring the current node.
        if current != start:
            current.make_visited()

    # we didn't find the path
    return False


# Create the nodes set, which is the slices of the window.
'''
In other words, the grid(list) is like: 
(N stands for node object)

[ 1st row: N(1,1), N(1,2), N(1,3)... , N(1,n)
  2nd row: N(2,1), N(2,2), N(2,3)... , N(2,n)
  ...
  last row: N(n,1), N(n,2), N(n,3)... , N(n,n) ]
  
'''
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        # grid rows set
        grid.append([])
        for j in range(rows):
            # add node objects into every row set.
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

# Draw the lines of grid
def draw_lines(window, rows, width):
    gap = width // rows
    # Draw the horizontal lines.
    for i in range(rows):
        pygame.draw.line(window,grey,(0, i*gap),(width, i*gap))
        # Draw the vertical lines.
        for j in range(rows):
            pygame.draw.line(window,grey,(j*gap, 0),(j*gap, width))

# the main draw function, updating every frame.
def window_draw(window, grid, rows, width):
    # base background color
    window.fill(white)

    # draw the nodes.
    for row in grid:
        for node in row:
            node.draw(window) # the draw here is the class method in line 81.

    # draw the lines.
    draw_lines(window, rows, width)

    # update the drawing above on display
    pygame.display.update()


# A function transfrom the mouse position in to the node position.
def get_click_pos(mouse_pos, rows, width):
    gap = width // rows

    node_row = mouse_pos[1] // gap
    node_col = mouse_pos[0] // gap

    return node_row, node_col

def main(window, width):
    # take rows as constant temporarily
    rows = 40

    # generates the 2D array of the nodes' set
    grid = make_grid(rows, width)

    start = None # is the start point been placed yet.
    end = None # is the end point been placed yet.
    run = True

    while run:
        window_draw(window, grid, rows, width)
        # check every event(click, input, etc.)
        # all checks need to be in this for-loop
        for event in pygame.event.get():
            # the "X" button of the window should ensure us to end the process.
            if event.type == pygame.QUIT:
                run = False

            # Set the mouse click interaction, assigning the node colors
            if pygame.mouse.get_pressed()[0]: # left click
                mouse_pos = pygame.mouse.get_pos() # return the mouse click pos
                row, col = get_click_pos(mouse_pos, rows, width) #use the function to get the node pos in grid.
                node = grid[row][col]
                if not start and node!= end: # means not yet put the start position.
                    start = node
                    start.make_start()

                elif not end and node != start: # not yet put the ned position.
                    end = node
                    end.make_end()

                elif node != start and node != end:
                    barrier = node
                    barrier.make_barrier()
            elif pygame.mouse.get_pressed()[2]: # right click
                mouse_pos = pygame.mouse.get_pos() # return the mouse click pos
                row, col = get_click_pos(mouse_pos, rows, width) #use the function to get the node pos in grid.
                node = grid[row][col]
                node.reset() # right click to reset the node into white color.
                if node == start:
                    start = None
                elif node == end:
                    end = None

            # when press space then start the algorithm.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithm(lambda: window_draw(window, grid, rows, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(rows, width)

    pygame.quit()

main(window, width)