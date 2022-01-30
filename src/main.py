import sys, random, math
import pygame as pg
import pygame.math as pymath
import pygame.draw as pydraw

def quit():
    pg.quit()
    sys.exit()

class Player:
    def __init__(self, size):
        self.pos = pymath.Vector2(int(SCREEN_WIDTH / 2 - size[0] / 2), int(SCREEN_HEIGHT / 2 - size[1] / 2))
        self.size = pymath.Vector2(size)
        self.speed = pymath.Vector2(0, 0)

        self.truepos = pymath.Vector2(self.pos)
        self.truespeed = pymath.Vector2(self.speed)

        self.rect = pg.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.col = pymath.Vector3(255, 255, 255) # temp color

    def tick(self):
        self.check_input()

        self.truepos.x += self.truespeed.x
        self.truepos.y += self.truespeed.y

        self.rect.centerx = self.truepos.x
        self.rect.centery = self.truepos.y

        pydraw.rect(screen, self.col, self.rect)

    def check_input(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            self.pos.y -= 4
        if keys[pg.K_s]:
            self.pos.y += 4
        if keys[pg.K_a]:
            self.pos.x -= 4
        if keys[pg.K_d]:
            self.pos.x += 4

pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()

window = pg.display.Info()

SCREEN_WIDTH = window.current_w - 90
SCREEN_HEIGHT = window.current_h - 90
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
game_font = pg.font.Font(None, 25)
isRunning = True
FPS = 60

player = Player((30, 30))

while isRunning == True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()

    screen.fill((0, 0, 0))

    player.tick()

    pg.display.update()
    clock.tick(FPS)

quit()