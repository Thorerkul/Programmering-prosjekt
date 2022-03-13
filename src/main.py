from inspect import isfunction
import sys, random, math
import pygame as pg
import pygame.math as pymath
import pygame.draw as pydraw

def quit():
    pg.quit()
    sys.exit()

class Player:
    def __init__(self, size, pos, char="billy"):
        self.pos = pymath.Vector2(pos)
        self.size = pymath.Vector2(size)
        self.speed = pymath.Vector2(0, 0)
        self._gravity = 0.5
        self.max_speed = 6
        self.canJump = False
        self.prev_keys = []
        self.char = char
        self.lastMoveDir = pymath.Vector2(0, 0)
        self.hasBall = False
        self.isOnGround = False
        self.isGoingUp = False

        self.ballType = ""  

        self.jumpsfx = pg.mixer.Sound(r'src\assets\lyd\jump.wav')
        self.pickupsfx = pg.mixer.Sound(r'src\assets\lyd\pickup.wav')
        self.throwsfx = pg.mixer.Sound(r'src\assets\lyd\throw.wav')

        self.rect = pg.Rect(self.pos.x, self.pos.y, self.size.x - 10, self.size.y - 10)
        self.col = pymath.Vector3(255, 255, 255) # temp color

        self.loadSprites()
        self.current_frame = 0

    def loadSprites(self):
        self.runningsprites = []
        self.holdingsprites = []

        if self.char == "billy" or self.char == "dummy":
            path = 'src\\assets\\art\\karakterer\\Billy\\billy00'
            for i in range(30):
                if i >= 9:
                    file = path + str(i + 1) + '.png'
                else:
                    file = path + '0' + str(i + 1) + '.png'

                self.runningsprites.append(pg.image.load(file).convert_alpha())

            for i in range(30):
                file = path + str(i + 32) + '.png'

                self.holdingsprites.append(pg.image.load(file).convert_alpha())

            self.standingSprite = pg.image.load(r'src\assets\art\karakterer\Billy\billy0007.png').convert_alpha()
            self.airSprite = pg.image.load(r'src\assets\art\karakterer\Billy\billy0055.png').convert_alpha()

        if self.char == "bald" or self.char == "dummy":
            path = 'src\\assets\\art\\karakterer\\BaldGuy\\baldguy'
            for i in range(30):
                if i >= 9:
                    file = path + '00' + str(i + 1) + '.png'
                else:
                    file = path + '000' + str(i + 1) + '.png'

                print(file, i + 1)
                self.runningsprites.append(pg.image.load(file).convert_alpha())

            for i in range(30):
                file = path + str(i + 32) + '.png'

                self.holdingsprites.append(pg.image.load(file).convert_alpha())

            self.standingSprite = pg.image.load(r'src\assets\art\karakterer\BaldGuy\baldguy0007.png').convert_alpha()
            self.airSprite = pg.image.load(r'src\assets\art\karakterer\BaldGuy\baldguy0055.png').convert_alpha()

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
        self.selectBall()

        self.pos.x += self.speed.x
        self.pos.y += self.speed.y

        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

        screen.blit(self.animation(), self.rect)
        self.canJump = False

    def movementHandler(self):
        if self.char == "billy":
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
                if isMuted == False: self.jumpsfx.play()
            
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
                    self.ballType = ball.type
                    self.hasBall = True
                    if isMuted == False: self.pickupsfx.play()
                    ballList.remove(ball)
                    del ball
        else:
            mouse_pos = pymath.Vector2(pg.mouse.get_pos())
            dir = pymath.Vector2(mouse_pos.x - self.pos.x, mouse_pos.y - self.pos.y)
            dir = dir.normalize()

            dir = (dir[0] * 25, dir[1] * 25)
            
            dir = (0 - dir[0], 0 - dir[1])

            ball = Ball((self.pos.x, self.pos.y), speed=dir, type=self.ballType)
            ballList.append(ball)
            self.hasBall = False
            if isMuted == False: self.throwsfx.play()

    def animation(self):
        self.stateMachine()
        img = self.standingSprite

        if self.isOnGround:
            self.current_frame += 1
            if self.current_frame >= len(self.runningsprites):
                self.current_frame = 0
            if self.hasBall:
                img = self.holdingsprites[self.current_frame]
                if self.hasBall: self.drawBall()
            else:
                img = self.runningsprites[self.current_frame]
            if self.speed.x == 0:
                img = self.standingSprite
                if self.hasBall:
                    img = self.airSprite
        else:
            if self.isGoingUp and self.hasBall == False:
                img = self.standingSprite
            else:
                img = self.airSprite
                if self.hasBall: self.drawBall()

        if self.lastMoveDir.x == 1:
            img = pg.transform.flip(img, True, False)

        

        return img

    def stateMachine(self):
        for block in blockList:
            if self.rect.bottom + 3 <= block.rect.top:
                self.isOnGround = True
                break
            else:
                self.isOnGround = False
            # lazy programming
        if self.isOnGround:
            self.isOnGround = False
        else:
            self.isOnGround = True

        if self.speed.y < 2 and self.isOnGround == False:
            self.isGoingUp = True
        else:
            self.isGoingUp = False

    def drawBall(self):
        ball = Ball((self.pos.x, self.pos.y - self.size.y / 2 + 5), type=self.ballType)
        screen.blit(ball.image, ball.rect)
        del ball

    def selectBall(self):
        keys = pg.key.get_pressed()
        if self.hasBall:
            if keys[pg.K_1]:
                self.ballType = "basic"
            elif keys[pg.K_2]:
                self.ballType = "ice"
            elif keys[pg.K_3]:
                self.ballType = "steel"
            elif keys[pg.K_4]:
                self.ballType = "sun"
            elif keys[pg.K_5]:
                self.ballType = "nature"
            elif keys[pg.K_6]:
                self.ballType = "magic"
            elif keys[pg.K_7]:
                self.ballType = "soul"
            elif keys[pg.K_8]:
                self.ballType = "obsidian"

