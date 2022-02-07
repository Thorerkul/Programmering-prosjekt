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
        self.max_speed = 6
        self.canJump = False
        self.prev_keys = []

        self.rect = pg.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.col = pymath.Vector3(255, 255, 255) # temp color

    def tick(self):
        self.gravity()
        self.checkCollisions()
        self.movementHandler()

        self.pos.x += self.speed.x
        self.pos.y += self.speed.y

        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

        pydraw.rect(screen, self.col, self.rect)

    def movementHandler(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.speed.x = 0 - self.max_speed
        else:
            self.speed.x = 0
        if keys[pg.K_d]:
            self.speed.x = self.max_speed
            
        if keys[pg.K_SPACE] and self.canJump:
            self.speed.y = 0 - self.max_speed * 2.2
            
        if keys[pg.K_e] != self.prev_keys[pg.K_e] and keys[pg.K_e]:
            self.pickup()
        
        self.canJump = False
        self.prev_keys = keys

    def checkCollisions(self):
        for block in blockList:
            if self.rect.colliderect(block):
                if self.rect.centery <= block.rect.centery:
                    self.speed.y = -0.25
                    self.canJump = True
                else:
                    self.speed.y = 2
    
    def gravity(self):
        if self.speed.y <= 15:
            self.speed.y += self._gravity

    def pickup(self):
        for ball in ballList:
            if self.rect.colliderect(ball):
                if ball.isPickedUp:
                    ball.isPickedUp = False
                else:
                    ball.isPickedUp = True

class Block:
    def __init__(self, pos, size):
        self.pos = pymath.Vector2(pos)
        self.size = pymath.Vector2(size)
        self.col = pymath.Vector3(128, 128, 128) # temp color
        
        self.rect = pg.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def tick(self):
        pydraw.rect(screen, self.col, self.rect)

class Ball:
    def __init__(self, pos):
        self.pos = pymath.Vector2(pos)
        self.col = pymath.Vector3(255, 0, 0)
        self.size = 10
        self.speed = pymath.Vector2(0, 0)
        self.isPickedUp = False
        
        self.rect = pg.Rect(self.pos.x - self.size, self.pos.y - self.size, self.size * 2, self.size * 2)
        
    def tick(self):
        self.speed.y += 0.5
        for block in blockList:
            if self.rect.colliderect(block):
                if self.rect.centery <= block.rect.centery:
                    self.speed.y = -0.25
                else:
                    self.speed.y = 2
                    
        if self.isPickedUp:
            self.pos = player.pos
            self.speed = player.speed
                    
        self.pos.x += self.speed.x
        self.pos.y += self.speed.y
        
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
        
        pydraw.circle(screen, self.col, self.pos, self.size)

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
ballList = []

player = Player((30, 30))

block = Block((0, SCREEN_HEIGHT - 20), (SCREEN_WIDTH, 100))
blockList.append(block)

block = Block((60, 470), (100, 25))
blockList.append(block)

test = Ball((50, 50))
ballList.append(test)
test = Ball((1050, 50))
ballList.append(test)

while isRunning == True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()

    screen.fill((0, 0, 0))

    for block in blockList:
        block.tick()

    player.tick()
    
    for ball in ballList:
        ball.tick()

    pg.display.update()
    clock.tick(FPS)

quit()
