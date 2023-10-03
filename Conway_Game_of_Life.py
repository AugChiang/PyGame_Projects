'''
Rule #1: Underpopulation
A live cell with fewer than 2 live neighbors dies.

Rule #2: Survival
A live cell with 2 or 3 live neighbors remains alive.

Rule #3: Overpopulation
A live cell with more than 3 live neighbors dies.

Rule #4: Reproduction
A dead cell with exactly 3 live neighbors becomes alive.
'''

import pygame as pg
import random
from collections import deque

pg.init()

BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (128,128,128)
YELLOW = (255,255,0)

WIDTH, HEIGHT = 800, 800
LINE_CHART_WIDTH, LINE_CHART_HEIGHT = 200, 200
CELL_SIZE = 10
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

FPS = 120

pg.font.init()
currfont = pg.font.SysFont("Arial", 24, bold=True)
localmaxfont = pg.font.SysFont("Arial", 24, bold=True)
liveratio = pg.font.SysFont("Arial", 24, bold=True)
historymaxfont = pg.font.SysFont("Arial", 24, bold=True)
MAX_LIVE = 1

screen = pg.display.set_mode((WIDTH, HEIGHT+LINE_CHART_HEIGHT))
clock = pg.time.Clock()

def draw_grid(positions):
  for pos in positions:
    col, row = pos
    # top left corner
    topLeft = (col*CELL_SIZE, row*CELL_SIZE)
    pg.draw.rect(screen, YELLOW, (*topLeft, CELL_SIZE, CELL_SIZE))

  for row in range(GRID_HEIGHT+1):
    # where to draw, color, start point, end point
    pg.draw.line(screen, GREY, (0, row*CELL_SIZE), (WIDTH, row*CELL_SIZE))

  for col in range(GRID_WIDTH):
    # where to draw, color, start point, end point
    pg.draw.line(screen, GREY, (col*CELL_SIZE, 0), (col*CELL_SIZE, HEIGHT))

def gen(num):
  return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)])

# just need to check the cells that are alive,
# no need to check all the cells!!!
def adjust_grid(positions):
  # update the cells need to copy a new one for updating the set,
  # or it will affect the current cells.
  all_neighbors = set()
  new_positions = set()

  # 'positions' are live cells
  for pos in positions:
    neighbors = get_neighbors(pos)
    all_neighbors.update(neighbors)

    # is the 'pos' a live cell, and keep it if 'yes'
    neighbors = list(filter(lambda x: x in positions, neighbors))

    # Rule No. 2
    if len(neighbors) in [2,3]: # if == 2 or 3
      new_positions.add(pos)

  # all neighbors (live cells)
  for pos in all_neighbors:
    neighbors = get_neighbors(pos)
    neighbors = list(filter(lambda x: x in positions, neighbors))

    # Rule No.4
    if len(neighbors) == 3:
      new_positions.add(pos)

  return new_positions

def get_neighbors(pos):
  x, y = pos
  neighbors = []
  for dx in [-1, 0, 1]:
    if x+dx < 0 or x+dx >= GRID_WIDTH:
      continue
    for dy in [-1, 0, 1]:
      if y+dy < 0 or y+dy >= GRID_HEIGHT:
        continue
      if dx == 0 and dy == 0:
        continue

      neighbors.append((x+dx, y+dy))

  return neighbors

def draw_line_chart(xdata):
  global MAX_LIVE
  ymax = max(xdata) if xdata else 1
  if ymax > MAX_LIVE:
    MAX_LIVE = ymax
  for idx, y in enumerate(xdata):
    # print(idx, y)
    currnum = currfont.render("Current: "+str(y), True, WHITE, BLACK)
    ratio = liveratio.render("Live Ratio: "+str(round(y/ymax, 2)), True, WHITE, BLACK)
    screen.blit(currnum, (620, 870))
    screen.blit(ratio, (620, 900))
    pg.draw.rect(screen, YELLOW, (15*idx, ((HEIGHT+LINE_CHART_HEIGHT) - LINE_CHART_HEIGHT*y//ymax+40), 12, LINE_CHART_HEIGHT*y//ymax))

  recentmax = localmaxfont.render("Recent Max: "+str(ymax), True, WHITE, BLACK)
  totalmax = historymaxfont.render("History Max: "+str(MAX_LIVE), True, WHITE, BLACK)
  screen.blit(recentmax, (620, 930))
  screen.blit(totalmax, (620, 960))

def main():
  run = True
  positions = set()
  playing = False
  count = 0
  update_freq = 30
  num_of_live_cells = deque(maxlen=40)

  while run:
    clock.tick(FPS)

    if playing:
      count += 1

    if count >= update_freq:
      count = 0
      positions = adjust_grid(positions)
      # print(len(positions))
      num_of_live_cells.append(len(positions))

    pg.display.set_caption("Playing" if playing else "Paused")

    for event in pg.event.get():
      if event.type == pg.QUIT:
        run = False
      # click to assign the cell
      if event.type == pg.MOUSEBUTTONDOWN:
        x, y = pg.mouse.get_pos()
        col = x // CELL_SIZE
        row = y // CELL_SIZE
        pos = (col, row)

        if pos in positions:
          positions.remove(pos)
        else:
          positions.add(pos)

      # click to clear the pos
      if event.type == pg.KEYDOWN:
        # pause
        if event.key == pg.K_SPACE:
          playing = not playing
        # clear all
        if event.key == pg.K_c:
          positions = set()
          playing = False
          count = 0
          num_of_live_cells = deque(maxlen=40)
        # generate random cells
        if event.key == pg.K_g:
          positions = gen(random.randrange(8, 20)*GRID_WIDTH)
    screen.fill(BLACK)
    draw_grid(positions)
    draw_line_chart(num_of_live_cells)
    pg.display.update()
  pg.quit()


if __name__ == "__main__":
  main()