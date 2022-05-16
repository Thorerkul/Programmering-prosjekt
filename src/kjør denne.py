import sys, random, math, colorsys
import pygame as pg
import pygame.math as pymath
import pygame.draw as pydraw

def quit():
    pg.quit()
    sys.exit()

def startGame(map):
    global player, floor, test, bgimg, bgrect, isInMenu, level
    isInMenu = False
    pg.mixer.music.unload()
    load_music("match")
    pg.mixer.music.set_volume(0.3)
    #pg.mixer.music.play(loops=-1)
    
    if map == "empty":
        level = "empty"
        bgimg = pg.image.load(r'assets\art\bg\space.png').convert_alpha()
        bgimg = pg.transform.scale(bgimg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bgrect = pg.Rect(0, 0, window.current_w, window.current_h)

        player = Player((60, 60), (50, 50))
        playerList.append(player)

        floor = Block((0, SCREEN_HEIGHT - 20), (SCREEN_WIDTH, 100))

        test = Ball((50, 50), type="ice")
        ballList.append(test)

    if map == "editor":
        global editor, isInEditor
        level = "editor"
        bgimg = pg.image.load(r'assets\art\bg\black.png').convert_alpha()
        bgimg = pg.transform.scale(bgimg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bgrect = pg.Rect(0, 0, window.current_w, window.current_h)

        player = Player((60, 60), (50, 50))
        playerList.append(player)

        floor = Block((0, SCREEN_HEIGHT - 20), (SCREEN_WIDTH, 100))

        test = Ball((50, 50), type="ice")
        ballList.append(test)

        isInEditor = True
        editor = EditorHandler()
        #ai = Ai((60, 60), (90, 50))
        #aiList.append(ai)

    if map == "default":
        global dummy, particlesystem, aiList
        level = "default"

        bgimg = pg.image.load(r'assets\art\bg\space.png').convert_alpha()
        bgimg = pg.transform.scale(bgimg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bgrect = pg.Rect(0, 0, window.current_w, window.current_h)

        player = Player((60, 60), (50, 50))
        playerList.append(player)

        #block = Block((500, 400), (200, 30))
        #blockList.append(block)

        floor = Block((0, SCREEN_HEIGHT - 20), (SCREEN_WIDTH, 100))

        test = Ball((50, 50), type="ice")
        ballList.append(test)

        particlesystem = ParticleSystem((500, 500), (10, -10), 1, 5, (255, 255, 255), 10, 50, 1)

        ai = Ai((60, 60), (90, 50))
        aiList.append(ai)
        
        block = Block((random.randrange(50, 900), 400), (random.randint(1, 8) * 50, 20))
        blockList.append(block)
        block = Block((random.randrange(50, 900), 300), (random.randint(1, 8) * 50, 20))
        blockList.append(block)
        block = Block((random.randrange(50, 900), 200), (random.randint(1, 8) * 50, 20))
        blockList.append(block)
        
    if map == "boss":
        level = "boss"

        bgimg = pg.image.load(r'assets\art\maps\pixil-frame-0 (4).png').convert_alpha()
        bgimg = pg.transform.scale(bgimg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bgrect = pg.Rect(0, 0, window.current_w, window.current_h)

        player = Player((60, 60), (50, 50))
        playerList.append(player)

        #block = Block((500, 400), (200, 30))
        #blockList.append(block)

        floor = Block((0, SCREEN_HEIGHT - 20), (SCREEN_WIDTH, 100))

        test = Ball((50, 50), type="ice")
        ballList.append(test)

        ai = Ai((120, 120), (90, 50), type="aggresive")
        aiList.append(ai)
        
    if map == "level1":
        level = "level1"
        bgimg = pg.image.load(r'assets\art\bg\black.png').convert_alpha()
        bgimg = pg.transform.scale(bgimg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bgrect = pg.Rect(0, 0, window.current_w, window.current_h)

        player = Player((60, 60), (50, 50))
        playerList.append(player)

        floor = Block((0, SCREEN_HEIGHT - 20), (SCREEN_WIDTH, 100))

        test = Ball((50, 50), type="ice")
        ballList.append(test)

        isInEditor = True
        editor = EditorHandler()
        #ai = Ai((60, 60), (90, 50))
        #aiList.append(ai)

def loadSaves(dir='saves'):
    global levelr, levela, blockList
    dir = 'assets\saves\\level1.txt'
    levela = open(dir, 'a')
    levelr = open(dir, 'r')

    x = 0
    while True:
        content = levelr.readline()
        if content != '':
            temp = ''
            for char in content:
                if char == ']':
                    break
                temp = temp + char
            temp = temp.replace('[', '')
            temp = temp.split(', ')
            for i in range(len(temp)):  
                temp[i] = float(temp[i])
                temp[i] = int(temp[i])
            block = Block((temp[0], temp[1]), (temp[2], 20))
            blockList.append(block)
        else:
            break

def get_closest_value(input_list, input_value):
 
  difference = lambda input_list : abs(input_list - input_value)
 
  res = min(input_list, key=difference)
 
  return res

def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))

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

        self.statusEffect = ""
        self.hasStatus = False
        self.prevHasStatus = False
        self.statusTimer = 0
        self.particleSystem = ParticleSystem(self.pos, (0, -15), 1, 10, (255, 215, 0), 10, 10, 1)

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
            self.frozenSprite = pg.image.load(r'assets\art\karakterer\Billy\billyFrozen.png').convert_alpha()
            self.stuckSprite = pg.image.load(r'assets\art\karakterer\Billy\billyStuck.png').convert_alpha()

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
        self.frozenSprite = pg.transform.scale(self.frozenSprite, (int(self.size.x), int(self.size.y)))
        self.stuckSprite = pg.transform.scale(self.stuckSprite, (int(self.size.x), int(self.size.y)))

    def tick(self):
        self.gravity()
        self.checkCollisions()
        self.movementHandler()
        if level == "default" or level == "editor":
            self.selectBall()
        self.ballAction()
        self.HpHandler()
        self.statusHandler()

        self.pos.x += self.speed.x
        self.pos.y += self.speed.y

        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

        screen.blit(self.animation(), self.rect)
        self.canJump = False
        self.prev_hasBall = self.hasBall
        self.prevHasStatus = self.hasStatus

    def movementHandler(self):
        if self.char == "billy":
            keys = pg.key.get_pressed()
            #print(self.statusEffect)
            if self.statusEffect == "frozen":
                self.speed.x /= 1.01
            elif self.statusEffect == "stuck":
                self.speed.x /= 1.9
            else:
                if keys[pg.K_a]:
                    self.speed.x = 0 - self.max_speed
                    self.lastMoveDir.x = -1
                else:
                    self.speed.x /= 1.9
                if keys[pg.K_d]:
                    self.speed.x = self.max_speed
                    self.lastMoveDir.x = 1
                
            if keys[pg.K_SPACE] and self.canJump:
                if self.statusEffect != "stuck":
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
            #print(dir)

            if self.ballType != "magic":
                ball = Ball((self.pos.x, self.pos.y), speed=dir, type=self.ballType)
            else:
                ball = Ball((self.pos.x, self.pos.y), speed=(dir[0]/100, dir[1]/100), type=self.ballType)
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

        if self.hasStatus and self.statusEffect == "frozen":
            img = self.frozenSprite

        if self.hasStatus and self.statusEffect == "stuck":
            img = self.stuckSprite

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
        if self.hp <= 0:
            self.die()
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
                        elif ball.type == "sun":
                            self.statusEffect = "fire"
                            self.hasStatus = True
                            self.hp -= 1
                        elif ball.type == "ice":
                            self.statusEffect = "frozen"
                            self.hasStatus = True
                            self.hp -= 1
                        elif ball.type == "nature":
                            self.statusEffect = "stuck"
                            self.hasStatus = True
                            self.hp -= 1
                        else:
                            self.hp -= 1

        text = str(int(self.hp)) + " / " + str(self.maxhp)
        surf = game_font.render(text, True, (255, 255, 255))
        rect = surf.get_rect(center = (self.pos.x, self.pos.y - 50))
        screen.blit(surf, rect)

    def statusHandler(self):
        if self.hasStatus:
            self.statusTimer += 1
            if self.statusTimer >= 2 * FPS:
                self.statusTimer = 0
                self.hasStatus = False
                self.statusEffect = ""

            if self.statusEffect == "fire":
                self.hp -= 0.1
                self.particleSystem.tick(self.pos)

    def die(self):
        global player, playerList
        for player in playerList:
            if player == self:
                playerList.remove(player)
                del player
                player = Player((60, 60), (50, 50), char=self.char)
                playerList.append(player)
                break

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

        for player in aiList:
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
                for player in combinedList:
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

            for i, val in enumerate(combinedList):
                dx = self.pos.x - val.pos.x
                dy = self.pos.y - val.pos.y
                if dx == 0:
                    dx = 0.00001
                if dy == 0:
                    dy = 0.00001
                Fx.append(G*(m1*m2)/dx**2)
                Fy.append(G*(m1*m2)/dy**2)
                Fx[i] = 1 / Fx[i]
                Fy[i] = 1 / Fy[i]

                if self.pos.x > val.pos.x:
                    if Fx[i] < 0:
                        Fx[i] = 0 - Fx[i]
                if self.pos.x < val.pos.x:
                    if Fx[i] > 0:
                        Fx[i] = 0 - Fx[i]

                if self.pos.y < val.pos.y:
                    if Fy[i] < 0:
                        Fy[i] = 0 - Fy[i]
                if self.pos.y > val.pos.y:
                    if Fy[i] > 0:
                        Fy[i] = 0 - Fy[i]

            for i, val in enumerate(Fx):
                self.speed.x -= val * 10
            for i, val in enumerate(Fy):
                self.speed.y += val * 10

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
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse = pg.mouse.get_pressed(3)
        self.mouse = self.mouse[0]
        self.mouse = int(self.mouse)
        self.prev_mouse = self.mouse
        self.length = 100

    def tick(self):
        self.mouse_pos = pg.mouse.get_pos()
        self.mouse = pg.mouse.get_pressed(3)
        self.mouse = self.mouse[0]
        self.mouse = int(self.mouse)

        rect = pg.Rect(self.mouse_pos[0], self.mouse_pos[1], self.length, 20)
        rect.center = (self.mouse_pos[0], self.mouse_pos[1])
        pydraw.rect(screen, (0, 0, 0), rect)

        if self.mouse != self.prev_mouse and self.mouse == True:
            block = Block((self.mouse_pos[0], self.mouse_pos[1]), (self.length, 20))
            blockList.append(block)
            x = [int(block.pos.x), int(block.pos.y), self.length]
            levela.write(str(x))
            levela.write('\n')
        self.prev_mouse = self.mouse

    def setLength(self, length):
        self.length += length
        if self.length < 50:
            self.length = 50
        if self.length > 400:
            self.length = 400

class HUD:
    def __init__(self):
        self.hotbar_pos = pymath.Vector2(SCREEN_WIDTH / 2, 0)
        self.hotbar_num_items = 8
        self.hotbar_size = 40
        self.iconList = []
        self.red_icon = pg.image.load(r'assets\art\balls\Basic_ball.png').convert_alpha()
        self.iconList.append(self.red_icon)
        self.ice_icon = pg.image.load(r'assets\art\balls\ice_icon.png').convert_alpha()
        self.iconList.append(self.ice_icon)
        self.steel_icon = pg.image.load(r'assets\art\balls\steel_icon.png').convert_alpha()
        self.iconList.append(self.steel_icon)
        self.sun_icon = pg.image.load(r'assets\art\balls\sun_icon.png').convert_alpha()
        self.iconList.append(self.sun_icon)
        self.nature_icon = pg.image.load(r'assets\art\balls\nature_icon.png').convert_alpha()
        self.iconList.append(self.nature_icon)
        self.magic_icon = pg.image.load(r'assets\art\balls\magic_icon.png').convert_alpha()
        self.iconList.append(self.magic_icon)
        self.soul_icon = pg.image.load(r'assets\art\balls\soul_icon.png').convert_alpha()
        self.iconList.append(self.soul_icon)
        self.obsidian_icon = pg.image.load(r'assets\art\balls\obsidian_icon.png').convert_alpha()
        self.iconList.append(self.obsidian_icon)
        self.hotbar_bg = pg.image.load(r'assets\art\balls\bg.png').convert_alpha()
        self.hotbar_bg = pg.transform.scale(self.hotbar_bg, (self.hotbar_size, self.hotbar_size))

        for i, val in enumerate(self.iconList):
            self.iconList[i] = pg.transform.scale(self.iconList[i], (self.hotbar_size - 10, self.hotbar_size - 10))


        self.select_arrow = pg.image.load(r'assets\art\diverse\select arrow.png').convert_alpha()
        self.select_arrow = pg.transform.scale(self.select_arrow, (20, 20))
        self.selectRect = pg.Rect(-100, 50, 20, 20)

        self.hotbarList = []
        for i in range(self.hotbar_num_items):
            y = i - self.hotbar_num_items / 2
            z = self.hotbar_size + 3 * self.hotbar_num_items

            x = y * self.hotbar_size

            posx = x + SCREEN_WIDTH / 2
            posx = posx + y * 5
            rect = pg.Rect(posx, 0, self.hotbar_size, self.hotbar_size)
            rect.centery = self.hotbar_size / 2
            rect.centerx = posx
            self.hotbarList.append(rect)

    def tick(self):
        for i, val in enumerate(self.hotbarList):
            screen.blit(self.hotbar_bg, val)
            screen.blit(self.iconList[i], pg.Rect(val.left + 5, val.top + 5, self.hotbar_size - 10, self.hotbar_size - 10))

        for player in playerList:
            if player.ballType == "basic":
                self.selectRect.centerx = self.hotbarList[0].centerx
            if player.ballType == "ice":
                self.selectRect.centerx = self.hotbarList[1].centerx
            if player.ballType == "steel":
                self.selectRect.centerx = self.hotbarList[2].centerx
            if player.ballType == "sun":
                self.selectRect.centerx = self.hotbarList[3].centerx
            if player.ballType == "nature":
                self.selectRect.centerx = self.hotbarList[4].centerx
            if player.ballType == "magic":
                self.selectRect.centerx = self.hotbarList[5].centerx
            if player.ballType == "soul":
                self.selectRect.centerx = self.hotbarList[6].centerx
            if player.ballType == "obsidian":
                self.selectRect.centerx = self.hotbarList[7].centerx
        screen.blit(self.select_arrow, self.selectRect)

class Ai:
    def __init__(self, size, pos, char="billy", type="norm"):
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
        
        self.statusEffect = ""
        self.hasStatus = False
        self.prevHasStatus = False
        self.statusTimer = 0

        self.ballType = ""  

        self.jumpsfx = pg.mixer.Sound(r'assets\lyd\jump.wav')
        self.pickupsfx = pg.mixer.Sound(r'assets\lyd\pickup.wav')
        self.throwsfx = pg.mixer.Sound(r'assets\lyd\throw.wav')

        self.rect = pg.Rect(self.pos.x, self.pos.y, self.size.x - 10, self.size.y - 10)
        self.col = pymath.Vector3(255, 255, 255) # temp color

        self.loadSprites()
        self.current_frame = 0

        self.target = ""
        self.isGoingForTarget = True
        self.isGoingRight = False
        self.isMoving = False
        self.timer = 0
        self.timeTimer = 1
        self.timerRandom = random.randrange(0, 20) - 10
        if type == "norm":
            self.targetlist = ["", "left", "right", "jump", "ball", "ball", "away", "away"]
        if type == "aggressive":
            self.targetlist = ["", "left", "right", "jump", "ball", "ball", "away"]
        if type == "dumb":
            self.targetlist = ["", "left", "right", "jump", "left", "right", "jump", "ball", "ball", "away", "away"]
        if type == "scared":
            self.targetlist = ["", "left", "right", "jump", "ball", "away", "away"]

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
            self.frozenSprite = pg.image.load(r'assets\art\karakterer\Billy\billyFrozen.png').convert_alpha()
            self.stuckSprite = pg.image.load(r'assets\art\karakterer\Billy\billyStuck.png').convert_alpha()

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
            self.frozenSprite = pg.transform.scale(self.frozenSprite, (int(self.size.x), int(self.size.y)))

        # rescaling
        for i in range(len(self.runningsprites)):
            self.runningsprites[i] = pg.transform.scale(self.runningsprites[i], (int(self.size.x), int(self.size.y)))
        for i in range(len(self.holdingsprites)):
            self.holdingsprites[i] = pg.transform.scale(self.holdingsprites[i], (int(self.size.x), int(self.size.y)))
        self.standingSprite = pg.transform.scale(self.standingSprite, (int(self.size.x), int(self.size.y)))
        self.airSprite = pg.transform.scale(self.airSprite, (int(self.size.x), int(self.size.y)))
        self.frozenSprite = pg.transform.scale(self.frozenSprite, (int(self.size.x), int(self.size.y)))
        self.stuckSprite = pg.transform.scale(self.stuckSprite, (int(self.size.x), int(self.size.y)))

    def tick(self):
        self.gravity()
        self.checkCollisions()
        self.selectBall()
        self.ballAction()
        self.HpHandler()
        self.aiHandler()
        self.statusHandler()

        self.pos.x += self.speed.x
        self.pos.y += self.speed.y

        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y

        screen.blit(self.animation(), self.rect)
        self.canJump = False
        self.prev_hasBall = self.hasBall

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
        #print("y")
        if self.hasBall == False:
            for ball in ballList:
                if self.rect.colliderect(ball):
                    self.ballType = ball.type
                    self.hasBall = True
                    if isMuted == False: self.pickupsfx.play()
                    ballList.remove(ball)
                    del ball
        else:
            y = []
            x = []
            temp = 0
            for player in playerList:
                temp = self.pos.x - player.pos.x
                x.append(temp)

            temp = get_closest_value(x, 0)
            y.append(temp)

            x = []
            temp = 0
            for player in playerList:
                temp = self.pos.y - player.pos.y
                x.append(temp)

            temp = get_closest_value(x, 0)
            y.append(temp)

            y[0] = 0 - y[0]

            #print(y)
            mouse_pos = pymath.Vector2(y)
            dir = pymath.Vector2(mouse_pos.x - self.pos.x, mouse_pos.y - self.pos.y)
            dir = dir.normalize()

            dir = (dir[0] * 25, dir[1] * 10)
            
            dir = (0 - dir[0], 0 - dir[1])
            #print(dir)

            if self.ballType != "magic":
                ball = Ball((self.pos.x, self.pos.y), speed=dir, type=self.ballType)
            else:
                ball = Ball((self.pos.x, self.pos.y), speed=(dir[0]/100, dir[1]/100), type=self.ballType)
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

        if self.statusEffect == "frozen":
            img = self.frozenSprite

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
        if self.hp <= 0:
            self.die()
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
                        elif ball.type == "sun":
                            self.statusEffect = "fire"
                            self.hasStatus = True
                            self.hp -= 1
                        elif ball.type == "ice":
                            self.statusEffect = "frozen"
                            self.hasStatus = True
                            self.hp -= 1
                        elif ball.type == "nature":
                            self.statusEffect = "stuck"
                            self.hasStatus = True
                            self.hp -= 1
                        else:
                            self.hp -= 1

                        #print("ball")

        text = str(int(self.hp)) + " / " + str(self.maxhp)
        surf = game_font.render(text, True, (255, 100, 100))
        rect = surf.get_rect(center = (self.pos.x, self.pos.y - 50))
        screen.blit(surf, rect)

    def aiHandler(self):
        #print("hasBall: ", self.hasBall, " isGoingForTarget: ", self.isGoingForTarget, " target: ", self.target, " ballList: ", ballList)
        self.aiLoop()
        self.aiAction()

    def aiLoop(self):
        self.timer += 1
        if self.timer >= (self.timeTimer * FPS) + self.timerRandom:
            self.timer = 0
            self.timerRandom = random.randrange(0, 20) - 10
            self.target = self.targetlist[random.randrange(0, len(self.targetlist) - 1) + 1]
            self.isGoingForTarget = True

    def aiAction(self):
        # "", "left", "right", "jump", "ball", "ball", "away", "away"

        if self.isGoingForTarget:
            if self.target == "left":
                if self.statusEffect == "frozen":
                    self.speed.x /= 1.01
                elif self.statusEffect == "stuck":
                    self.speed.x /= 1.9
                else:
                    self.speed.x = 0 - self.max_speed
                    self.lastMoveDir.x = -1
            else:
                self.speed.x /= 1.9
        
            if self.target == "right":
                if self.statusEffect == "frozen":
                    self.speed.x /= 1.01
                elif self.statusEffect == "stuck":
                    self.speed.x /= 1.9
                else:
                    self.speed.x = self.max_speed
                    self.lastMoveDir.x = 1
                
            if self.statusEffect != "stuck":
                if self.target == "jump" and self.canJump:
                    self.speed.y = 0 - self.max_speed * 2.2
                    if isMuted == False: self.jumpsfx.play()

            if self.target == "away":
                if self.statusEffect == "frozen":
                    self.speed.x /= 1.01
                elif self.statusEffect == "stuck":
                    self.speed.x /= 1.9
                else:
                    x = []
                    temp = 0
                    for player in playerList:
                        temp = self.pos.x - player.pos.x
                        x.append(temp)

                    for player in aiList:
                        if player != self:
                            temp = self.pos.x - player.pos.x
                            x.append(temp)

                    temp = get_closest_value(x, 0)

                    if temp < 0:
                        self.speed.x = 0 - self.max_speed
                        self.lastMoveDir.x = -1
                    else:
                        self.speed.x /= 1.9
                    if temp > 0:
                        self.speed.x = self.max_speed
                        self.lastMoveDir.x = 1

            if self.target == "ball":
                if self.statusEffect == "frozen":
                    self.speed.x /= 1.01
                elif self.statusEffect == "stuck":
                    self.speed.x /= 1.9
                else:
                    x = []
                    temp = 0
                    for player in ballList:
                        temp = self.pos.x - player.pos.x
                        x.append(temp)

                    if x != []:
                        temp = get_closest_value(x, 0)

                    if temp > 0:
                        self.speed.x = 0 - self.max_speed
                        self.lastMoveDir.x = -1
                    else:
                        self.speed.x /= 1.9
                    if temp < 0:
                        self.speed.x = self.max_speed
                        self.lastMoveDir.x = 1

            self.pickup()

    def statusHandler(self):
        if self.hasStatus:
            self.statusTimer += 1
            if self.statusTimer >= 2 * FPS:
                self.statusTimer = 0
                self.hasStatus = False
                self.statusEffect = ""

            if self.statusEffect == "fire":
                self.hp -= 0.1

    def die(self):
        global player, aiList
        for player in aiList:
            if player == self:
                aiList.remove(player)
                del player
                player = Ai((60, 60), (50, 50))
                aiList.append(player)
                break

class MainMenu:
    def __init__(self):
        class Button:
            def __init__(self, pos, size, text, tuttext=False, col=(0, 0, 0), rainbow=(False, 0)):
                self.rect = pg.Rect(pos[0], pos[1], size[0], size[1])
                self.text = text
                self.textcol = col
                self.col = (255, 255, 255)
                self.prevClicked = False
                self.mouse = pg.mouse.get_pos()
                self.mouseClicked = pg.mouse.get_pressed(3)
                self.mouseClicked = self.mouseClicked[0]
                self.tut = tuttext
                self.isRainbow = rainbow[0]
                self.sat = rainbow[1]
                if self.isRainbow:
                    self.hue = 0

                self.mouseRect = pg.Rect(self.mouse[0], self.mouse[1], 1, 1)

            def tick(self):
                if self.isRainbow:
                    self.hue += 0.01
                    self.textcol = hsv2rgb(self.hue, self.sat, 0.3)
                if self.tut == False:
                    self.surf = menu_font.render(self.text, True, self.textcol)
                else:
                    self.surf = tut_font.render(self.text, True, self.textcol)
                self.rect_b = self.surf.get_rect(topleft = (self.rect.left, self.rect.top))
                self.rect_b = pg.Rect((self.rect_b.x - 5,self.rect_b.y - 5), (self.rect_b.width + 15,self.rect_b.height + 10))
                pg.draw.rect(screen, self.col, self.rect_b)
                screen.blit(self.surf, self.rect)

                self.prevClicked = self.mouseClicked

            def get_clicked(self):
                self.mouse = pg.mouse.get_pos()
                self.mouseClicked = pg.mouse.get_pressed(3)
                self.mouseClicked = self.mouseClicked[0]

                self.mouseRect = pg.Rect(self.mouse[0], self.mouse[1], 1, 1)
                if self.mouseRect.colliderect(self.rect_b):
                    if self.mouseClicked != self.prevClicked:
                        if self.mouseClicked == False:
                            return True
                else:
                    return False

        self.levelTypes = ["default", "editor", "empty", "boss", "level1"]
        self.levelDict = {}
        self.isInLevelSel = False
        self.isInTut = False
        self.isInCredits = False

        self.titleText = "COOL BALL GAME"
        self.titleCol = (0, 0.4, 1)

        self.bgSurf = pg.image.load(r'assets\art\bg\mainBG.png')
        self.bgRect = self.bgSurf.get_rect(topleft = (0, 0))

        self.playButton = Button((SCREEN_WIDTH / 2 - 50, 300), (100, 100), "Play")
        self.playButton.tick()

        self.quitButton = Button((SCREEN_WIDTH / 2 - 50, 400), (100, 100), "Quit")
        self.quitButton.tick()

        self.tutorialButton = Button((SCREEN_WIDTH / 2 - 50, 200), (100, 100), "Tutorial")
        self.tutorialButton.tick()

        self.creditButton = Button((50, 420), (100, 100), "Credits")
        self.creditButton.tick()

        self.tutbutton1 = Button((30, 100), (100, 100), "Use A and D to move", tuttext=True)
        self.tutbutton2 = Button((30, 150), (100, 100), "Press SPACEBAR to jump", tuttext=True)
        self.tutbutton3 = Button((30, 200), (100, 100), "Press E to pick up the ball", tuttext=True)
        self.tutbutton4 = Button((30, 250), (100, 100), "Press E again to throw the ball towards the mouse pointer", tuttext=True)
        self.tutbutton5 = Button((30, 300), (100, 100), "When frozen, you cannot move, but can still jump", tuttext=True)
        self.tutbutton6 = Button((30, 350), (100, 100), "When grounded by nature, you cannot move or jump", tuttext=True)
        self.tutbutton7 = Button((30, 400), (100, 100), "When burning, you will take damage over time", tuttext=True)
        self.tutbutton8 = Button((30, 450), (100, 100), "Press ESC to close the game and TAB to return to the menu", tuttext=True)
        self.tutbutton1.tick()
        self.tutbutton2.tick()
        self.tutbutton3.tick()
        self.tutbutton4.tick()
        self.tutbutton5.tick()
        self.tutbutton6.tick()
        self.tutbutton7.tick()
        self.tutbutton8.tick()

        self.tutExitButton = Button((30, 20), (100, 100), "Return To Menu", tuttext=True, col=(50, 50, 50))
        self.tutExitButton.tick()

        self.selExitButton = Button((40, 20), (100, 100), "Return To Menu", tuttext=True, col=(50, 50, 50))
        self.selExitButton.tick()

        self.creditExitButton = Button((40, 20), (100, 100), "Return To Menu", tuttext=True, col=(50, 50, 50))
        self.creditExitButton.tick()

        self.tutImg1 = pg.image.load(r'assets\art\karakterer\Billy\billy0039.png')
        self.tutImg1 = pg.transform.scale(self.tutImg1, (100, 100))
        self.tutImg2 = pg.image.load(r'assets\art\karakterer\Billy\billyFrozen.png')
        self.tutImg2 = pg.transform.scale(self.tutImg2, (100, 100))
        self.tutImg3 = pg.image.load(r'assets\art\karakterer\Billy\billyStuck.png')
        self.tutImg3 = pg.transform.scale(self.tutImg3, (100, 100))
        self.tutImg4 = pg.image.load(r'assets\art\karakterer\Billy\billy0007.png')
        self.tutImg4 = pg.transform.scale(self.tutImg4, (100, 100))
        self.tutparticle = ParticleSystem((800, 100), (0, -15), 1, 10, (255, 215, 0), 10, 10, 1)


        self.creditButton1  = Button((30, 100), (100, 100), "Devs:", tuttext=True)
        self.creditButton2  = Button((30, 150), (100, 100), "Abdirahjiin", tuttext=True)
        self.creditButton3  = Button((30, 200), (100, 100), "Alexander", tuttext=True)
        self.creditButton4  = Button((30, 250), (100, 100), "Julian", tuttext=True)
        self.creditButton5  = Button((30, 300), (100, 100), "Thor", tuttext=True, rainbow=(True, 1))
        self.creditButton6  = Button((30, 350), (100, 100), "Tor Aleksander", tuttext=True)
        #self.creditButton7  = Button((30, 400), (100, 100), "Victor", tuttext=True)    

        self.creditButton8  = Button((600, 100), (100, 100), "Music:", tuttext=True)
        self.creditButton9  = Button((600, 150), (100, 100), "SubspaceAudio", tuttext=True)
        self.creditButton10 = Button((600, 200), (100, 100), "Trevor Lentz", tuttext=True)

        self.creditButton1.tick()
        self.creditButton2.tick()
        self.creditButton3.tick()
        self.creditButton4.tick()
        self.creditButton5.tick()
        self.creditButton6.tick()
        #self.creditButton7.tick()
        self.creditButton8.tick()
        self.creditButton9.tick()
        self.creditButton10.tick()

        y = 300
        for i, val in enumerate(self.levelTypes):
            if i * 100 >= 300:
                y = 400
                i = 0
            button = Button((i * 200 + 200, y), (100, 100), val)
            self.levelDict[val] = button
        for item in self.levelDict.items():
            item[1].tick()

    def tick(self):
        screen.blit(self.bgSurf, self.bgRect)
        if self.isInLevelSel == False and self.isInTut == False and self.isInCredits == False:
            if self.playButton.get_clicked():
                startGame("default")
            if self.quitButton.get_clicked():
                quit()
            if self.tutorialButton.get_clicked():
                self.isInTut = True
            if self.creditButton.get_clicked():
                self.isInCredits = True
                pg.mixer.music.unload()
                load_music("credits")
                pg.mixer.music.set_volume(0.5)
                pg.mixer.music.play(loops=-1)
            self.playButton.tick()
            self.quitButton.tick()
            self.tutorialButton.tick()
            self.creditButton.tick()

            self.titleCol = (self.titleCol[0] + 0.01, 0.4, 1)
            if self.titleCol[0] > 1:
                self.titleCol = (0, 0.4, 1)
            surf = title_font.render(self.titleText, True, hsv2rgb(self.titleCol[0], self.titleCol[1], self.titleCol[2]))
            rect_b = surf.get_rect(center = (SCREEN_WIDTH / 2, 50))
            screen.blit(surf, rect_b)
        
        if self.isInTut == False and self.isInLevelSel and self.isInCredits == False:
            if self.selExitButton.get_clicked():
                self.isInLevelSel = False
            self.selExitButton.tick()
            for item in self.levelDict.items():
                item[1].tick()
                if item[1].get_clicked():
                    startGame(item[0])
        if self.isInTut and self.isInLevelSel == False and self.isInCredits == False:
            if self.tutExitButton.get_clicked():
                self.isInTut = False
            self.tutbutton1.tick()
            self.tutbutton2.tick()
            self.tutbutton3.tick()
            self.tutbutton4.tick()
            self.tutbutton5.tick()
            self.tutbutton6.tick()
            self.tutbutton7.tick()
            self.tutbutton8.tick()
            self.tutExitButton.tick()
            rect = self.tutImg1.get_rect(topleft = (500, 70))
            screen.blit(self.tutImg1, rect)
            rect = self.tutImg2.get_rect(topleft = (600, 70))
            screen.blit(self.tutImg2, rect)
            rect = self.tutImg3.get_rect(topleft = (700, 70))
            screen.blit(self.tutImg3, rect)
            self.tutparticle.tick((850, 130))
            rect = self.tutImg4.get_rect(topleft = (800, 70))
            screen.blit(self.tutImg4, rect)

        if self.isInTut == False and self.isInLevelSel == False and self.isInCredits:
            if self.creditExitButton.get_clicked():
                self.isInCredits = False
                pg.mixer.music.unload()
                load_music("menu")
                pg.mixer.music.set_volume(0.5)
                pg.mixer.music.play(loops=-1)
            self.creditButton1.tick()
            self.creditButton2.tick()
            self.creditButton3.tick()
            self.creditButton4.tick()
            self.creditButton5.tick()
            self.creditButton6.tick()
            #self.creditButton7.tick()
            self.creditButton8.tick()
            self.creditButton9.tick()
            self.creditButton10.tick()
            self.creditExitButton.tick()

pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()

window = pg.display.Info()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 512
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
game_font = pg.font.Font(None, 25)
menu_font = pg.font.Font(None, 75)
title_font = pg.font.Font(None, 120)
tut_font = pg.font.Font(None, 50)
isRunning = True
FPS = 60
isMuted = True
isInEditor = False
isInMenu = True
pg.mixer.music.set_volume(0.5)

def load_music(place):
    if place == "match":
        x = random.randint(1, 3)
        y = r'assets\lyd\Music\Juhani Junkala [Retro Game Music Pack] Level ' + str(x) + '.wav'
    if place == "menu":
        y = r'assets\lyd\Music\A-Better-World.wav'
    if place == "credits":
        y = r'assets\lyd\Music\Lines-of-Code.wav'
    pg.mixer.music.load(y)

load_music("menu")
#pg.mixer.music.play(loops=-1)

blockList = []
ballList = []
playerList = []
aiList = []
combinedList = playerList + aiList

if isInEditor:
    editor = EditorHandler()

loadSaves(dir='level1')

hud = HUD()

menu = MainMenu()

while isRunning == True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            quit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                quit()
            if event.key == pg.K_TAB:
                isInMenu = True
                menu.isInLevelSel = False
                menu.isInTut = False
                menu.isInCredits = False
                pg.mixer.music.unload()
                load_music("menu")
                pg.mixer.music.set_volume(0.5)
                pg.mixer.music.play(loops=-1)
                aiList.clear()
                playerList.clear()
                blockList.clear()
                ballList.clear()

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

            if event.key == pg.K_r:
                for player in playerList:
                    player.hp -= 1
                for player in aiList:
                    player.hp -= 1

        if isInEditor:
            if event.type == pg.MOUSEWHEEL:
                editor.setLength(event.y * 50)
                #print("y")

    screen.fill((0, 0, 0))
    if isInMenu == False:
        screen.blit(bgimg, bgrect)

        for block in blockList:
            block.tick()

        for player in playerList:
            player.tick()
    
        for ai in aiList:
            ai.tick()
    
        for ball in ballList:
            ball.tick()

        if isInEditor:
            editor.tick()

        hud.tick()
        combinedList = playerList + aiList

    else:
        menu.tick()

    pg.display.update()
    clock.tick(FPS)

levela.close()
levelr.close()
quit()
