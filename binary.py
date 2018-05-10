import sys
from struct import unpack, pack
import math

increase = 2
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
        self.header = []
        self.pixels = []

def parseBMP(fileName):
    bmp = BMPFile(fileName)
    openedBmp = open(fileName, 'rb')
    openedBmp.seek(18)
    bmp.width = unpack('I', openedBmp.read(4))[0]
    bmp.height = unpack('I', openedBmp.read(4))[0]
    bmp.realWidth = 3 * bmp.width + (4 - ((3 * bmp.width) % 4)) % 4;
    bmp.area = bmp.realWidth * bmp.height
    openedBmp.seek(54)
    print bmp.area
    # for k in range(bmp.height):
    #     bmp.pixels.append([])
    # for i in range(bmp.height):
    #     for j in range(bmp.realWidth):
    #         red = unpack('B', openedBmp.read(1))[0]
    #         green = unpack('B', openedBmp.read(1))[0]
    #         blue = unpack('B', openedBmp.read(1))[0]
    #         pixel = PixelData(red, green, blue)
    #         print red, green, blue
    #         bmp.pixels[i].append(pixel)
    return bmp

example = parseBMP("duck.bmp")
