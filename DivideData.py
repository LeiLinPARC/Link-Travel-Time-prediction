import os

def lineTodriverID(line):
    '''
    156;2014-02-01 00:00:00.739166+01;POINT(41.8836718276551 12.4877775603346)   
    '''
    return int(line.strip().split(';')[0])

def driverIDtoPath(outputDir,driverID):
    return outputDir + '/driver_' + str(driverID) + '.txt'

def getDriverIDs(fileIn):
    '''
    Reads the fileIn, and returns set of driverIDs
    '''
    driverIDs = set()
    with open(fileIn,'r') as fin:
        for line in fin:
            driverIDs.add(int(lineTodriverID(line)))
    print("len(driverIDs) = " + str(len(driverIDs)))
    return driverIDs

def createFiles(fileIn,outputDir):
    '''
    Creates new files, one for each Driver
    '''
    driverIDs = getDriverIDs(fileIn)
    for driverID in driverIDs:
        filePath = driverIDtoPath(outputDir,driverID)
        open(filePath,'w').close()
    
def divideByDriver(fileIn,outputDir):
    '''
    Reads the fileIn, and makes 313 new files, one for each driver
    156;2014-02-01 00:00:00.739166+01;POINT(41.8836718276551 12.4877775603346)   
    '''
    createFiles(fileIn,outputDir)
    print("Files Created")
    with open(fileIn,'r') as fin:
        for line in fin:
            driverID = lineTodriverID(line)
            filePath = driverIDtoPath(outputDir,driverID)
            with open(filePath, 'a') as file:
                file.write(line)


def main():
    outputDir = '/home/aniket/Desktop/BTP/Travel Time Prediction/sampleData/TaxiData'
    fileIn = '/home/aniket/Desktop/BTP/Travel Time Prediction/sampleData/sample_filteredTaxiData2.txt'
    print("Starting")
    divideByDriver(fileIn,outputDir)
    print("done")

if __name__=="__main__":
    main()

