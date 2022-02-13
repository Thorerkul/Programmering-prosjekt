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

        self.rect = pg.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)
        self.col = pymath.Vector3(255, 255, 255) # temp color

        self.load_sprites()
        self.current_frame = 0

    def load_sprites(self):
        self.runningsprites = []

        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0001.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0002.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0003.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0004.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0005.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0006.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0007.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0009.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0010.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0011.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0012.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0013.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0014.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0015.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0016.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0017.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0018.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0019.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0020.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0021.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0022.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0023.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0024.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0025.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0026.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0027.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0028.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0029.png'))
        self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0030.png'))

    def tick(self):
        self.gravity()
        self.checkCollisions()
        self.movementHandler()

        self.pos.x += self.speed.x
        self.pos.y += self.speed.y

        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

        screen.blit(self.animation(), self.rect)

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
            
        #if keys[pg.K_e]!= self.prev_keys[pg.K_e] and keys[pg.K_e]:
            #self.pickup()
        
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

    def animation(self):
        self.current_frame += 1
        if self.current_frame >= 29:
            print(self.current_frame)
            self.current_frame = 0
        return self.runningsprites[self.current_frame]

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