from geopy.distance import vincenty as vin
import dataToGraph
import numpy as np
from lshash import LSHash

def CheckIfValidNode(node,fileNodes):
	#Not needed anymore, Was used to verify if results are correct
	nodes = GetNodes(fileNodes)
	for osmnode in nodes:
		if osmnode == node:
			return True
	return False

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
    # Dimension of our vector space
    lsh = LSHash(hash_size=10, input_dim=2)

    nodes = GetNodes(fileNodes)
    for node in nodes:
        v = np.array(node,dtype=float)
        lsh.index(v)
    bunch = []
    bunch_size = 5000
    count_lines_read = 0
    count_lines_written = 0
    with open(fileIn, "r") as fin, open(fileOut, "w") as fout:
        for line in fin:
            [latitude,longitude] = dataToGraph.lineToPoint(line)
            query = np.array((latitude,longitude),dtype=float)
            result = lsh.query(query,num_results=1)
            closest_node = result[0][0]
            count_lines_read += 1
            if vin((latitude,longitude),closest_node).miles < threshold:
                line = replacePointByOSMnode(line,closest_node)
                bunch.append(line)
                if len(bunch) == bunch_size:
                    fout.writelines(bunch)
                    count_lines_written += len(bunch)
                    bunch = []
                    if(count_lines_written % 10 == 0):
                	    print("%d written / %d read" % (count_lines_written,count_lines_read))
        fout.writelines(bunch)
        count_lines_written += len(bunch)
        print("%d lines written" % count_lines_written)

def main():
    #Run this script after running filterTaxiDataset.py 
    fileIn = "/home/aniket/Desktop/BTP/Travel Time Prediction/sampleData/sample_filteredTaxiData.txt"
    fileOut = "/home/aniket/Desktop/BTP/Travel Time Prediction/sampleData/sample_filteredTaxiData2.txt" #Gets rid of intermediate values
    fileNodes = "/home/aniket/Desktop/BTP/Travel Time Prediction/sampleData/sample_osmnxNodes.txt"
    threshold = 0.05 #mile 

    filterDataset(fileIn,fileOut,fileNodes,threshold)
    print("done")

if __name__=="__main__":
    main()


