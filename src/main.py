import sys, random, math
import pygame as pg
import pygame.math as pymath
import pygame.draw as pydraw

def quit():
    pg.quit()
    sys.exit()

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

        self.loadSprites()
        self.current_frame = 0

    def loadSprites(self):
        self.runningsprites = []
        self.holdingsprites = []

        if self.char == "billy":
            path = 'src\\assets\\art\\karakterer\\Billy\\billy00'
            for i in range(30):
                if i >= 9:
                    file = path + str(i + 1) + '.png'
                else:
                    file = path + '0' + str(i + 1) + '.png'

                self.runningsprites.append(pg.image.load(file).convert_alpha())

            for i in range(30):
                file = path + str(i + 32) + '.png'
                print(file)

                self.holdingsprites.append(pg.image.load(file).convert_alpha())

            self.standingSprite = pg.image.load(r'src\assets\art\karakterer\Billy\billyStanding.png').convert_alpha()
            self.airSprite = pg.image.load(r'src\assets\art\karakterer\Billy\billyAir.png').convert_alpha()

            # self.runningsprites.append(pg.image.load(r'src\assets\art\karakterer\Billy\billy0001.png').convert_alpha())

        # rescaling
        for i in range(len(self.runningsprites)):
            self.runningsprites[i] = pg.transform.scale(self.runningsprites[i], (int(self.size.x), int(self.size.y)))
        for i in range(len(self.holdingsprites)):
            self.holdingsprites[i] = pg.transform.scale(self.holdingsprites[i], (int(self.size.x), int(self.size.y)))
        self.standingSprite = pg.transform.scale(self.standingSprite, (int(self.size.x), int(self.size.y)))
        self.airSprite = pg.transform.scale(self.airSprite, (int(self.size.x), int(self.size.y)))

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

        if self.rect.right >= SCREEN_WIDTH - 10:
            while self.rect.right >= SCREEN_WIDTH - 10:
                self.pos.x -= 1

                self.rect.centerx = self.pos.x
                self.rect.centery = self.pos.y
                
        if self.rect.left <= 10:
            while self.rect.left <= 10:
                self.pos.x += 1
                
                self.rect.centerx = self.pos.x
                self.rect.centery = self.pos.y
    
    def gravity(self):
        if self.speed.y <= 15:
            self.speed.y += self._gravity

    def pickup(self):
        if self.hasBall == False:
            for ball in ballList:
                if self.rect.colliderect(ball):
                    ballList.remove(ball)
                    del ball
                    self.hasBall = True
        else:
            mouse_pos = pymath.Vector2(pg.mouse.get_pos())
            dir = pymath.Vector2(mouse_pos.x - self.pos.x, mouse_pos.y - self.pos.y)
            dir = dir.normalize()

            dir = (dir[0] * 25, dir[1] * 25)

            ball = Ball((self.pos.x, self.pos.y), speed=dir)
            ballList.append(ball)
            self.hasBall = False

    def animation(self):
        # print(self.current_frame)

        if self.speed.x != 0 and self.speed.y <= 1 and self.speed.y >= 0:
            self.current_frame += 1
            if self.current_frame >= len(self.runningsprites):
                self.current_frame = 0

            if self.hasBall == False:
                img = self.runningsprites[self.current_frame]
            else:
                img = self.holdingsprites[self.current_frame]

        elif self.speed.y >= 1.75 or self.speed.y <= -0.75:
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
    def __init__(self, pos, speed=(0, 0)):
        self.pos = pymath.Vector2(pos)
        self.col = pymath.Vector3(255, 0, 0)
        self.size = 10
        self.speed = pymath.Vector2(speed)
        
        self.rect = pg.Rect(self.pos.x - self.size, self.pos.y - self.size, self.size * 2, self.size * 2)
        
    def tick(self):
        if self.speed.y < 15:
            self.speed.y += 0.5
        for block in blockList:
            if self.rect.colliderect(block):
                if self.rect.bottom <= block.rect.top + 20:
                    while self.rect.colliderect(block):
                        self.pos.y -= 0.1

                        self.rect.centerx = self.pos.x
                        self.rect.centery = self.pos.y

                    self.speed.y = 0 - self.speed.y / 1.3
                    self.speed.x /= 1.1
                else:
                    while self.rect.colliderect(block):
                        self.pos.y += 0.1

                        self.rect.centerx = self.pos.x
                        self.rect.centery = self.pos.y
                    self.speed.y = 0 - self.speed.y / 1.3
                    self.speed.x /= 1.1

        if self.rect.right >= SCREEN_WIDTH - 10:
            if self.speed.x >= 0:
                self.speed.x = 0 - self.speed.x / 1.3
        if self.rect.left <= 10:
            if self.speed.x <= 0:
                self.speed.x = 0 - self.speed.x / 1.3
                    
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

block = Block((60, 470), (100, 30))
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
