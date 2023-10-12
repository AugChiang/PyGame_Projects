import pygame as pg
import time
import random
import math

pg.init()

WIDTH, HEIGHT = 800, 600
STAT_HEIGHT = 40
WIN = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Aiming Trainer")
FPS = 60
LIVES = 3

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200 ,200)
BG_COLOR = (0, 20, 40)

# define the customized event
TARGET_SPAWN_T = 400 # every N ms will spawn a new target
TARGET_EVENT = pg.USEREVENT
TARGET_PADDING = 40

# status bar 
LABEL_FONT = pg.font.SysFont("comicsans", 32)

class Target:
    MAX_SIZE = 30 # max size and start shrinking
    GROWTH_RATE = 0.4 # pixels grow per frame
    COLOR = RED
    COLOR2 = WHITE
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True
    
    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False
        
        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win):
        # where to draw, color, center pos, radius
        # draw the ring shape, notice the order affects the overlapping
        pg.draw.circle(win, self.COLOR, (self.x, self.y),
                       self.size)
        pg.draw.circle(win, self.COLOR2, (self.x, self.y),
                       self.size*0.7)
        pg.draw.circle(win, self.COLOR, (self.x, self.y),
                       self.size*0.5)
        pg.draw.circle(win, self.COLOR2, (self.x, self.y),
                       self.size*0.3)
    
    def collide(self, x, y):
        '''
        track click pos whether within the target
        '''
        d = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return d <= self.size

def draw_targets(win, targets):
    '''
    win: where to draw: obj
    targets: list of target obj
    '''
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)

def format_time(secs):
    milli = math.floor(int(secs*1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"

def draw_stat(win, elapsed_time, target_pressed, misses):
    pg.draw.rect(win, GREY, (0,0, WIDTH, STAT_HEIGHT))
    time_label = LABEL_FONT.render(
        f"TIME: {format_time(elapsed_time)}", 1, BLACK)

    agi = round(target_pressed/elapsed_time, 1)
    agi_label = LABEL_FONT.render(f"Rate: {agi} #/s", 1, BLACK)

    hits_label = LABEL_FONT.render(f"Hits: {target_pressed}", 1, BLACK)
    lives_label = LABEL_FONT.render(f"Life:  {LIVES - misses}", 1, BLACK)

    win.blit(time_label, (8, 10))
    win.blit(agi_label, (250, 10))
    win.blit(hits_label, (450, 10))
    win.blit(lives_label, (650, 10))

def get_mid(surface):
    return (WIDTH - surface.get_width()) / 2

def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(
        f"TIME: {format_time(elapsed_time)}", 1, WHITE)

    agi = round(targets_pressed/elapsed_time, 1)
    agi_label = LABEL_FONT.render(f"Rate: {agi} #/s", 1, WHITE)

    hits_label = LABEL_FONT.render(f"Hits: {targets_pressed}", 1, WHITE)
    acc = round(targets_pressed / clicks *100, 1) if clicks != 0 else 0
    acc_label = LABEL_FONT.render(F"Accuracy: {acc} %", 1, WHITE)

    win.blit(time_label, (get_mid(time_label), HEIGHT*0.3))
    win.blit(agi_label, (get_mid(agi_label), HEIGHT*0.4))
    win.blit(hits_label, (get_mid(hits_label), HEIGHT*0.5))
    win.blit(acc_label, (get_mid(acc_label), HEIGHT*0.6))
    
    pg.display.update()
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN:
                quit()

def main():
    run = True
    targets = []
    clock = pg.time.Clock()
    target_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()


    # trigger event, every N msec
    pg.time.set_timer(TARGET_EVENT, TARGET_SPAWN_T)

    while run:
        clock.tick(FPS)
        mouse_pos = pg.mouse.get_pos() # (x, y) tuple
        click = False
        elapsed_time = time.time() - start_time

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
                
            if event.type == TARGET_EVENT:
                # randomly generate target
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(STAT_HEIGHT + TARGET_PADDING, HEIGHT - TARGET_PADDING)
                target = Target(x, y)
                targets.append(target)
            if event.type == pg.MOUSEBUTTONDOWN:
                click = True
                clicks += 1
        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                misses += 1
            
            # if mouse click pos is within the target
            if click and target.collide(*mouse_pos):
                targets.remove(target)
                target_pressed += 1

        if misses >= LIVES:
            end_screen(WIN, elapsed_time, target_pressed, clicks) # end the game
            
    
        draw_targets(WIN, targets)
        draw_stat(win=WIN, elapsed_time=elapsed_time,
                  target_pressed=target_pressed, misses=misses)
        pg.display.update()


if __name__ == "__main__":
    main()