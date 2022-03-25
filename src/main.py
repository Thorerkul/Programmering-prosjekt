import sys, random, math
import pygame as pg
import pygame.math as pymath
import pygame.draw as pydraw

def quit():
    pg.quit()
    sys.exit()

def startGame(map):
    global player, floor, test, bgimg, bgrect
    if map == "empty":
        bgimg = pg.image.load(r'src\assets\art\bg\space.png').convert_alpha()
        bgimg = pg.transform.scale(bgimg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bgrect = pg.Rect(0, 0, window.current_w, window.current_h)

        player = Player((60, 60), (50, 50))
        playerList.append(player)

        floor = Block((0, SCREEN_HEIGHT - 20), (SCREEN_WIDTH, 100), False)

        test = Ball((50, 50), type="ice")
        ballList.append(test)

    if map == "editor":
        global editor, isInEditor
        bgimg = pg.image.load(r'src\assets\art\bg\black.png').convert_alpha()
        bgimg = pg.transform.scale(bgimg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bgrect = pg.Rect(0, 0, window.current_w, window.current_h)

        player = Player((60, 60), (50, 50))
        playerList.append(player)

        floor = Block((0, SCREEN_HEIGHT - 20), (SCREEN_WIDTH, 100), False)

        test = Ball((50, 50), type="ice")
        ballList.append(test)

        isInEditor = True
        editor = EditorHandler()

    if map == "default":
        global dummy, block, particlesystem

        bgimg = pg.image.load(r'src\assets\art\bg\hell.png').convert_alpha()
        bgimg = pg.transform.scale(bgimg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bgrect = pg.Rect(0, 0, window.current_w, window.current_h)

        player = Player((60, 60), (50, 50))
        playerList.append(player)

        dummy = Player((60, 60), (500, 50), char="dummy")
        playerList.append(dummy)

        block = Block((170, 700), (200, 30), True, isX=False)
        blockList.append(block)

        floor = Block((0, SCREEN_HEIGHT - 20), (SCREEN_WIDTH, 100), False)

        test = Ball((50, 50), type="ice")
        ballList.append(test)

        particlesystem = ParticleSystem((500, 500), (10, -10), 1, 5, (255, 255, 255), 10, 50, 1)

class Player:
    def __init__(self, size, pos, char="billy"):
        self.pos = pymath.Vector2(pos)
        self.size = pymath.Vector2(size)
        self.speed = pymath.Vector2(0, 0)
        self.max_speed = 6
        self.canJump = False
        self.prev_keys = []
        self.char = char
        self.lastMoveDir = pymath.Vector2(0, 0)
        self.hasBall = False
        self.prev_hasBall = False
        self.isOnGround = False
        self.isGoingUp = False
        self.weight = 0.5
        self.defaultWeight = 0.5
        self.maxhp = 100
        self.hp = self.maxhp

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

        if self.char == "bald":
            path = 'src\\assets\\art\\karakterer\\BaldGuy\\baldguy'
            for i in range(30):
                if i >= 9:
                    file = path + '00' + str(i + 1) + '.png'
                else:
                    file = path + '000' + str(i + 1) + '.png'

                if i == 19:
                    file = 'src\\assets\\art\\karakterer\\BaldGuy\\baldguy0030.png'

                print(file)
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
        self.ballAction()
        self.HpHandler()

        self.pos.x += self.speed.x
        self.pos.y += self.speed.y

        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

        screen.blit(self.animation(), self.rect)
        self.canJump = False
        self.prev_hasBall = self.hasBall

    def movementHandler(self):
        if self.char == "billy":
            keys = pg.key.get_pressed()
            if keys[pg.K_a]:
                self.speed.x = 0 - self.max_speed
                self.lastMoveDir.x = -1
            else:
                self.speed.x /= 1.9
            if keys[pg.K_d]:
                self.speed.x = self.max_speed
                self.lastMoveDir.x = 1
                
            if keys[pg.K_SPACE] and self.canJump:
                self.speed.y = 0 - self.max_speed * 2.2
                if isMuted == False: self.jumpsfx.play()
            
            self.prev_keys = pg.key.get_pressed()
            
        if self.char == "dummy":
            self.speed.x /= 2

    def checkCollisions(self):
        for block in blockList:
            if self.rect.colliderect(block):
                if self.rect.centery <= block.rect.centery:
                    self.speed.y = -0.25
                    self.canJump = True
                    if block.isMoving:
                        if block.isX:
                            if block.slide == False:
                                if block.isGoingRight:
                                    self.pos.x += 2
                                else:
                                    self.pos.x -= 2
                        else:
                            if block.isGoingRight == False:
                                self.pos.y -= 2
                else:
                    self.speed.y = 2
                    
        if self.rect.colliderect(floor):
            self.speed.y = -0.25
            self.canJump = True

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
            self.speed.y += self.weight

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
            if self.speed.x <= 0.1 and self.speed.x >= -0.1:
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

    def ballAction(self):
        self.weight = self.defaultWeight
        if self.ballType == "obsidian" and self.hasBall:
            self.weight = 2
        if self.ballType == "steel" and self.hasBall:
            self.weight = 1.25

    def HpHandler(self):
        for ball in ballList:
            if ball.lifetime >= 3:
                if self.rect.colliderect(ball):
                    if ball.isThrown:
                        if ball.type == "steel":
                            self.speed.x = ball.speed.x / 2
                            self.hp -= 5
                        elif ball.type == "obsidian":
                            self.speed.x = ball.speed.x / 1.1
                            self.hp -= 0.5
                        else:
                            self.hp -= 1

        text = str(int(self.hp)) + " / " + str(self.maxhp)
        surf = game_font.render(text, True, (255, 255, 255))
        rect = surf.get_rect(center = (self.pos.x, self.pos.y - 50))
        screen.blit(surf, rect)

class Block:
    def __init__(self, pos, size, isMoving, isX=True, slide=False):
        self.pos = pymath.Vector2(pos)
        self.size = pymath.Vector2(size)
        self.col = pymath.Vector3(128, 128, 128) # temp color
        self.isMoving = isMoving
        if self.isMoving:
            self.isX = isX
            self.slide = slide
            self.isGoingRight = True
        
        self.rect = pg.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def tick(self):
        if self.isMoving:
            if self.isX:
                if self.rect.right >= SCREEN_WIDTH:
                    self.isGoingRight = False
                if self.rect.left <= 0:
                    self.isGoingRight = True
                if self.isGoingRight: self.pos.x += 1
                else: self.pos.x -= 1
            else:
                if self.rect.bottom >= SCREEN_HEIGHT:
                    self.isGoingRight = False
                if self.rect.top <= 0:
                    self.isGoingRight = True
                if self.isGoingRight: self.pos.y += 1
                else: self.pos.y -= 1

        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

        pydraw.rect(screen, self.col, self.rect)

class Ball:
    def __init__(self, pos, type="basic", speed=(0, 0)):
        self.pos = pymath.Vector2(pos)
        self.col = pymath.Vector3(255, 0, 0)
        self.size = 10
        self.speed = pymath.Vector2(speed)
        self.type = type
        self.weight = 0.5
        self.lifetime = 0

        self.bounceSound = pg.mixer.Sound(r'src\assets\lyd\ballBounce.wav')

        if self.type == "basic":
            self.image = pg.image.load(r'src\assets\art\balls\Basic_ball.png').convert_alpha()
        elif self.type == "ice":
            self.image = pg.image.load(r'src\assets\art\balls\ice_ball.png').convert_alpha()
        elif self.type == "steel":
            self.image = pg.image.load(r'src\assets\art\balls\steel_ball.png').convert_alpha()
        elif self.type == "sun":
            self.image = pg.image.load(r'src\assets\art\balls\Sun_ball.png').convert_alpha()
        elif self.type == "nature":
            self.image = pg.image.load(r'src\assets\art\balls\nature_ball.png').convert_alpha()
        elif self.type == "magic":
            self.image = pg.image.load(r'src\assets\art\balls\magic_ball.png').convert_alpha()
        elif self.type == "soul":
            self.image = pg.image.load(r'src\assets\art\balls\soul_ball.png').convert_alpha()
        elif self.type == "obsidian":
            self.image = pg.image.load(r'src\assets\art\balls\obsidian_ball.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (self.size + 9, self.size + 9))
        
        self.boucesLeft = 3
        self.isThrown = True
        
        self.rect = pg.Rect(self.pos.x - self.size, self.pos.y - self.size, self.size * 2, self.size * 2)

        if self.type == "soul":
            self.particlesystem = ParticleSystem(self.pos, (0, 0), -0.005, 1, (128, 0, 255), 5, 500, 1)
        
    def tick(self):
        self.lifetime += 1
        self.specialUpdate()
        if self.speed.y < 15:
            self.speed.y += self.weight
        for block in blockList:
            if self.rect.colliderect(block):
                if self.rect.bottom <= block.rect.top + 20:
                    while self.rect.colliderect(block):
                        self.pos.y -= 0.1

                        self.rect.centerx = self.pos.x
                        self.rect.centery = self.pos.y

                    self.speed.y = 0 - self.speed.y / self.weight * 3 / 5
                    self.speed.x /= 1.1
                    if isMuted == False: self.bounceSound.play()
                    self.boucesLeft -= 1
                else:
                    while self.rect.colliderect(block):
                        self.pos.y += 0.1

                        self.rect.centerx = self.pos.x
                        self.rect.centery = self.pos.y
                    self.speed.y = 5
                    self.speed.x /= 1.1
                    if isMuted == False: self.bounceSound.play()
                    self.boucesLeft -= 1
                    
        if self.rect.colliderect(floor):
            while self.rect.colliderect(floor):
                self.pos.y -= 0.5
                self.rect.centery -= 0.5
            self.speed.x /= 1.1
            self.speed.y = 0 - self.speed.y / 1.3
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

        if self.type == "obsidian":
            self.weight = 2

        if self.type == "steel":
            self.weight = 1.25


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

class EditorHandler:
    def __init__(self):
        self.mouse = pymath.Vector2(pg.mouse.get_pos())
        self.mousepress = pg.mouse.get_pressed(3)
        self.prevMousepress = self.mousepress
        self.hasClicked = [False, False, False]
        self.clickpos = [pymath.Vector2(0, 0), pymath.Vector2(0, 0)]

    def tick(self):
        global blockList
        self.mouse = pymath.Vector2(pg.mouse.get_pos())
        self.mousepress = [pg.mouse.get_pressed(3)]
        self.mousepress = self.mousepress[0]

        if self.mousepress[0] != self.prevMousepress[0] and self.mousepress[0] == True:
            if self.hasClicked[0]:
                self.hasClicked[0] = False
                self.clickpos[1] = pymath.Vector2(self.mouse.x, self.mouse.y)

                print("yes")
                block = Block(self.clickpos[0], (self.clickpos[0].x - self.clickpos[1].x, self.clickpos[0].y - self.clickpos[1].y), False)
                blockList.append(block)
                print("yes 2")
            else:
                self.hasClicked[0] = True
                self.clickpos[0] = pymath.Vector2(self.mouse.x, self.mouse.y)

        print(self.mouse, self.mousepress[0], self.prevMousepress[0], self.hasClicked[0], self.clickpos, blockList)
        self.prevMousepress = self.mousepress

pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()

window = pg.display.Info()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 512
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
game_font = pg.font.Font(None, 25)
isRunning = True
FPS = 60
isMuted = True
isFullscreen = True
isInEditor = False
pg.mixer.music.set_volume(0.1)
#pg.display.toggle_fullscreen() 

def load_music():
    x = random.randint(1, 3)
    y = r'src\assets\lyd\Music\Juhani Junkala [Retro Game Music Pack] Level ' + str(x) + '.wav'
    pg.mixer.music.load(y)

load_music()

blockList = []
ballList = []
playerList = []

startGame("editor")

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
    screen.blit(bgimg, bgrect)

    for player in playerList:
        player.tick()
    
    for ball in ballList:
        ball.tick()

    if isInEditor:
        editor.tick()

    for block in blockList:
        block.tick()
        print(block.col)

    pg.display.update()
    clock.tick(FPS)

quit()
