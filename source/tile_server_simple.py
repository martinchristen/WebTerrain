from flask import Flask, send_file
from elevationtile import *
from PIL import *
from spectra import *
from io import BytesIO

app = Flask(__name__)

@app.route("/elv/<z>/<x>/<y>")
def index(x,y,z):
    tile = ElevationTile(x,y,z)
    tile.downloadSRTMData()

    rgbdata = []
    for y in range(256):
        for x in range(256):
            rgb = calcSpecColor(tile.elevation[y][x], 0.0, 8850.0)
            data = (int(rgb[0] * 255.), int(rgb[1] * 255.), int(rgb[2] * 255.))
            rgbdata.append(data)

    im = Image.new("RGB", (256, 256))
    im.putdata(rgbdata)

    file = BytesIO()
    im.save(file, 'JPEG', quality=70)
    file.seek(0)
    return send_file(file, mimetype='image/jpeg')


app.run()