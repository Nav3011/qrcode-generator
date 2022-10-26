import cv2
import numpy as np
import random
from timeline import *
from constants import *
import time

MODULE_SIZE = 15
VERSION = 7
PADDING = 20
MODULE_COUNT = (4 * VERSION + 17)
HEIGHT = MODULE_COUNT * MODULE_SIZE + 2 * PADDING
WIDTH = MODULE_COUNT * MODULE_SIZE + 2 * PADDING
ORIGIN = (PADDING, PADDING)
END = (WIDTH - PADDING, HEIGHT - PADDING)
FINDER_PATTERN = [[1,1,1,1,1,1,1], [1,0,0,0,0,0,1], [1,0,1,1,1,0,1], [1,0,1,1,1,0,1], [1,0,1,1,1,0,1], [1,0,0,0,0,0,1], [1,1,1,1,1,1,1]]
ALIGNMENT_PATTERN = [[1,1,1,1,1], [1,0,0,0,1], [1,0,1,0,1], [1,0,0,0,1], [1,1,1,1,1]]
MODULE_COORDINATE_MAP = {}
COLOR_GREY = 200
BLANK_IMAGE = np.ones([WIDTH, HEIGHT, 3], dtype = np.uint8) * COLOR_GREY
FRAME_NAME = "qrcode"

def drawGrid():
    X_STARTS = []
    X_ENDS = []
    Y_STARTS = []
    Y_ENDS = []
    for module_count_index in range(MODULE_COUNT + 1):
        # print(module_count_index)
        # cv2.circle(BLANK_IMAGE, ( PADDING + module_count_index * MODULE_SIZE, PADDING), 2, (0, 0, 0), -1)
        # cv2.circle(BLANK_IMAGE, ( PADDING, PADDING + module_count_index * MODULE_SIZE), 2, (0, 0, 0), -1)
        X_STARTS.append((PADDING + module_count_index * MODULE_SIZE, PADDING))
        X_ENDS.append((PADDING + module_count_index * MODULE_SIZE, HEIGHT - PADDING))
        Y_STARTS.append((PADDING, PADDING + module_count_index * MODULE_SIZE))
        Y_ENDS.append((WIDTH - PADDING, PADDING + module_count_index * MODULE_SIZE))

    for i in range(MODULE_COUNT + 1):
        # draw the starts and end of X:
        # cv2.circle(BLANK_IMAGE, X_STARTS[i], 1, (0, 0, 0), -1)
        # cv2.circle(BLANK_IMAGE, X_ENDS[i], 1, (0, 0, 0), -1)
        # cv2.circle(BLANK_IMAGE, Y_STARTS[i], 1, (0, 0, 0), -1)
        # cv2.circle(BLANK_IMAGE, Y_ENDS[i], 1, (0, 0, 0), -1)

        cv2.line(BLANK_IMAGE, X_STARTS[i], X_ENDS[i], (0, 0, 0), 1)
        cv2.line(BLANK_IMAGE, Y_STARTS[i], Y_ENDS[i], (0, 0, 0), 1)

def createMapOfModuleCoordinate():
    result = {}
    for i in range(MODULE_COUNT):
        for j in range(MODULE_COUNT):
            result[i * MODULE_COUNT + j] = (j * MODULE_SIZE + PADDING, i * MODULE_SIZE + PADDING)

    return result

def createRandomMatrix():
    temp = np.ones((MODULE_COUNT, MODULE_COUNT), dtype=int) * 2
    # print(temp)
    return temp

def finderPatterns(image):
    finder_points = [(0,0), (0, MODULE_COUNT - 7), (MODULE_COUNT - 7, 0)]
    # time.sleep(1)
    for p in range(3):
        # time.sleep(1)
        POINT = finder_points[p]
        for i in range(len(FINDER_PATTERN)):
            for j in range(len(FINDER_PATTERN[i])):
                image[POINT[0] + j][POINT[1]+i] = FINDER_PATTERN[i][j]
    return image

def drawSeperator(image):
    # print(image[1])
    seperatorLength = 8
    # top-left finder
    for x in range(seperatorLength):
        # bottom
        image[seperatorLength - 1][x] = 0
        # right
        image[x][seperatorLength - 1] = 0

    #top-right finder
    for x in range(seperatorLength):
        # bottom
        image[seperatorLength - 1][MODULE_COUNT - seperatorLength + x] = 0
        # left
        image[x][MODULE_COUNT - seperatorLength] = 0

    #bottom-left finder
    for x in range(seperatorLength):
        # top
        image[MODULE_COUNT - seperatorLength][x] = 0
        # right
        image[MODULE_COUNT - seperatorLength + x][seperatorLength - 1] = 0

    return image 

