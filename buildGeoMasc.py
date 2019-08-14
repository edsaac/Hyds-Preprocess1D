#!/usr/bin/env python3

import csv, sys, os, shutil
import math

#import own functions 
import fily, gets, build

#Retrieve path of files from the arguments passed to the script
pathToCSVFile = "../06-XSections/Nodes.csv"
#pathToCSVFile = str(sys.argv[1])            #CSV  input file 

# Field names for the different attributes of the points given on the
#  CSV inputFile
iLinColID = "AdMapKey"                # Line Identification
iLinColWh = gets.getColumn(iLinColID,pathToCSVFile)

#Extract id-coordinates as a list
iCoord = gets.getCommaFile(pathToCSVFile,col=iLinColWh)
iCoord.remove(iLinColID)
INDEXES = build.setColumn(iCoord)

iFloats = [float(i) for i in INDEXES]           #Save as floats
print(iFloats)

#Abscisae constructor
firstAbs = 0
lenghtAbs = 100
abscisae = [firstAbs + x*lenghtAbs for x in range(len(INDEXES))]
k = 0

fily.resetFile("../06-XSections/GEO_.tmp","T3S")

for iINDEX in INDEXES:
    
    pathToTempFile = "../06-XSections/File_.tmp"
    commandExtract = "grep ^" + \
        str(iINDEX) + \
        ", " + pathToCSVFile + \
        " > " + pathToTempFile
    
    os.system(commandExtract)

    #Extract orders as a list
    orderCol = gets.getCommaFile(pathToTempFile,col=1)
    ORDERS = build.setColumn(orderCol)
    oInts = [int(i) for i in ORDERS]
    oInts.sort()

    stationX = gets.getCommaFile(pathToTempFile,col=4)
    flotionX = [float(i) for i in stationX]  
    stationZ = gets.getCommaFile(pathToTempFile,col=6)
    flotionZ = [float(i) for i in stationZ]  

    
    fily.appendFile("PROFIL Bief_1 P" + iINDEX + " " + str(abscisae[k]) + "\n", "../06-XSections/GEO_.tmp", True)

    for i in oInts:
        fily.appendFile(\
        "{:.2f}".format(flotionX[i]) + " " + \
        "{:.2f}".format(flotionZ[i]) + " B\n" , \
        "../06-XSections/GEO_.tmp",\
        True)
    k+=1