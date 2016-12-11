from tile import *

class ImageTile(Tile):
    def __init__(self, x=0, y=0, zoom=0):
        Tile.__init__(self, x,y, zoom)


    def getType(self):
        return "ImageTile"