class Block:
    def __init__(self, pos, size):
        self.pos = pymath.Vector2(pos)
        self.size = pymath.Vector2(size)
        self.col = pymath.Vector3(128, 128, 128) # temp color
        
        self.rect = pg.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def tick(self):
        pydraw.rect(screen, self.col, self.rect)

class Ball:
    def __init__(self, pos, type="basic", speed=(0, 0)):
        self.pos = pymath.Vector2(pos)
        self.col = pymath.Vector3(255, 0, 0)
        self.size = 10
        self.speed = pymath.Vector2(speed)
        self.type = type

        self.bounceSound = pg.mixer.Sound(r'src\assets\lyd\ballBounce.wav')

        if self.type == "basic":
            self.image = pg.image.load(r'src\assets\art\Basic_ball.png').convert_alpha()
        elif self.type == "ice":
            self.image = pg.image.load(r'src\assets\art\ice_ball.png').convert_alpha()
        elif self.type == "steel":
            self.image = pg.image.load(r'src\assets\art\steel_ball.png').convert_alpha()
        elif self.type == "sun":
            self.image = pg.image.load(r'src\assets\art\Sun_ball.png').convert_alpha()
        elif self.type == "nature":
            self.image = pg.image.load(r'src\assets\art\nature_ball.png').convert_alpha()
        elif self.type == "magic":
            self.image = pg.image.load(r'src\assets\art\magic_ball.png').convert_alpha()
        elif self.type == "soul":
            self.image = pg.image.load(r'src\assets\art\soul_ball.png').convert_alpha()
        elif self.type == "obsidian":
            self.image = pg.image.load(r'src\assets\art\obsidian_ball.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (self.size + 9, self.size + 9))
        
        self.boucesLeft = 3
        self.isThrown = True
        
        self.rect = pg.Rect(self.pos.x - self.size, self.pos.y - self.size, self.size * 2, self.size * 2)

        if self.type == "soul":
            self.particlesystem = ParticleSystem(self.pos, (0, 0), -0.1, 1, (128, 0, 255), 5, 500, 1)
        
    def tick(self):
        self.specialUpdate()
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
                    if isMuted == False: self.bounceSound.play()
                    self.boucesLeft -= 1
                else:
                    while self.rect.colliderect(block):
                        self.pos.y += 0.1

                        self.rect.centerx = self.pos.x
                        self.rect.centery = self.pos.y
                    self.speed.y = 0 - self.speed.y / 1.3
                    self.speed.x /= 1.1
                    if isMuted == False: self.bounceSound.play()
                    self.boucesLeft -= 1

        if self.rect.right >= SCREEN_WIDTH - 10:
            if self.speed.x >= 0:
                self.speed.x = 0 - self.speed.x / 1.3
                if isMuted == False: self.bounceSound.play()
                self.boucesLeft -= 1
        if self.rect.left <= 10:
            if self.speed.x <= 0:
                self.speed.x = 0 - self.speed.x / 1.3
                if isMuted == False: self.bounceSound.play()
                self.boucesLeft -= 1
                
        for player in playerList:
            if self.rect.colliderect(player):
                if self.isThrown:
                    self.speed.x = 0 - self.speed.x
                    self.speed.y = 0 - self.speed.y
                    
                    while self.rect.colliderect(player):
                        self.pos.x += self.speed.x
                        self.pos.y += self.speed.y
                        
                        self.rect.centerx = self.pos.x
                        self.rect.centery = self.pos.y
                    self.boucesLeft -= 1
                    
        if self.boucesLeft <= 0:
            self.isThrown = False
                
        self.pos.x += self.speed.x
        self.pos.y += self.speed.y
        
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

        screen.blit(self.image, self.rect)
        if self.type == "soul":
            self.particlesystem.tick(self.pos)

    def specialUpdate(self):
        if self.type == "soul":
            if self.isThrown:
                max = 0
                low = 0
                for player in playerList:
                    pos = self.pos.y - player.pos.y
                    if pos > 50 or pos < -50:
                        if pos > max: max = pos
                        if pos < low: low = pos

                if 0 - low > max:
                    if self.speed.y < 5:
                        self.speed.y += 2
                else:
                    if self.speed.y > 5:
                        self.speed.y -= 2


class ParticleSystem:
    def __init__(self, pos, speed, gravity, spread, col, size, lifetime, spawnrate):
        self.maxnum = 10000000000
        self.particleList = []
        self.lifetime = lifetime
        self.spawnrate = spawnrate
        self.currentSpawn = 0

        self.pos = pymath.Vector2(pos)
        self.speed = pymath.Vector2(speed)
        self.gravity = gravity
        self.spread = pymath.Vector2(spread)
        self.col = list(col)
        self.size = size

    def tick(self, pos):
        self.pos = pos

        self.randomNum = random.randrange(0, 100)
        self.randomNum = self.randomNum / 100

        if len(self.particleList) < self.maxnum:
            self.currentSpawn += 1
            if self.currentSpawn >= self.spawnrate:
                self.currentSpawn = 0

                spread = self.randomNum * self.spread
                spread = spread[0]
                tempspeedx = self.speed.x + spread - self.spread[0] / 2

                particle = Particle(self.pos, (tempspeedx, self.speed.y), self.gravity, self.col, self.size)
                self.particleList.append(particle)

        for particle in self.particleList:
            if particle.lifetime >= self.lifetime:
                self.particleList.remove(particle)

            particle.tick()

class Particle:
    def __init__(self, pos, speed, gravity, col, size):
        self.pos = pymath.Vector2(pos)
        self.speed = pymath.Vector2(speed)
        self.gravity = gravity
        self.col = col
        self.size = size
        self.lifetime = 0
        
        self.rect = pg.Rect(self.pos.x, self.pos.y, self.size, self.size)

    def tick(self):
        self.speed.y += self.gravity
        self.pos += self.speed
        self.rect.center = (self.pos.x, self.pos.y)
        pydraw.rect(screen, self.col, self.rect)
        self.lifetime += 1

pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()

window = pg.display.Info()
print(window.current_w, window.current_h)

SCREEN_WIDTH = 1536
SCREEN_HEIGHT = 864
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
game_font = pg.font.Font(None, 25)
isRunning = True
FPS = 60
isMuted = True
isFullscreen = True
pg.display.toggle_fullscreen() 

def load_music():
    x = random.randint(1, 3)
    y = r'src\assets\lyd\Music\Juhani Junkala [Retro Game Music Pack] Level ' + str(x) + '.wav'
    pg.mixer.music.load(y)

load_music()

blockList = []
ballList = []
playerList = []

player = Player((60, 60), (50, 50), char="bald")
playerList.append(player)

dummy = Player((60, 60), (500, 50), char="dummy")
playerList.append(dummy)

block = Block((170, 600), (200, 30))
blockList.append(block)

block = Block((0, SCREEN_HEIGHT - 20), (SCREEN_WIDTH, 100))
blockList.append(block)

test = Ball((50, 50), type="ice")
ballList.append(test)

particlesystem = ParticleSystem((500, 500), (10, -10), 1, 5, (255, 255, 255), 10, 50, 1)

while isRunning == True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                quit()
            if event.key == pg.K_F11:
                if isFullscreen:
                    isFullscreen = False
                    SCREEN_WIDTH = 1920
                    SCREEN_HEIGHT = 1080
                else:
                    isFullscreen = True
                    SCREEN_WIDTH = window.current_w
                    SCREEN_HEIGHT = window.current_h
                pg.display.toggle_fullscreen() 

            if event.key == pg.K_m:
                if isMuted:
                    isMuted = False
                    pg.mixer.music.play(loops=-1)
                else:
                    isMuted = True
                    pg.mixer.music.stop()

            if event.key == pg.K_e:
                for player in playerList:
                    if player.char != "dummy":
                        player.pickup()

    screen.fill((0, 0, 0))

    for block in blockList:
        block.tick()

    for player in playerList:
        player.tick()
    
    for ball in ballList:
        ball.tick()

    particlesystem.tick((500, 500))

    pg.display.update()
    clock.tick(FPS)

quit()
