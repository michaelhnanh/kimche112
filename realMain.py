from cmu_graphics import *
from background import *
# from upgrades import *
# from weapons import *
from enemy import *
import math, random

base = 'cmu://872298/35005449/kerrybase.png'
base75 = 'cmu://872298/35005453/kerrybase75.png'
base50 = 'cmu://872298/35005456/kerrybase50.png'
base25 = 'cmu://872298/35005457/kerrybase25.png'
hit75 = 'cmu://872298/35005459/kerryhit75.png'
hit50 = 'cmu://872298/35005461/kerryhit50.png'
hit25 = 'cmu://872298/35005463/kerrryhit25.png'

def onAppStart(app):
    #main menu
    app.mainMenu = True
    app.hoverStart = False
    app.hoverRetry = False

    #wave maker
    app.waveCount = 5
    spawnWave(app, app.waveCount)
    
    #larger level variables
    app.step = 0
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

    app.linex1 = 0
    app.liney1 = 0
    app.lineLength = 25

    app.lineAngle = 90
    app.bulletAngle = 90

    app.kerryurl = base

    generateBackground(app)

class Player():
    def __init__(self):
        self.x = 350
        self.y = 350
        self.movespeed = 7
        self.maxHealth = 100
        self.health = 100
        self.xp = 0
        self.level = 0
        self.upgrades = []
        self.weapon = None
        self.orientation = 0
        self.size = 50
    
def onStep(app):
    # enemy movement in general
    app.step += 1

    if app.player.health <= (app.player.maxhealth * 0.75):
        app.kerryurl = base75
    elif app.player.health <= (app.player.maxhealth * 0.5):
        app.kerryurl = base50
    elif app.player.health <= (app.player.maxhealth * 0.25):
        app.kerryurl = base25

    for enemy in Enemy.enemyList:
        checkEnemyHit(app, enemy)

        if enemy.hp <= 0:
            Enemy.enemyList.remove(enemy)
        
        if enemy.timer != 0:
            enemy.timer -= 1
        elif enemy.timer == 0:
            enemy.moveOK = True

        # enemy movement to player
        if collidePlayer(app, enemy):
            app.player.damaged = True
            xScalar, yScalar = moveTo(app.player, enemy)
            enemy.x += xScalar * enemy.movespeed * 10
            enemy.y += yScalar * enemy.movespeed * 10

            enemy.moveOK = False
            enemy.timer = enemy.waitTime
            app.player.health -= enemy.damage
            
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

    for bullet in Bullet.bulletList:
        newX, newY = getRadiusEndpoint(bullet.x, bullet.y, 5, bullet.angleFired)
        bullet.x, bullet.y = newX, newY
        
        if (bullet.x + bullet.radius <= 0 or bullet.x - bullet.radius >= app.width
                or bullet.y + bullet.radius <= 0 or bullet.y + bullet.radius <= 0):
            try:
                Bullet.bulletList.remove(bullet)
            except ValueError as e:
                print('fuck you bitch')
        
        for enemy in Enemy.enemyList:
            if distance(bullet.x, bullet.y, enemy.x, enemy.y) <= enemy.size:
                enemy.hp -= bullet.damage
                try:
                    Bullet.bulletList.remove(bullet)
                except ValueError as e:
                    print('fuck you bitch')

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
     
class Bullet(Weapon):
    bulletList = []
    bulletId = 0
    def __init__(self, x, y, radius, angleFired, damage):
        Bullet.bulletId += 1
        self.id = Bullet.bulletId
        Bullet.bulletList.append(self)
        self.x = x
        self.y = y
        self.radius = radius
        self.angleFired = angleFired
        self.damage = damage

def getRadiusAndAngleToEndpoint(cx,cy,targetX,targetY):
    radius = distance(cx,cy,targetX,targetY)
    angle = math.degrees(math.atan2(cy-targetY,targetX-cx)) % 360
    return (radius,angle)

def getRadiusEndpoint(cx,cy,r,theta):
        return (cx + r*math.cos(math.radians(theta)),
                (cy - r*math.sin(math.radians(theta))))

def onMouseMove(app,mouseX,mouseY):
    radius, angle = getRadiusAndAngleToEndpoint(app.player.x, app.player.y, mouseX, mouseY)
    app.lineAngle = angle
    app.linex1, app.liney1 = getRadiusEndpoint(app.player.x, app.player.y, app.lineLength, app.lineAngle)
    if app.mainMenu:
        if app.width//2-95 <= mouseX <= app.width//2+95 and 365 <= mouseY <= 435:
            app.hoverStart = True
        else:
            app.hoverStart = False
    if app.player.health <= 0:
        if app.width//2-110 <= mouseX <= app.width//2+110 and 370 <= mouseY <= 430:
            app.hoverRetry = True
        else:
            app.hoverRetry = False

