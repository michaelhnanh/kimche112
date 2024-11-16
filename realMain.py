from cmu_graphics import *
import math, random

def onAppStart(app):
    spawnWave(15)
    
    app.stepsPerSecond = 100
    app.width = 700
    app.height = 700
    app.player = Player()
    app.moveVectorX = 0
    app.moveVectorY = 0
    
    # weapon init
    app.weaponBallX = app.player.x
    app.weaponBallY = app.player.y
    app.bulletVisible = False
    app.swordVisible = True
    app.linex0 = app.player.x
    app.liney0 = app.player.y
    app.linex1 = 200
    app.liney1 = 350
    app.lineLength = 50
    app.lineAngle = 90
    app.bulletVisible = False
    app.bulletx0 = 0
    app.bullety0 = 0
    app.bulletR = 10
    app.bulletAngle = 90

    generateBackground(app)

class Player():
    def __init__(self):
        self.x = 350
        self.y = 350
        self.movespeed = 3
        self.maxHealth = 100
        self.health = 100
        self.xp = 0
        self.level = 0
        self.upgrades = []
        self.weapon = None
        self.orientation = 0

        self.size = 50
        self.damageTimer = 0
        self.damageWait = 200
        self.damaged = False
        self.color = 'blue'

class Upgrade():
    def __init__(self):
        self.active = False

class Tile():
    color = 1
    tileID = 0
    def __init__(self, cx, cy, app):
        self.x = cx
        self.y = cy
        self.ledge = self.x - app.width//2
        self.redge = self.x + app.width//2
        self.dedge = self.y + app.width//2
        self.uedge = self.y - app.width//2
        if Tile.color > 0:
            self.color = 'gray'
        else:
            self.color = 'darkGray'
        Tile.color *= -1
        self.ID = Tile.tileID
        Tile.tileID += 1

    def __repr__(self):
        return f'{self.ID}'

    def updateEdges(self, app):
        self.ledge = self.x - app.width//2
        self.redge = self.x + app.width//2
        self.dedge = self.y + app.width//2
        self.uedge = self.y - app.width//2

class Weapon:
     def __init__(self,name,damage,range):
          self.name = name
          self.damage = damage
          self.range = range

     def __repr__(self):
          return f'Attacking with {self.name}'
     
     def hitEnemy(self,damage,range):
          for enemy in Enemy.enemyList:
            enemyDistance=distance(app.player.x,app.player.y,app.enemy.x,app.enemy.y)
            if self.range>=enemyDistance:
                app.enemy.hp-=self.damage
                print(f'{self.name} hit the enemy!')
                if app.enemy.hp==0:
                     Enemy.enemyList.pop(enemy)
            else:
                return 'Oops,off target!'
        
class Sword(Weapon):
     def __init__(self,name,damage,range,speed):
         super().__init__(name='sword',damage=50,range=10)
         self.speed = speed
     
     def hit(self):
         return 'You are swing the sword'

class Gun1(Weapon):
     def __init__(self,name,damage,range,speed):
         super().__init__(name='gun1',damage=100,range=30)
         self.speed = speed

     def hit(self):
         return 'You are using the gun1'
     
class Gun2(Weapon):
     def __init__(self,name,damage,range,speed):
         super().__init__(name='gun2',damage=70,range=30)
         self.speed = speed

     def hit(self):
         return 'You are using the gun2'
     
class bullet(Weapon):
    bulletList = []
    bulletId = 0
    def __init__(self,name):
        self.name = name
        bullet.bulletId += 1
        self.id = bullet.bulletId
        bullet.bulletList.append(self)

    def projectilePath(self, enemy):
        for enemy in Enemy.enemyList:
            enemyDistance = distance(app.player.x,app.player.y,app.enemy.x,app.enemy.y)
            if self.range >= enemyDistance:
                for step in range(11):
                    x = (enemyDistance/10)*step
                    y = math.tan(math.radians(45)*x-(9.8/(2*(self.speed**2)))*(math.cos(math.radians(45))**2))*(x**2)
                return f'{self.name} fired towards enemy'
            else:
                return f'{self.name} is out of range to hit enemy'

