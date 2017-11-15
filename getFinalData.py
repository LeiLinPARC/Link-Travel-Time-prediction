import os
import dataToGraph
import dateutil
import dateutil.parser
from geopy.distance import vincenty as vin

def getEdgeFromLine(line):
    '''
    (41.9023473, 12.4836714, 41.902739, 12.4853082) Not in this format
    '''
    point1,point2 = line.strip().split(',')
    lon1 = float(point1.strip().split(' ')[0])
    lat1 = float(point1.strip().split(' ')[1])
    lon2 = float(point2.strip().split(' ')[0])
    lat2 = float(point2.strip().split(' ')[1])
    #print(str((lat1,lon1,lat2,lon2)))
    return (lat1,lon1,lat2,lon2)

def getEdges(fileEdges):
    '''
    Read edge file and return set of edges
    12.4825947 41.9026259, 12.4816662 41.9023843
    '''
    edges = set()
    with open(fileEdges,'r') as fin:
        for line in fin:
            edge = getEdgeFromLine(line)
            # print(str(edge))
            edges.add(edge)
    print(str(len(edges)) + " edges")
    return edges

def areSameEdge(osmEdge,edge,threshold=0.01):
    # print("osmEdge = " + str(osmEdge))    
    if vin((osmEdge[0],osmEdge[1]),(edge[0],edge[1])).miles < threshold and \
    vin((osmEdge[2],osmEdge[3]),(edge[2],edge[3])).miles < threshold:
        # print("areSameEdge: returning True")
        return True
    return False    

def isValidEdge(edges,edge):
    # print("len(edges) = " + str(len(edges)))
    for osmEdge in edges:
        if areSameEdge(osmEdge,edge):
            # print("isValidEdge: returning True")
            return True
    # print("isValidEdge: returning False")        
    return False

def getTimeFromLine(line):
    '''
    Returns timestamp from line
    156;2014-02-01 00:00:00.739166+01;POINT(41.8836718276551 12.4877775603346)   
    '''
    return dateutil.parser.parse(line.strip().split(';')[1].strip())

def getFinalData(InputDir,fileOut,fileEdges):
    '''
    Reads the fileIn, and makes 313 new files, one for each driver
    156;2014-02-01 00:00:00.739166+01;POINT(41.8836718276551 12.4877775603346)   
    '''
    edges = getEdges(fileEdges)
    filenames = os.listdir(InputDir)
    with open(fileOut,'w') as fout:
        for filename in filenames:
            fileIn = InputDir + '/' + filename
            print(filename)
            with open (fileIn,'r') as fin:
                lines = fin.readlines()
                for i in xrange(len(lines)-1):
                    [lat1,lon1] = dataToGraph.lineToPoint(lines[i])
                    [lat2,lon2] = dataToGraph.lineToPoint(lines[i+1])
                    if isValidEdge(edges,(lat1,lon1,lat2,lon2)):
                        timestamp1 = getTimeFromLine(lines[i])
                        timestamp2 = getTimeFromLine(lines[i+1])
                        duration = timestamp2 - timestamp1
                        durationInSeconds = duration.total_seconds()
                        outLine = lines[i].strip().split(';')[0] + ';'
                        outLine = outLine + str(lat1) + '_' + str(lon1)
                        outLine = outLine + ' ' + str(lat2) + '_' + str(lon2) + ';'
                        outLine = outLine + lines[i].strip().split(';')[1].strip() + ';'
                        outLine = outLine + str(durationInSeconds) + '\n'
                        fout.write(outLine)

def main():
    InputDir = '/home/aniket/Desktop/BTP/Travel Time Prediction/sampleData/filteredTaxiData'
    fileOut = '/home/aniket/Desktop/BTP/Travel Time Prediction/sampleData/finalData.txt'
    fileEdges = '/home/aniket/Desktop/BTP/Travel Time Prediction/sampleData/sample_Edges.txt'
    print("Starting")
    getFinalData(InputDir,fileOut,fileEdges)
    print("done")

if __name__=="__main__":
    main()