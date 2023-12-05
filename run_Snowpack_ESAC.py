#!/usr/bin/python

import string, time, os, math, sys
#from station_Util import stationDict
#runSnowpack = 1
#
# example: run_Snowpack.py Lolo
#
inputDir = "/home/bran/SNOWPACK/input/"
stationList = ["CUES","Tioga","Rock_Creek"]

def main():
    dataArray = {}
    global dateTime,station,fHour
    for station in stationList:
        print (station)
        iniList = _getIniList(station)
        print("INI LIST: ", iniList)
        inPut = inputDir + station + "/" + station + ".smet"
        if os.path.exists(inPut):
            endTime = _FileEndTime(inPut)
            for file in iniList:
                print(file)
                ##buid string to run Snowpack
                ##  Change path below to location of "Snowpack-3.6.0/bin/snowpack" on your computer 
                snowpackCmd = "/home/bran/SNOWPACK/Snowpack-3.6.0-x86_64/data/usr/bin/snowpack -c " + \
                      "/home/bran/SNOWPACK/input/" + station + "/" + file + \
                      " -e " + endTime
                print (snowpackCmd,file.split(".")[0])
                os.system(snowpackCmd)
                outDir = "/home/bran/SNOWPACK/output/" + station + "/"
                localFileList = os.listdir(outDir)
                print("Here1: ", localFileList)
                for fileName in localFileList:
                    print(fileName)
                    if fileName.split(".")[1] == "haz":
                        outName = fileName.split(".")[0]
                print("Here2: ", outName)
                cpCmd = "cp " + outDir + outName + ".pro " + outDir + file.split(".")[0] + ".pro"
                os.system(cpCmd)

def _getIniList(station):
    iniList = []
    iniDir = "/home/bran/SNOWPACK/input/" + station + "/"
    #lsCmd = "ls " + iniDir + "*.ini"
    fileList = os.listdir(iniDir)
    for file in fileList:
        if file.split(".")[1] == "ini":
            iniList.append(file)
    return iniList
 
def _FileEndTime(inPut):
    file = inputDir + station + "/" + station + ".smet"
    inputText = open(file,'r')
    inData = inputText.read()
    inputText.close()
    lines = inData.split("\n")
#    print (lines[len(lines)-2])
    for line in lines:
        if line != "" and len(line.split()[0]) == 16:
            endTime = line.split()[0]
    #endTime = "2019-05-01T00:00"
    return endTime 

if __name__ == "__main__":
    main()
