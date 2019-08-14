#!/usr/bin/env python3

import csv, sys, os, shutil
from statistics import median
from statistics import mean
import math

#import own functions 
import fily, gets, build

#Retrieve path of files from the arguments passed to the script
pathToCSVFile = "../04-CSV/Extracted.csv"
#pathToCSVFile = str(sys.argv[1])            #CSV  input file 

#Extract id-coordinates as a list
iCoord = gets.getCommaFile(pathToCSVFile,col=3)
iCoord.remove("id")

INDEXES = build.setColumn(iCoord)
fily.touchFile("../04-CSV/azimuthFile.tmp")
fily.appendFile("id" "," +\
            "AZ" + "," + \
            "X" + "," + \
            "Y" + "," + \
            "Z" + "\n",\
            "../04-CSV/azimuthFile.tmp",\
            True)

for iINDEX in INDEXES[0:100]:
    # Field names for the different attributes of the points given on the
    # CSV inputFile
    xColumnID = 0                       # X-Coordinate
    yColumnID = 1                       # Y-Coordinate
    zColumnID = 2                       # Z-Coordinate

    pathToTempFile = "../04-CSV/File_.tmp"
    commandExtract = "grep \"," + \
        str(iINDEX) + \
        "$\" " + pathToCSVFile + \
        " > " + pathToTempFile
    
    os.system(commandExtract)

    xCoord = gets.getCommaFile(pathToTempFile,col=xColumnID)
    yCoord = gets.getCommaFile(pathToTempFile,col=yColumnID)
    zCoord = gets.getCommaFile(pathToTempFile,col=zColumnID)

    xFloats = [float(i) for i in xCoord]
    yFloats = [float(i) for i in yCoord]
    zFloats = [float(i) for i in zCoord]

    whX1 = xFloats.index(max(xFloats))
    whX2 = xFloats.index(min(xFloats))
    
    whY1 = xFloats.index(max(xFloats))
    whY2 = xFloats.index(min(xFloats))
    
    devXX = xFloats[whX1] - xFloats[whX2]   # maxX - minX
    devYY = yFloats[whY1] - yFloats[whY2]   # maxY - minY
    
    devXY = yFloats[whX1] - mean(xFloats)
    
    if devXX/devYY > 1.5:
        xMean = median(xFloats)
        yMean = median(yFloats) + (max(xFloats) - min(xFloats))
    elif devYY/devXX > 1.5:
        xMean = median(xFloats) + (max(yFloats) - min(yFloats))
        yMean = median(yFloats)
    elif devXY < 0:
        xMean = median(xFloats) + (max(yFloats) - min(yFloats))/2
        yMean = median(yFloats) - (max(xFloats) - min(xFloats))/2
    elif devXY > 0:
        xMean = median(xFloats) + (max(yFloats) - min(yFloats))/2
        yMean = median(yFloats) + (max(xFloats) - min(xFloats))/2
    else:
        xMean = median(xFloats) 
        yMean = median(yFloats) 


    # if devXX/devYY > 1.5:
    #     xMean = mean(xFloats)
    #     yMean = mean(yFloats) + (max(xFloats) - min(xFloats))
    # elif devYY/devXX > 1.5:
    #     xMean = mean(xFloats) + (max(yFloats) - min(yFloats))
    #     yMean = mean(yFloats)
    # elif devXY < 0:
    #     xMean = mean(xFloats) + (max(yFloats) - min(yFloats))/2
    #     yMean = mean(yFloats) - (max(xFloats) - min(xFloats))/2
    # elif devXY > 0:
    #     xMean = mean(xFloats) + (max(yFloats) - min(yFloats))/2
    #     yMean = mean(yFloats) + (max(xFloats) - min(xFloats))/2
    # else:
    #     xMean = mean(xFloats) 
    #     yMean = mean(yFloats) 


    # xMean = mean(xFloats) 
    # yMean = mean(yFloats) 
    
    #azimuth = [(xFloats[i]-xMean)+(yFloats[i]-yMean) for i in range(len(xCoord))]
    azimuth = [math.degrees(math.atan2(yFloats[i]-yMean,xFloats[i]-xMean)) for i in range(len(xCoord))]
    #azimuth = [((xFloats[i]-xMean)/abs(xFloats[i]-xMean))*((yFloats[i]-yMean)**2 + (xFloats[i]-xMean)**2) for i in range(len(xCoord))]
    #azimuth = [(yFloats[i]-yMean)**2 + (xFloats[i]-xMean)**2 * math.cos((math.atan2(yFloats[i]-yMean,xFloats[i]-xMean))) for i in range(len(xCoord))]

    for i in range(len(xCoord)):
        fily.appendFile(str(iINDEX) + "," +\
            "{:.4f}".format(azimuth[i]) + "," + \
            "{:.2f}".format(xFloats[i]) + "," + \
            "{:.2f}".format(yFloats[i]) + "," + \
            "{:.2f}".format(zFloats[i]) + "\n",\
            "../04-CSV/azimuthFile.tmp",\
            True)

    fily.appendFile(str(iINDEX) + "," +\
            "{:.4f}".format(0) + "," + \
            "{:.2f}".format(xMean) + "," + \
            "{:.2f}".format(yMean) + "," + \
            "{:.2f}".format(0) + "\n",\
            "../04-CSV/azimuthFile.tmp",\
            True)


print(str(INDEXES))