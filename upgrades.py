from cmu_graphics import *
# from background import *
# from upgrades import *
# from weapons import *
from enemy import *
import math, random

class Upgrade():
    def __init__(self, name):
        self.name = name
    
    def activateUpgrade(self, other, name, app):
        for attribute in app.upgradesList[name]:
            if attribute == 'movespeedmult':
                other.movespeed *= Upgrade.upgradesList[name][attribute]
            if attribute == 'healthup':
                other.health += Upgrade.upgradesList[name][attribute]
            if attribute == 'damageup':
                Weapon.damage += Upgrade.upgradesList[name][attribute]
            if attribute == 'damagemult':
                Weapon.damage *= Upgrade.upgradesList[name][attribute]
            if attribute == 'rangeup':
                Weapon.range += Upgrade.upgradesList[name][attribute]
            if attribute == 'rangemult':
                Weapon.range *= Upgrade.upgradesList[name][attribute]
            if attribute == 'auraactive':
                Aura.active = Upgrade.upgradesList[name][attribute]
            if attribute == 'aura':
                app.aura.width += Upgrade.upgradesList[name][attribute]
            if attribute == 'auradamage':
                app.aura.damage += Upgrade.upgradesList[name][attribute]
            if attribute == 'frequency':
                app.aura.freq = Upgrade.upgradesList[name][attribute]

class Aura:
    active = False
    
    def __init__(self, width, damage, freq):
        self.width = width
        self.damage = damage
        self.freq = freq