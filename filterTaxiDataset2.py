from geopy.distance import vincenty as vin
import dataToGraph

def GetNodes(fileNodes):
    '''
    Reads osmnxNodes.txt lines of the form
    12.459091 41.902267
    and adds nodes to the nodes (set)
    '''
    nodes = set()
    with open(fileNodes, "r") as fin:
        for line in fin:
            [longitude, latitude] = line.strip().split(' ')
            nodes.add((float(latitude),float(longitude)))
    print("%d nodes" % len(nodes)) 
    return nodes        


def closestNode(node,nodes,threshold):
    '''
    finds distance of point(node) with each node of OSM graph.
    If any node is closer than threshold, returns that node,
    Else returns None
    '''
    #fixme : MAKE IT FASTER!!
    closest_node = None
    closest_node_dist = -1

    for osmNode in nodes:
        dist = vin(node,osmNode).miles
        if dist < threshold:
            if closest_node_dist == -1 or dist < closest_node_dist:
                closest_node_dist = dist
                closest_node = osmNode            
    return closest_node        


def replacePointByOSMnode(line,closest_node):
    '''
    Replaces latitude and longitude of original line in dataset, with
    closest mapped point in OSM graph's latitude and longitude
    '''
    driverID, timeStamp, point = line.split(';')
    #156;2014-02-01 00:00:00.739166+01;POINT(41.8836718276551 12.4877775603346)
    return driverID+";"+timeStamp+";"+"POINT("+str(closest_node[0])+" "+str(closest_node[1])+")\n"

def filterDataset(fileIn, fileOut,fileNodes,threshold):
    '''
    Reads filteredTaxiData.txt and filters out lines that are farther away from every node in OSM graph ,
    by a threshold value (0.1 mile). A data entry will be kept if the distance of point is less than this threshold,
    from any node in OSM graph
    '''
    nodes = GetNodes(fileNodes)
    count_lines_written = 0
    with open(fileIn, "r") as fin, open(fileOut, "w") as fout:
        for line in fin:
            [latitude,longitude] = dataToGraph.lineToPoint(line)
            closest_node = closestNode((float(latitude),float(longitude)),nodes,threshold)
            if closest_node is not None:
                line = replacePointByOSMnode(line,closest_node)
                fout.write(line)
                count_lines_written += 1
                print("%d lines written" % count_lines_written)

def main():
    #Run this script after running filterTaxiDataset.py 
    fileIn = "/home/aniket/Desktop/BTP/Travel Time Prediction/sampleData/sample_filteredTaxiData.txt"
    fileOut = "/home/aniket/Desktop/BTP/Travel Time Prediction/sampleData/sample_filteredTaxiData_2.txt" #Gets rid of intermediate values
    fileNodes = "/home/aniket/Desktop/BTP/Travel Time Prediction/sampleData/sample_osmnxNodes.txt"
    threshold = 0.005 #mile

    filterDataset(fileIn,fileOut,fileNodes,threshold)
    print("done")

if __name__=="__main__":
    main()