class Enemy:
    enemyList = []
    enemyId = 0
    def __init__(self, sprite, movespeed, totalhp, damage, species):
        degree = math.radians(random.randrange(0, 360, 20))
        self.x = 350+500*math.cos(degree)
        self.y = 350+500*math.sin(degree)
        self.movespeed = movespeed
        self.sprite = sprite
        self.hp = totalhp
        self.damage = damage
        self.species = species
        Enemy.enemyId += 1
        self.id = Enemy.enemyId
        self.moveOK = True

        self.size = 25

        self.timer = 0
        self.waitTime = 50
        
        Enemy.enemyList.append(self)

    def __repr__(self):
        return f'{self.species}, {self.hp} HP'

def spawnWave(count):
    for _ in range(count):
        enemy = Enemy('red', 0.75, 100, 10, 'cookie')
    
def onStep(app):
    # enemy movement in general
    for enemy in Enemy.enemyList:
        if enemy.moveOK == False:
            enemy.timer += 1
        if enemy.timer == enemy.waitTime:
            enemy.timer = 0
            enemy.moveOK = True
            
        if app.player.damaged == True:
            app.player.color = 'cyan'
            app.player.damageTimer += 1
        else:
            app.player.color = 'blue'
        if app.player.damageTimer == app.player.damageWait:
            app.player.damageTimer = 0 
            app.player.damaged = False

        # enemy movement to player
        if collidePlayer(app, enemy):
            app.player.damaged = True
            xScalar, yScalar = moveTo(app.player, enemy)
            enemy.x += xScalar * enemy.movespeed*10
            enemy.y += yScalar * enemy.movespeed*10
            enemy.moveOK = False
        if enemy.moveOK == True:
            xScalar, yScalar = moveTo(app.player, enemy)
            enemy.x -= xScalar * enemy.movespeed
            enemy.y -= yScalar * enemy.movespeed

        # enemy collision checking
        for other in Enemy.enemyList:
            if enemy.id != other.id:
                d = distance(enemy.x, enemy.y, other.x, other.y)
                if d <= (enemy.size + other.size):
                    #enemy move away from other enemy
                    xScalar, yScalar = moveTo(enemy, other)
                    enemy.x -= xScalar * enemy.movespeed
                    enemy.y -= yScalar * enemy.movespeed

    if app.bulletVisible:
        newX, newY = getRadiusEndpoint(app.bulletx0, app.bullety0, 5 , app.bulletAngle)
        app.bulletx0, app.bullety0 = newX, newY
        
        if (app.bulletx0+app.bulletR<=0 or app.bulletx0-app.bulletR>=app.width
                or app.bullety0+app.bulletR<=0):
                    app.bulletVisible=False
                    
def collidePlayer(app, enemy):
    xDistance = abs(app.player.x - enemy.x)
    yDistance = abs(app.player.y - enemy.y)
    if xDistance <= app.player.size and yDistance <= app.player.size:
        return True


def moveTo(target, chaser):
    xToTarget = chaser.x - target.x
    yToTarget = chaser.y - target.y
    length = (xToTarget ** 2 + yToTarget ** 2) ** 0.5
    if length < 1:
        length = 1
    normalX = xToTarget / length
    normalY = yToTarget / length
    return normalX, normalY

