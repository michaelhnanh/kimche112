from cmu_graphics import *
import math

def onAppStart(app):
    app.width = 500
    app.height = 500
    app.characterBox = 50
    
    app.exp = []
    app.enemies = []

def redrawAll(app):
    drawCircle(app.width/2, app.height/2, app.characterBox, fill='cyan')

def main():
    runApp()

main()