def drawAlignmentPattern(image):
    ALIGNMENT_VALUES = ALIGNMENT_PATTERNS_COORDINATES[VERSION]
    ALIGNMENT_POINTS = []
    for p in ALIGNMENT_VALUES:
        for q in ALIGNMENT_VALUES:
            ALIGNMENT_POINTS.append((p, q))
    for t in ALIGNMENT_POINTS:
        CENTER_POINT = t
        START_EDGE = (CENTER_POINT[0] - 2, CENTER_POINT[1] - 2)
        positions = []
        for i in range(len(ALIGNMENT_PATTERN)):
            for j in range(len(ALIGNMENT_PATTERN[i])):
                positions.append(image[START_EDGE[0] + i][START_EDGE[1] + j])
        if(1 in positions or 0 in positions):
            pass
        else:
            for i in range(len(ALIGNMENT_PATTERN)):
                for j in range(len(ALIGNMENT_PATTERN[i])):
                    image[START_EDGE[0] + i][START_EDGE[1] + j] = ALIGNMENT_PATTERN[i][j]
    
    return image

def drawTimingPattern(image):
    # vertical timing pattern - 6th column & 8th row - 6th column & MODULE_COUNT - 9
    for i in range(8, MODULE_COUNT - 8):
        if(i%2 == 0):
            image[i][6] = 1
            image[6][i] = 1
        else:
            image[i][6] = 0
            image[6][i] = 0

    return image

def placeDarkModule(image):
    image[4 * VERSION + 9][8] = 1
    return image

def formatInfo(image):
    for i in range(9):
        # print(image[8][MODULE_COUNT - i - 1])
        if image[8][i] == 2:
            image[8][i] = 3
        if image[i][8] == 2:
            image[i][8] = 3
        if i < 8 and image[8][MODULE_COUNT - i - 1] == 2:
            image[8][MODULE_COUNT - i - 1] = 3
        if i < 8 and image[MODULE_COUNT - i - 1][8] == 2:
            image[MODULE_COUNT - i - 1][8] = 3
        # print(image[8][MODULE_COUNT - i - 1])
    return image

def versionInfo(image):
    topStart = MODULE_COUNT - 11
    for i in range(6):
        for j in range(3):
            image[topStart + j][i] = 3
            image[i][topStart + j] = 3
    return image


def showQRCode(IMAGE, NAME, QRARRAY):
    for i in range(len(QRARRAY)):
        # print(QRARRAY[i])
        for j in range(len(QRARRAY)):
            start = MODULE_COORDINATE_MAP[MODULE_COUNT * i + j]
            end = start[0] + MODULE_SIZE, start[1] + MODULE_SIZE
            if(QRARRAY[i][j] == 0):
                cv2.rectangle(IMAGE, start, end, (255, 255, 255), -1)
            elif(QRARRAY[i][j] == 1):
                cv2.rectangle(IMAGE, start, end, (0, 0, 0), -1)
            elif(QRARRAY[i][j] == 3):
                cv2.rectangle(IMAGE, start, end, (255, 0, 0), -1)
                # cv2.rectangle(name, MODULE_COORDINATE_MAP[])
    drawGrid()
    cv2.imshow(NAME, IMAGE)
    code = cv2.waitKey(0) & 0xFF
    return code

while True:
    # cv2.imshow(frame_name, blank_image)
    cv2.rectangle(BLANK_IMAGE, ORIGIN, END, (COLOR_GREY, COLOR_GREY, COLOR_GREY), -1)
    # cv2.setWindowProperty(frame_name, cv2.WND_PROP_TOPMOST, 1)
    # drawGrid()
    MODULE_COORDINATE_MAP = createMapOfModuleCoordinate()
    # print(MODULE_COORDINATE_MAP)
    BASE = createRandomMatrix()
    FINDER = finderPatterns(BASE)
    SEPERATOR = drawSeperator(FINDER)
    ALIGNMENT = drawAlignmentPattern(SEPERATOR)
    TIMIMG = drawTimingPattern(ALIGNMENT)
    DARKMODULE = placeDarkModule(TIMIMG)
    FORMATINFO = formatInfo(DARKMODULE)
    VERSIONINFO = FORMATINFO
    if VERSION >= 7:
        VERSIONINFO = versionInfo(VERSIONINFO)
    # finder_pattern = drawFinderPatterns(grid)
    # QRCODE = drawQRCode(MATRIX)
    k = showQRCode(BLANK_IMAGE, FRAME_NAME, FORMATINFO)
    cv2.setWindowProperty(FRAME_NAME, cv2.WND_PROP_TOPMOST, 1)
    if k == 27:
        saveImage(BLANK_IMAGE)
        cv2.destroyAllWindows()
        break