def generateBackground(app):
    app.bg = []
    i = 0
    for row in range(-3, 4):
        app.bg.append([])
        for col in range(-3, 4):
            tile = Tile((app.width//3)*col, (app.height//3)*row, app)
            app.bg[i].append(tile)
        i += 1

def drawBackground(app):
    for row in app.bg:
        for tile in row:
            tile.updateEdges(app)
            if tile.ledge > app.width:
                tile.x -= app.width//3*5
                if tile.color == 'gray':
                    tile.color = 'darkGray'
                elif tile.color == 'darkGray':
                    tile.color = 'gray'
            if tile.redge < 0:
                tile.x += app.width//3*5
                if tile.color == 'gray':
                    tile.color = 'darkGray'
                elif tile.color == 'darkGray':
                    tile.color = 'gray'
            if tile.uedge > app.height:
                tile.y -= app.height//3*5*6
                # if tile.color == 'gray':
                #     tile.color = 'darkGray'
                # elif tile.color == 'darkGray':
                #     tile.color = 'gray'
            if tile.dedge < 0:
                tile.y += app.height//3*6
                # if tile.color == 'gray':
                #     tile.color = 'darkGray'
                # elif tile.color == 'darkGray':
                #     tile.color = 'gray'
            drawRect(tile.x, tile.y, app.width//3, app.height//3, fill=tile.color, align='center')


def redrawAll(app):
    drawBackground(app)
    for enemy in Enemy.enemyList:
        drawCircle(enemy.x, enemy.y, enemy.size, fill=enemy.sprite)
    drawRect(app.player.x, app.player.y, app.player.size, app.player.size, fill=app.player.color, align = 'center')

    drawRect(app.width//2,app.height-25,400,50,fill=None,border='red',align='center')
    drawLabel('Weapon', app.width//2,app.height-42,size=14,bold=True)
    drawRect(app.width//2-app.width//5,app.height-20,100,30,fill=None,border='red',align='center')
    drawLabel('Sword', app.width//2-app.width//5,app.height-20)
    drawRect(app.width//2,app.height-20,100,30,fill=None,border='red',align='center')
    drawLabel('Gun1',app.width//2,app.height-20)
    drawRect(app.width//2+app.width//5,app.height-20,100,30,fill=None,border='red',align='center')
    drawLabel('Gun2',app.width//2+app.width//5,app.height-20)

    # if app.arrowVisible:
    #     drawLine(app.linex0+25,app.liney0+25,app.linex1,app.liney1,opacity=100)
    
    drawLine(app.linex0+25,app.liney0+25,app.linex1,app.liney1,opacity=100)
    if app.bulletVisible:
        drawCircle(app.bulletx0,app.bullety0,app.bulletR,fill='blue')
    

def onKeyHold(app, keys):
    if 'right' in keys or 'd' in keys:
        app.moveVectorX = app.player.movespeed
    if 'left' in keys or 'a' in keys:
        app.moveVectorX = -1 * app.player.movespeed
    if 'up' in keys or 'w' in keys:
        app.moveVectorY = -1 * app.player.movespeed
    if 'down' in keys or 's' in keys:
        app.moveVectorY = app.player.movespeed
    if ('w' in keys and 'd' in keys) or ('up' in keys and 'right' in keys):
        app.moveVectorX, app.moveVectorY = (1/2**0.5)*app.player.movespeed, -(1/2**0.5)*app.player.movespeed
    if ('s' in keys and 'd' in keys) or ('down' in keys and 'right' in keys):
        app.moveVectorX, app.moveVectorY = (1/2**0.5)*app.player.movespeed, (1/2**0.5)*app.player.movespeed
    if ('w' in keys and 'a' in keys) or ('up' in keys and 'left' in keys):
        app.moveVectorX, app.moveVectorY = -(1/2**0.5)*app.player.movespeed, -(1/2**0.5)*app.player.movespeed
    if ('s' in keys and 'a' in keys) or ('down' in keys and 'left' in keys):
        app.moveVectorX, app.moveVectorY = -(1/2**0.5)*app.player.movespeed, (1/2**0.5)*app.player.movespeed
    moveWorld(app)

def moveWorld(app):
    if app.moveVectorX != 0 or app.moveVectorY != 0:
        for enemy in Enemy.enemyList:
            enemy.x -= app.moveVectorX
            enemy.y -= app.moveVectorY
        for row in app.bg:
            for tile in row:
                tile.x -= app.moveVectorX
                tile.y -= app.moveVectorY

def onKeyRelease(app, keys):
    app.moveVectorX, app.moveVectorY = 0, 0
        
def onMouseMove(app,mouseX,mouseY):
    radius,angle=getRadiusAndAngleToEndpoint(app.linex0,app.liney0,mouseX,mouseY)
    app.lineAngle=angle
    app.linex1,app.liney1=getRadiusEndpoint(app.linex0,app.liney0,app.lineLength,app.lineAngle)

def onMousePress(app,mouseX,mouseY):
    app.bulletVisible = True
    x, y = getRadiusEndpoint(app.linex0,app.liney0,app.lineLength+app.bulletR,app.lineAngle)
    app.bulletx0, app.bullety0 = x, y
    app.bulletAngle = app.lineAngle

def getRadiusAndAngleToEndpoint(cx,cy,targetX,targetY):
    radius=distance(cx,cy,targetX,targetY)
    angle=math.degrees(math.atan2(cy-targetY,targetX-cx))%360
    return (radius,angle)

def getRadiusEndpoint(cx,cy,r,theta):
        return (cx+r*math.cos(math.radians(theta)),
                (cy-r*math.sin(math.radians(theta))))

def onMouseClick(app):
    pass

def distance(x0,y0,x1,y1):
    return ((x1-x0)**2+(y1-y0)**2)**0.5

runApp()