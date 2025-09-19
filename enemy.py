from cmu_graphics import *
from background import *
from upgrades import *
# from weapons import *
from enemy import *
import math, random

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
        self.timer = 0
        self.waitTime = 100
        self.attack = False
        self.attackTimer = 100
        self.damage = 10

        self.size = 25
        self.hitbox = self.size//2
        
        Enemy.enemyList.append(self)

    def __repr__(self):
        return f'{self.species}, {self.hp} HP'

def spawnWave(app, count):
    for _ in range(count):
        enemy = Enemy('red', 5, 100, 10, 'cookie')

def collidePlayer(app, enemy):
    xDistance = abs(app.player.x - enemy.x)
    yDistance = abs(app.player.y - enemy.y)
    if xDistance <= (app.player.size//2 + enemy.size)  and yDistance <= (app.player.size//2 + enemy.size):
        return True

def checkEnemyHit(app, enemy):
    if collidePlayer(app, enemy):
        enemy.moveOK = False
        enemy.timer = enemy.waitTime
        enemy.attackTimer += 1

        if enemy.attackTimer % 100 == 0:
            app.player.health -= enemy.damage
        
        if 50 <= enemy.attackTimer%100 <= 100:
            enemy.attack = True
        else:
            enemy.attack = False
    else:
        enemy.attackTimer = 0

def enemyToPlayer(app, enemy):
    xToPlayer = enemy.x - app.player.x
    yToPlayer = enemy.y - app.player.y
    length = (xToPlayer ** 2 + yToPlayer ** 2) ** 0.5
    normalX = xToPlayer / length
    normalY = yToPlayer / length

    return enemy.movespeed * normalX, enemy.movespeed * normalY
