import sys, random, math
import pygame as pg
import pygame.math as pymath
import pygame.draw as pydraw

def quit():
    pg.quit()
    sys.exit()

import sys, random, math
import pygame as pg
import pygame.math as pymath
import pygame.draw as pydraw

class Player:
    def __init__(self, size, char="billy"):
        self.pos = pymath.Vector2(int(SCREEN_WIDTH / 2 - size[0] / 2), int(SCREEN_HEIGHT / 2 - size[1] / 2))
        self.size = pymath.Vector2(size)
        self.speed = pymath.Vector2(0, 0)
        self._gravity = 0.5
        self.max_speed = 6
        self.canJump = False
        self.prev_keys = []
        self.char = char
        self.lastMoveDir = pymath.Vector2(0, 0)
        self.hasBall = False

        self.rect = pg.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.col = pymath.Vector3(255, 255, 255) # temp color

        self.load_sprites()
        self.current_frame = 0

    def load_sprites(self):
        self.runningsprites = []

        if self.char == "billy":
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0001.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0002.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0003.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0004.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0005.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0006.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0007.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0009.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0010.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0011.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0012.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0013.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0014.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0015.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0016.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0017.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0018.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0019.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0020.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0021.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0022.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0023.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0024.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0025.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0026.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0027.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0028.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0029.png').convert_alpha())
            self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0030.png').convert_alpha())
            self.standingSprite = pg.image.load(r'src\assets\art\karakterer\Billy\billy0031.png').convert_alpha()
            self.airSprite = pg.image.load(r'src\assets\art\karakterer\Billy\billy0032.png').convert_alpha()

        # rescaling
        for i in range(len(self.runningsprites)):
            self.runningsprites[i] = pg.transform.scale(self.runningsprites[i], (int(self.size.x), int(self.size.y)))
        self.standingSprite = pg.transform.scale(self.standingSprite, (int(self.size.x), int(self.size.y)))
        self.airSprite = pg.transform.scale(self.airSprite, (int(self.size.x), int(self.size.y)))

    def tick(self):
        self.gravity()
        self.movementHandler()
        self.checkCollisions()

        self.pos.x += self.speed.x
        self.pos.y += self.speed.y

        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

        screen.blit(self.animation(), self.rect)

    def movementHandler(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.speed.x = 0 - self.max_speed
            self.lastMoveDir.x = -1
        else:
            self.speed.x = 0
        if keys[pg.K_d]:
            self.speed.x = self.max_speed
            self.lastMoveDir.x = 1
            
        if keys[pg.K_SPACE] and self.canJump:
            self.speed.y = 0 - self.max_speed * 2.2
        
        self.canJump = False
        self.prev_keys = pg.key.get_pressed()

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
                if self.hasBall

    def animation(self):
        self.current_frame += 1

        if self.current_frame >= 29:
            self.current_frame = 0

        if self.speed.x != 0 and self.speed.y <= 1 and self.speed.y >= 0:
            img = self.runningsprites[self.current_frame]

        elif self.speed.y >= 1.5 or self.speed.y <= -0.5:
            img = self.airSprite
        else:
            img = self.standingSprite

        if self.lastMoveDir.x == 1:
            img = pg.transform.flip(img, True, False)

        return img

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

player = Player((50, 50))

floor = Block((0, SCREEN_HEIGHT - 20), (SCREEN_WIDTH, 100))
blockList.append(floor)

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

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_e:
                player.pickup()

    screen.fill((0, 0, 0))

    for block in blockList:
        block.tick()

    player.tick()
    
    for ball in ballList:
        ball.tick()

    pg.display.update()
    clock.tick(FPS)

quit()
