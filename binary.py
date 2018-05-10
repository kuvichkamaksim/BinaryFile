import sys
from struct import unpack, pack
import math

increase = 3
resultFile = open("duck"+str(increase)+".bmp", 'w')

class PixelData:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

class BMPFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.height = 0
        self.width = 0
        self.realWidth = 0
        self.area = 0
        self.header = None
        self.pixels = []

def parseBMP(fileName):
    bmp = BMPFile(fileName)
    with open(fileName, 'rb') as openedBmp:
        bmp.header = openedBmp.read(54)
        openedBmp.seek(18)
        bmp.width = unpack('I', openedBmp.read(4))[0]
        bmp.height = unpack('I', openedBmp.read(4))[0]
        bmp.realWidth = 3 * bmp.width + (4 - ((3 * bmp.width) % 4)) % 4;
        bmp.area = bmp.realWidth * bmp.height
        openedBmp.seek(54)
        bmp.pixels = [[PixelData(*map(ord, openedBmp.read(3)))
                         for _ in range(bmp.width)]
                            for _ in range(bmp.height)]
    return bmp


def createNewBmp(bmp, cof):
    newWidth = cof*bmp.width
    newHeight = cof*bmp.height
    fileName = "result"+str(cof)+".bmp"
    newBmp = BMPFile(fileName)

    newBmp.width = newWidth
    newBmp.height = newHeight

    newHead = bmp.header[:18]
    newHead += pack('I', newWidth)
    newHead += pack('I', newHeight)
    newHead += bmp.header[26:]
    newBmp.header = newHead

    for k in range(newBmp.height):
        newBmp.pixels.append([])
    for k in range(newBmp.height):
        for q in range(newBmp.width):
            newBmp.pixels[k].append(PixelData(0,0,0))
    for i in range(bmp.height):
        for j in range(bmp.width):
            newBmp.pixels[cof*i][cof*j] = bmp.pixels[i][j]
    return newBmp


def interpolate(p1, p2, dif):
    a = []
    for i in range(dif-1):
        coef = (i+1.0)/dif
        # print coef, i, dif
        redComp = int(min(p1.red, p2.red) +math.fabs(p1.red-p2.red)*coef)
        greenComp = int(min(p1.green, p2.green) +math.fabs(p1.green-p2.green)*coef)
        blueComp = int(min(p1.blue, p2.blue) +math.fabs(p1.blue-p2.blue)*coef)
        # print redComp, greenComp, blueComp
        a.append(PixelData(redComp, greenComp, blueComp ))
    return a

def fillImg(bmp, cof):
    for i in range(bmp.height):
        for j in range(bmp.width//cof):
            if cof*(j+1) < bmp.width:
                temp = interpolate(bmp.pixels[i][cof*j], bmp.pixels[i][cof*(j+1)], cof)
                for k in range(len(temp)):
                    bmp.pixels[i][j*cof+k+1] = temp[k]

    for i in range(bmp.height//cof):
        for j in range(bmp.width):
            if cof*(i+1) < bmp.height:
                temp = interpolate(bmp.pixels[i*cof][j], bmp.pixels[cof*(i+1)][j], cof)
                for k in range(len(temp)):
                    bmp.pixels[i*cof+k+1][j] = temp[k]

def writeInBmp(bmp):
    resultFile = open(bmp.filename, 'w')
    resultFile.write(bmp.header)
    # resultFile.write(map(chr, (p.red, p.green, p.blue))
    #                  for p in row for row in bmp.pixels)
    for row in bmp.pixels:
        for pixel in row:
            components = pixel.red, pixel.green, pixel.blue
            resultFile.write(''.join(map(chr, components)))

example = parseBMP("duck.bmp")
res = createNewBmp(example, increase)
fillImg(res,increase)
writeInBmp(res)
