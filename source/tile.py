import math

class Tile(object):
    def __init__(self, x=0, y=0, zoom=0):
        self.x = x
        self.y = y
        self.zoom = zoom

    def getType(self):
        return "BaseTile"

    def quadkey(self):
        return tilecoord2Quadkey(self.x, self.y, self.zoom)

    def normalizedcoord(self):
        q = self.quadkey()
        return quadKeyToNormalizedCoord(q)

# ------------------------------------------------------------------------------
# Functions to create Tiles:

def fromQuadkey(key):
    x,y,zoom = quadKeyToTileCoord(key)
    return Tile(x,y,zoom)

def fromTileCoord(x,y,zoom):
    return Tile(x,y,zoom)

def fromTMSTileCoord(x,y,zoom):
    return Tile(x, (2**zoom-1)-y, zoom)

def fromWGS84Coord(lng, lat, zoom):
    x,y,zoom = WGS84ToTile(lng,lat,zoom)
    return Tile(x,y,zoom)


# ------------------------------------------------------------------------------

def quadKeyToNormalizedCoord(key):
    zoomlevels = len(key)
    x = 0
    y = 0
    scale = 1.0
    for i in range(0, zoomlevels):
        scale /= 2.0
        if key[i] == "0":
            y += scale
        elif key[i] == "1":
            x += scale
            y += scale
        elif key[i] == "2":
            pass
        elif key[i] == "3":
            x += scale

    return [x, y, x + scale, y + scale]

# ------------------------------------------------------------------------------


def quadKeyToNormalizedMercatorCoord(key):
    zoomlevels = len(key)
    x = 0
    y = 0
    scale = 1.0
    for i in range(0,zoomlevels):
        scale /= 2.0
        if key[i] == "0":
            y += scale
        elif key[i] == "1":
            x += scale
            y += scale
        elif key[i] == "2":
            pass
        elif key[i] == "3":
            x += scale

    return [ x*2.-1.,  (y)*2.-1, (x + scale)*2-1, (y + scale)*2.-1.]

# ------------------------------------------------------------------------------


def quadKeyToTileCoord(key):
    zoom = len(key)
    x = 0
    y = 0

    for i in range(zoom,0,-1):
        mask = 2 ** (i-1)
        c = int(key[zoom-i])
        if (c & 1) != 0:
            x += mask
        if (c & 2) != 0:
            y += mask

    return [x,y,zoom]

# ------------------------------------------------------------------------------


def tilecoord2Quadkey(tx, ty, zoom):
    key = ""
    for i in range(zoom, 0, -1):
        digit = 0
        mask = 1 << (i - 1)
        if (tx & mask) != 0:
            digit += 1
        if (ty & mask) != 0:
            digit += 2
        key += str(digit)
    return key

# ------------------------------------------------------------------------------


def TMS2Quadkey(tx, ty, zoom):
    return tilecoord2Quadkey(tx, (2**zoom-1)-ty, zoom)

# ------------------------------------------------------------------------------


def normalizedMercatorToWGS84(x, y):
    x = x * math.pi
    y = y * math.pi

    t = math.exp(-y);
    lat = math.pi / 2 - 2.0 * math.atan(t)
    lng = x / 1.0
    return [lng * 57.295779513082320876798154814105, lat * 57.295779513082320876798154814105]

# ------------------------------------------------------------------------------


def quadkeyToWGS84(quadcode):
    lod = len(quadcode)
    mercator = quadKeyToNormalizedMercatorCoord(quadcode)
    t0 = normalizedMercatorToWGS84(mercator[0],mercator[1])
    t1 = normalizedMercatorToWGS84(mercator[2],mercator[3])
    return [t0[0], t0[1],  t1[0], t1[1]]

# ------------------------------------------------------------------------------


def WGS84ToTile(lng, lat, zoom):
    # bl = NormalizedMercatorToWGS84(-1,-1)
    # tr = NormalizedMercatorToWGS84(1,1)

    MinLongitude = -180  # bl[0]
    MaxLongitude = 180  # tr[0]
    MinLatitude = -85.05112877980659  # bl[1]
    MaxLatitude = 85.05112877980659  # tr[1]

    mapSize = pow(2, zoom) * 256  # Tile Size 256x256

    if lng < MinLongitude:
        lng = MinLongitude
    elif lng > MaxLongitude:
        lng = MaxLongitude

    if lat < MinLatitude:
        lat = MinLatitude
    elif lat > MaxLatitude:
        lat = MaxLatitude

    p = [0, 0, 0]
    p[0] = int((lng + 180.0) / 360.0 * (2 ** zoom))
    p[1] = int((1.0 - math.log(math.tan(lat * math.pi / 180.0)
                               + 1.0 / math.cos(lat * math.pi / 180.0)) / math.pi) / 2.0 * (2 ** zoom))
    p[2] = zoom
    return p

# ------------------------------------------------------------------------------


def WGS84ToQuadkey(lng, lat, zoom):
    t = WGS84ToTile(lng, lat, zoom)
    return tilecoord2Quadkey(t[0],t[1],zoom)

# ------------------------------------------------------------------------------


def tileToWGS84(x, y, zoom):
    key = tilecoord2Quadkey(x,y,zoom)
    return quadkeyToWGS84(key)

# ------------------------------------------------------------------------------

