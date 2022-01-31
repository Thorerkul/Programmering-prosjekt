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
        self.movementHandler()
        self.checkCollisions()

        self.truepos.x += self.truespeed.x
        self.truepos.y += self.truespeed.y

        self.rect.centerx = self.truepos.x
        self.rect.centery = self.truepos.y

        pydraw.rect(screen, self.col, self.rect)

    def movementHandler(self):
        def try_move(x, y):
            for block in blockList:
                if self.rect.colliderect(block.rect) == False:
                    self.speed.x = x
                    self.speed.y = y

        keys = pg.key.get_pressed()

        if keys[pg.K_w]:
            try_move(0, -4)
        else:
            self.speed.y = 0
        if keys[pg.K_s]:
            try_move(0, 4)

        if keys[pg.K_a]:
            try_move(-4, 0)
        else:
            self.speed.x = 0
        if keys[pg.K_d]:
            try_move(4, 0)

        if keys[pg.K_w] and keys[pg.K_a]:
            try_move(-4, -4)
        if keys[pg.K_w] and keys[pg.K_d]:
            try_move(4, -4)

        if keys[pg.K_s] and keys[pg.K_a]:
            try_move(-4, 4)
        if keys[pg.K_s] and keys[pg.K_d]:
            try_move(4, 4)

    def checkCollisions(self):
        for block in blockList:
            if self.rect.colliderect(block.realrect):
                self.speed.x += 0 - self.speed.x * 2
                self.speed.y += 0 - self.speed.y * 2

class Block:
    def __init__(self, pos, size):
        self.pos = pymath.Vector2(pos)
        self.size = pymath.Vector2(size)
        self.col = pymath.Vector3(128, 128, 128) # temp color

        self.truepos = pymath.Vector2(self.pos)
        self.truespeed = pymath.Vector2(0, 0)
        
        self.rect = pg.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.realrect = pg.Rect(self.pos.x - 10, self.pos.y - 10, self.size.x + 20, self.size.y + 20)

    def tick(self):
        #if self.rect.colliderect(player) == False:
        self.camera()

        self.truepos.x += self.truespeed.x
        self.truepos.y += self.truespeed.y

        self.rect.centerx = self.truepos.x
        self.rect.centery = self.truepos.y

        #
        self.realrect.centerx = self.truepos.x
        self.realrect.centery = self.truepos.y
        #

        pydraw.rect(screen, (255, 0, 0), self.realrect)
        pydraw.rect(screen, self.col, self.rect)

    def camera(self):
        self.truespeed.x = 0 - player.speed.x
        self.truespeed.y = 0 - player.speed.y

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

block = Block((0, 0), (100, 100))
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