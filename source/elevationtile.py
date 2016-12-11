from PIL import Image
from urllib.request import urlopen
from io import BytesIO
import numpy as np
from tile import *

class ElevationTile(Tile):
    def __init__(self, x=0, y=0, zoom=0):
        Tile.__init__(self, x,y, zoom)
        self.elevation = np.zeros((256, 256, 1))

    def getType(self):
        return "ElevationTile"

    def downloadSRTMData(self):
        urldata = "https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"
        url = urldata.format(x=self.x,y=self.y,z=self.zoom)
        try:
            response = urlopen(url)
            buffer = BytesIO(response.read())
            im = Image.open(buffer)
            data = np.array(im)
            im.close()

            for y in range(data.shape[0]):
                for x in range(data.shape[1]):
                    r = data[y][x][0]
                    g = data[y][x][1]
                    b = data[y][x][2]

                    height = (r * 256 + g + b / 256) - 32768.
                    self.elevation[y][x][0] = height
        except:
            print("Error downloading SRTM data...")

