import sys
import os
import struct
from struct import unpack, pack
import math

increase = float(sys.argv[1])

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
    newWidth = int(cof*bmp.width)
    newHeight = int(cof*bmp.height)
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
            newBmp.pixels[int(cof*i)][int(cof*j)] = bmp.pixels[i][j]
    return newBmp


def interpolate(p1, p2, dif):
    dif = int(dif)
    a = []
    for i in range(dif-1):
        coef = (i+1.0)/dif
        redComp = int(max(p1.red, p2.red) -math.fabs(p1.red-p2.red)*coef)
        greenComp = int(max(p1.green, p2.green) -math.fabs((p1.green-p2.green))*coef)
        blueComp = int(max(p1.blue, p2.blue) -math.fabs(p1.blue-p2.blue)*coef)
        a.append(PixelData(redComp, greenComp, blueComp ))
    return a

def fillImg(bmp, cof):
    for i in range(bmp.height):
        for j in range(int(bmp.width//cof)):
            if cof*(j+1) < bmp.width:
                temp = interpolate(bmp.pixels[i][int(cof*j)], bmp.pixels[i][int(cof*(j+1))], cof)
                for k in range(len(temp)):
                    bmp.pixels[i][int(j*cof)+k+1] = temp[k]

    for i in range(int(bmp.height//cof)):
        for j in range(bmp.width):
            if cof*(i+1) < bmp.height:
                temp = interpolate(bmp.pixels[int(i*cof)][j], bmp.pixels[int(cof*(i+1))][j], cof)
                for k in range(len(temp)):
                    bmp.pixels[int(i*cof)+k+1][j] = temp[k]

    for i in range(bmp.height):
        for j in range(bmp.width):
            if j+1 <= bmp.width:
                if bmp.pixels[i][j].red == 0 and bmp.pixels[i][j].green == 0 and bmp.pixels[i][j].blue == 0:
                    temp = interpolate(bmp.pixels[i][j-1], bmp.pixels[i][j+1], 1)
                    # print temp
                    for k in range(len(temp)):
                        bmp.pixels[i][j+k] = temp[k] 

def writeInBmp(bmp):
    padding = bmp.width%4
    resultFile = open(bmp.filename, 'w')
    resultFile.write(bmp.header)
    for row in bmp.pixels:
        for pixel in row:
            components = pixel.red, pixel.green, pixel.blue
            resultFile.write(''.join(map(chr, components)))
        for i in range(padding):
            resultFile.write(struct.pack('B', 0))

example = parseBMP("duck.bmp")
res = createNewBmp(example, increase)
fillImg(res,increase)
writeInBmp(res)