def onMousePress(app,mouseX,mouseY):
    if app.mainMenu:
        if app.width//2-95 <= mouseX <= app.width//2+95 and 365 <= mouseY <= 435:
            app.mainMenu = False
            spawnWave(app, 1)
    elif app.player.health <= 0:
        if app.width//2-110 <= mouseX <= app.width//2+110 and 370 <= mouseY <= 430:
            app.player.health = 100
            Enemy.enemyList = []
            spawnWave(app, 1)
    else:
        x, y = getRadiusEndpoint(app.player.x, app.player.y, app.player.size//2, app.lineAngle)
        bullet = Bullet(x, y, 5, app.lineAngle, damage = 30)

def distance(x0,y0,x1,y1):
    return ((x1-x0)**2+(y1-y0)**2)**0.5

def moveTo(target, chaser):
    xToTarget = chaser.x - target.x
    yToTarget = chaser.y - target.y
    length = (xToTarget ** 2 + yToTarget ** 2) ** 0.5
    if length < 1:
        length = 1
    normalX = xToTarget / length
    normalY = yToTarget / length
    return normalX, normalY



def redrawAll(app):
    drawBackground(app)
    drawBackground(app)
    for enemy in Enemy.enemyList:
        drawCircle(enemy.x, enemy.y, 25, fill='red')
        if enemy.attack and not enemy.moveOK:
            drawCircle(enemy.x, enemy.y, 60, fill='red', opacity=50)

    health = app.player.health//1
    drawRect(10, 7.5, 160, 45)
    drawLabel(f'HP: {health}', 90, 30, size=40, fill='white', bold=True)

    drawRect(app.player.x, app.player.y, 50, 50, fill='cyan', align='center')
    try:
        drawImage(app.kerryurl, app.player.x, app.player.y, align = 'center', width = app.player.size, height = app.player.size)
    except: 
        print('goon')
    # drawRect(app.width//2,app.height-25,400,50,fill=None,border='red',align='center')
    # drawLabel('Weapon', app.width//2,app.height-42,size=14,bold=True)
    # drawRect(app.width//2-app.width//5,app.height-20,100,30,fill=None,border='red',align='center')
    # drawLabel('Sword', app.width//2-app.width//5,app.height-20)
    # drawRect(app.width//2,app.height-20,100,30,fill=None,border='red',align='center')
    # drawLabel('Gun1',app.width//2,app.height-20)
    # drawRect(app.width//2+app.width//5,app.height-20,100,30,fill=None,border='red',align='center')
    # drawLabel('Gun2',app.width//2+app.width//5,app.height-20)

    # gun line
    drawLine(app.player.x, app.player.y, app.linex1, app.liney1, opacity=100, lineWidth = 2)

    for bullet in Bullet.bulletList:
        drawCircle(bullet.x, bullet.y, bullet.radius, fill='blue')

    if app.mainMenu:
        drawRect(0, 0, app.width, app.height)
        drawLabel('KERRY', app.width//2, 120, fill='white', size=100, bold=True, italic=True)
        drawLabel('KILLR', app.width//2, 220, fill='white', size=100, bold=True, italic=True)
        drawLabel('START', app.width//2, 400, fill='white', size=50, bold=True)
        if app.hoverStart:
            drawRect(app.width//2-95, 365, 190, 70, fill=None, border='white', borderWidth=2)
    
    if app.player.health <= 0:
        drawRect(0, 0, app.width, app.height)
        drawLabel('GAME', app.width//2, 120, fill='white', size=100, bold=True, italic=True)
        drawLabel('OVR!', app.width//2, 220, fill='white', size=100, bold=True, italic=True)
        drawLabel('RETRY?', app.width//2, 400, fill='white', size=50, bold=True)
        if app.hoverRetry:
            drawRect(app.width//2-110, 370, 220, 60, fill=None, border='white', borderWidth=2)



    # if app.arrowVisible:
    #     drawLine(app.linex0+25,app.liney0+25,app.linex1,app.liney1,opacity=100)
    

    

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
        for bullet in Bullet.bulletList:
            bullet.x -= app.moveVectorX
            bullet.y -= app.moveVectorY
        for row in app.bg:
            for tile in row:
                tile.x -= app.moveVectorX
                tile.y -= app.moveVectorY

def onKeyRelease(app, keys):
    app.moveVectorX, app.moveVectorY = 0, 0

def onMouseClick(app):
    pass

def distance(x0,y0,x1,y1):
    return ((x1-x0)**2+(y1-y0)**2)**0.5

runApp()