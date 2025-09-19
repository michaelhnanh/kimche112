from cmu_graphics import *
# from background import *
# from upgrades import *
# from weapons import *
from enemy import *

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
