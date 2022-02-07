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
        self._gravity = 0.5

        self.rect = pg.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.col = pymath.Vector3(255, 255, 255) # temp color

    def tick(self):
        self.movementHandler()
        self.gravity()
        self.checkCollisions()

        self.pos.x += self.speed.x
        self.pos.y += self.speed.y

        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

        pydraw.rect(screen, self.col, self.rect)

    def movementHandler(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.speed.x = -4
        if keys[pg.K_d]:
            self.speed.x = 4

    def checkCollisions(self):
        for block in blockList:
            if self.rect.colliderect(block):
                #if self.rect.bottom <= block.rect.top:
                self.speed.y = -0.1
    
    def gravity(self):
        if self.speed.y <= 15:
            self.speed.y += self._gravity

class Block:
    def __init__(self, pos, size):
        self.pos = pymath.Vector2(pos)
        self.size = pymath.Vector2(size)
        self.col = pymath.Vector3(128, 128, 128) # temp color
        
        self.rect = pg.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def tick(self):
        pydraw.rect(screen, self.col, self.rect)

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

blockList = []

player = Player((30, 30))

block = Block((0, SCREEN_HEIGHT - 20), (SCREEN_WIDTH, 100))
blockList.append(block)

while isRunning == True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()

    screen.fill((0, 0, 0))

    for block in blockList:
        block.tick()

    player.tick()

    pg.display.update()
    clock.tick(FPS)

quit()
