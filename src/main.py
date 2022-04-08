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
        bgimg = pg.image.load(r'assets\art\bg\space.png').convert_alpha()
        bgimg = pg.transform.scale(bgimg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bgrect = pg.Rect(0, 0, window.current_w, window.current_h)

        player = Player((60, 60), (50, 50))
        playerList.append(player)

        floor = Block((0, SCREEN_HEIGHT - 20), (SCREEN_WIDTH, 100))

        test = Ball((50, 50), type="ice")
        ballList.append(test)
        
        loadSaves()

    if map == "editor":
        #global isInEditor
        bgimg = pg.image.load(r'assets\art\bg\black.png').convert_alpha()
        bgimg = pg.transform.scale(bgimg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bgrect = pg.Rect(0, 0, window.current_w, window.current_h)

        player = Player((60, 60), (50, 50))
        playerList.append(player)

        floor = Block((0, SCREEN_HEIGHT - 20), (SCREEN_WIDTH, 100))

        test = Ball((50, 50), type="ice")
        ballList.append(test)

        #isInEditor = True
        editor = EditorHandler()
        
        loadSaves()

    if map == "default":
        global dummy, particlesystem, isInEditor

        bgimg = pg.image.load(r'assets\art\bg\hell.png').convert_alpha()
        bgimg = pg.transform.scale(bgimg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bgrect = pg.Rect(0, 0, window.current_w, window.current_h)

        player = Player((60, 60), (50, 50))
        playerList.append(player)

        dummy = Player((60, 60), (500, 50), char="dummy")
        playerList.append(dummy)

        #block = Block((500, 400), (200, 30))
        #blockList.append(block)

        floor = Block((0, SCREEN_HEIGHT - 20), (SCREEN_WIDTH, 100))

        test = Ball((50, 50), type="ice")
        ballList.append(test)

        particlesystem = ParticleSystem((500, 500), (10, -10), 1, 5, (255, 255, 255), 10, 50, 1)
        isInEditor = True
        
        loadSaves()

def loadSaves():
    global levelr, levela, blockList
    levela = open('assets\saves\saves.txt', 'a')
    levelr = open('assets\saves\saves.txt', 'r')

    x = 0
    while True:
        content = levelr.readline()
        if content != '':
            temp = ''
            for char in content:
                if char == ')':
                    break
                temp = temp + char
            temp = temp.replace('(', '')
            temp = temp.split(', ')
            for i in range(len(temp)):
                temp[i] = float(temp[i])
                temp[i] = int(temp[i])
            block = Block((temp[0], temp[1]), (100, 20))
            blockList.append(block)
            #print(block.pos.y)
        else:
            break

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

        self.jumpsfx = pg.mixer.Sound(r'assets\lyd\jump.wav')
        self.pickupsfx = pg.mixer.Sound(r'assets\lyd\pickup.wav')
        self.throwsfx = pg.mixer.Sound(r'assets\lyd\throw.wav')

        self.rect = pg.Rect(self.pos.x, self.pos.y, self.size.x - 10, self.size.y - 10)
        self.col = pymath.Vector3(255, 255, 255) # temp color

        self.loadSprites()
        self.current_frame = 0

    def loadSprites(self):
        self.runningsprites = []
        self.holdingsprites = []

        if self.char == "billy" or self.char == "dummy":
            path = 'assets\\art\\karakterer\\Billy\\billy00'
            for i in range(30):
                if i >= 9:
                    file = path + str(i + 1) + '.png'
                else:
                    file = path + '0' + str(i + 1) + '.png'

                self.runningsprites.append(pg.image.load(file).convert_alpha())

            for i in range(30):
                file = path + str(i + 32) + '.png'

                self.holdingsprites.append(pg.image.load(file).convert_alpha())

            self.standingSprite = pg.image.load(r'assets\art\karakterer\Billy\billy0007.png').convert_alpha()
            self.airSprite = pg.image.load(r'assets\art\karakterer\Billy\billy0055.png').convert_alpha()

        if self.char == "bald":
            path = 'assets\\art\\karakterer\\BaldGuy\\baldguy'
            for i in range(30):
                if i >= 9:
                    file = path + '00' + str(i + 1) + '.png'
                else:
                    file = path + '000' + str(i + 1) + '.png'

                if i == 19:
                    file = 'assets\\art\\karakterer\\BaldGuy\\baldguy0030.png'

                print(file)
                self.runningsprites.append(pg.image.load(file).convert_alpha())

            for i in range(30):
                file = path + str(i + 32) + '.png'

                self.holdingsprites.append(pg.image.load(file).convert_alpha())

            self.standingSprite = pg.image.load(r'assets\art\karakterer\BaldGuy\baldguy0007.png').convert_alpha()
            self.airSprite = pg.image.load(r'assets\art\karakterer\BaldGuy\baldguy0055.png').convert_alpha()

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

            if self.ballType != "magic":
                ball = Ball((self.pos.x, self.pos.y), speed=dir, type=self.ballType)
            else:
                ball = Ball((self.pos.x, self.pos.y), speed=(dir[0]/10, dir[1]/10), type=self.ballType)
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
    def __init__(self, pos, size):
        self.pos = pymath.Vector2(pos)
        self.size = pymath.Vector2(size)
        self.col = pymath.Vector3(128, 128, 128) # temp color
        
        self.rect = pg.Rect(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def tick(self):
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

        self.bounceSound = pg.mixer.Sound(r'assets\lyd\ballBounce.wav')

        if self.type == "basic":
            self.image = pg.image.load(r'assets\art\balls\Basic_ball.png').convert_alpha()
        elif self.type == "ice":
            self.image = pg.image.load(r'assets\art\balls\ice_ball.png').convert_alpha()
        elif self.type == "steel":
            self.image = pg.image.load(r'assets\art\balls\steel_ball.png').convert_alpha()
        elif self.type == "sun":
            self.image = pg.image.load(r'assets\art\balls\Sun_ball.png').convert_alpha()
        elif self.type == "nature":
            self.image = pg.image.load(r'assets\art\balls\nature_ball.png').convert_alpha()
        elif self.type == "magic":
            self.image = pg.image.load(r'assets\art\balls\magic_ball.png').convert_alpha()
        elif self.type == "soul":
            self.image = pg.image.load(r'assets\art\balls\soul_ball.png').convert_alpha()
        elif self.type == "obsidian":
            self.image = pg.image.load(r'assets\art\balls\obsidian_ball.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (self.size + 9, self.size + 9))
        
        self.boucesLeft = 3
        self.isThrown = True
        
        self.rect = pg.Rect(self.pos.x - self.size, self.pos.y - self.size, self.size * 2, self.size * 2)

        if self.type == "soul":
            self.particlesystem = ParticleSystem(self.pos, (0, 0), -0.005, 1, (128, 0, 255), 5, 500, 1)
        
    def tick(self):
        self.lifetime += 1
        self.specialUpdate()
        if self.type != "magic":
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

        if self.type == "magic":
            # force = G*mass1*mass2/distance**2
            # G = 6.67430(15)
            G = 6.67430*15
            m1 = 100.0
            m2 = 1000.0
            Fx = []
            Fy = []

<<<<<<< HEAD
            for i in enumerate(playerList):
                dx = self.pos.x - playerList[i].pos.x
                dy = self.pos.y - playerList[i].pos.y
=======
            for player in playerList:
                Fx = 0
                Fy = 0
                dx = 0
                dy = 0
                
                dx = self.pos.x - player.pos.x
                dy = self.pos.y - player.pos.y

                dx = math.sqrt(dx**2)
                dx = math.sqrt(dx**2)
                
>>>>>>> d3f1f16 (Update main.py)
                if dx == 0:
                    dx = 0.00001
                if dy == 0:
                    dy = 0.00001
                Fx.append(G*(m1*m2)/dx**2)
                Fy.append(G*(m1*m2)/dy**2)
                Fx[i] = 1 / Fx
                Fy[i] = 1 / Fy

                if self.pos.x > playerList[i].pos.x:
                    if Fx < 0:
                        Fx = 0 - Fx
                if self.pos.x < playerList[i].pos.x:
                    if Fx > 0:
                        Fx = 0 - Fx

                if self.pos.y < playerList[i].pos.y:
                    if Fy < 0:
                        Fy = 0 - Fy
                if self.pos.y > playerList[i].pos.y:
                    if Fy > 0:
                        Fy = 0 - Fy

<<<<<<< HEAD
            self.speed.x -= Fx * 10
            self.speed.y += Fy * 10
=======
                if player.char == "dummy":

                    self.speed.x -= Fx * 100
                    self.speed.y += Fy * 100
        
>>>>>>> d3f1f16 (Update main.py)

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

# work on later
class EditorHandler:
    def __init__(self):
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse = pg.mouse.get_pressed(3)
        self.mouse = self.mouse[0]
<<<<<<< HEAD
        self.mouse_pos = pg.mouse.get_pos()
=======
        self.mouse = int(self.mouse)
>>>>>>> 54d946d (fghjk)
        self.prev_mouse = self.mouse

    def tick(self):
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse = pg.mouse.get_pressed(3)
        self.mouse = self.mouse[0]
<<<<<<< HEAD
        self.mouse_pos = pg.mouse.get_pos()
        if self.mouse != self.prev_mouse and self.mouse == True:
            block = Block((self.mouse_pos[0], self.mouse_pos[1]), (100, 20))
            block.rect.centerx = self.mouse_pos[0]
            block.rect.centery = self.mouse_pos[1]
            blockList.append(block)
            x = str(self.mouse_pos)
            levela.write(x)
            levela.write('\n')
            
        tempblock = Block((self.mouse_pos[0], self.mouse_pos[1]), (100, 20))
        tempblock.rect.centerx = self.mouse_pos[0]
        tempblock.rect.centery = self.mouse_pos[1]
        pydraw.rect(screen, (0, 0, 0), tempblock)
            
=======
        self.mouse = int(self.mouse)

        rect = pg.Rect(self.mouse_pos[0], self.mouse_pos[1], 100, 20)
        rect.center = (self.mouse_pos[0], self.mouse_pos[1])
        pydraw.rect(screen, (0, 0, 0), rect)

        if self.mouse != self.prev_mouse and self.mouse == True:
            block = Block((self.mouse_pos[0], self.mouse_pos[1]), (100, 20))
            blockList.append(block)
            x = block.pos
            levela.write(str(x))
            levela.write('\n')
>>>>>>> 54d946d (fghjk)
        self.prev_mouse = self.mouse
        """block = Block((self.clickpos[0].x, self.clickpos[0].y), (self.mouse[0] - self.clickpos[0].x, self.mouse[1] - self.clickpos[0].x))
                blockList.append(block)
                x = str([block.pos.x, block.pos.y, block.size.x, block.size.y])
                self.currentSave.append(x)
                levela.write(x)
                levela.write('\n')"""

class HUD:
    def __init__(self):
        self.hotbar_pos = pymath.Vector2(SCREEN_WIDTH / 2, 0)
        self.hotbar_num_items = 8
        self.hotbar_size = 19
        self.red_icon = pg.image.load(r'src\assets\art\balls\Basic_ball.png').convert_alpha()
        self.ice_icon = pg.image.load(r'src\assets\art\balls\ice_icon.png').convert_alpha()
        self.steel_icon = pg.image.load(r'src\assets\art\balls\steel_icon.png').convert_alpha()
        self.sun_icon = pg.image.load(r'src\assets\art\balls\sun_icon.png').convert_alpha()
        self.nature_icon = pg.image.load(r'src\assets\art\balls\nature_icon.png').convert_alpha()
        self.magic_icon = pg.image.load(r'src\assets\art\balls\magic_icon.png').convert_alpha()
        self.soul_icon = pg.image.load(r'src\assets\art\balls\soul_icon.png').convert_alpha()
        self.obsidian_icon = pg.image.load(r'src\assets\art\balls\obsidian_icon.png').convert_alpha()
        self.hotbar_bg = pg.image.load(r'src\assets\art\balls\bg.png').convert_alpha()

        self.hotbarList = []
        for i in range(self.hotbar_num_items):
            posx = 0
            print(posx)
            rect = pg.Rect(posx, 0, self.hotbar_size, self.hotbar_size)
            rect.top = 0
            self.hotbarList.append(rect)

    def tick(self):
        for i in self.hotbarList:
            pydraw.rect(screen, (100, 100, 100), i)

pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()

window = pg.display.Info()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 512
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
game_font = pg.font.Font(None, 25)
pause_font = pg.font.Font(None, 60)
isRunning = True
FPS = 60
isMuted = True
isFullscreen = True
isInEditor = False
isPaused = False
pg.mixer.music.set_volume(0.1)
#pg.display.toggle_fullscreen() 

def load_music():
    x = random.randint(1, 3)
    y = r'assets\lyd\Music\Juhani Junkala [Retro Game Music Pack] Level ' + str(x) + '.wav'
    pg.mixer.music.load(y)

load_music()

blockList = []
ballList = []
playerList = []

startGame("default")

if isInEditor:
    editor = EditorHandler()

<<<<<<< HEAD
=======
loadSaves()

hud = HUD()

>>>>>>> 0d7b8aa (h)
while isRunning == True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                if isPaused == True:
                    isPaused = False
                else:
                    isPaused = True
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

    if isPaused == False:
        screen.fill((0, 0, 0))
        screen.blit(bgimg, bgrect)
        
        for block in blockList:
            block.tick()

        for player in playerList:
            player.tick()
    
        for ball in ballList:
            ball.tick()

        if isInEditor:
            editor.tick()

    else:
        text = "Paused"
        surf = pause_font.render(text, False, (255, 255, 255))
        rect = surf.get_rect()
        rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        pydraw.rect(screen, (0, 0, 0), rect)
        screen.blit(surf, rect)

    hud.tick()

    pg.display.update()
    clock.tick(FPS)

quit()
