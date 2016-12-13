# Approximate RGB values for Visible Wavelengths (380nm to 780nm)
# Code based on FORTRAN implementation found here: http://www.physics.sfasu.edu/astro/color/spectra.html


def calcSpecColor(value, minimum, maximum):
    w = value * 400.0 / (maximum - minimum) + 380

    if w>=380.0 and w < 440.0:
        return [(-(w - 440.0) / (440.0 - 380.0)), 0., 1.]
    elif w>=440.0 and w < 490.0:
        return [0., ((w - 440.0) / (490.0 - 440.0)), 1.]
    elif w >= 490.0 and w < 510:
        return [0., 1., -(w - 510.0) / (510.0 - 490.0)]
    elif w >= 510.0 and w < 580.0:
        return [(w - 510.0) / (580.0 - 510.0), 1., 0.]
    elif w >= 580.0 and w < 645.0:
        return [1., (-(w - 645.0) / (645.0 - 580.0)), 0.]
    elif w >= 645.0 and w <= 780.0:
        return [1., 0., 0.]
    else:
        return [0.,0.,0.]



def testSpectra():
    from PIL import Image
    w = 1024
    h = 1024

    rgbdata = []

    for y in range(h):
        for x in range(w):
            rgb = calcSpecColor(float(x),0.0,1023.0)
            data = (int(rgb[0]*255.),int(rgb[1]*255.),int(rgb[2]*255.))
            rgbdata.append(data)

    im = Image.new("RGB", (w, h))
    im.putdata(rgbdata)
    im.save("output.png")




if __name__ == "__main__":
    testSpectra()