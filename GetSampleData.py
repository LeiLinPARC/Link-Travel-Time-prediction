import filterTaxiDataset

def sampleNodes(fileIn_Nodes,fileOut_Nodes,sampleMaxLatitude,sampleMinLatitude,sampleMaxLongitude,sampleMinLongitude):
    '''
    Move data from fileIn_Nodes to fileOut_Nodes, filtering out those data points, that are
    not in the sample window of min,max latitude and longitude.
    12.459091 41.902267
    '''
    print("Sampling Nodes")
    with open(fileIn_Nodes, "r") as fin, open(fileOut_Nodes, "w") as fout:
        for line in fin:
            longitude, latitude = line.strip().split(' ')
            latitude,longitude = float(latitude), float(longitude)
            if filterTaxiDataset.isWithinRange(latitude,longitude,sampleMaxLatitude,sampleMinLatitude,sampleMaxLongitude,sampleMinLongitude):
                fout.write(line)

def sampleEdges(fileIn_Edges,fileOut_Edges,sampleMaxLatitude,sampleMinLatitude,sampleMaxLongitude,sampleMinLongitude):
    '''
    Move data from fileIn_Edges to fileOut_Edges, filtering out those data points, that are
    not in the sample window of min,max latitude and longitude.
    12.4833041 41.8583686, 12.4809541 41.8583705
    ATTENTION: Longitude first!
    '''
    print("Sampling Edges")
    with open(fileIn_Edges, "r") as fin, open(fileOut_Edges, "w") as fout:
        for line in fin:
            point1, point2 = line.strip().split(',')
            longitude1, latitude1 = point1.strip().split(' ')
            latitude1,longitude1 = float(latitude1), float(longitude1)
            longitude2, latitude2 = point2.strip().split(' ')
            latitude2,longitude2 = float(latitude2), float(longitude2)
            if filterTaxiDataset.isWithinRange(latitude1,longitude1,sampleMaxLatitude,sampleMinLatitude,sampleMaxLongitude,sampleMinLongitude)  \
            and filterTaxiDataset.isWithinRange(latitude2,longitude2,sampleMaxLatitude,sampleMinLatitude,sampleMaxLongitude,sampleMinLongitude):
                fout.write(line)

def sampleTaxiData(fileIn_TaxiData,fileOut_TaxiData,sampleMaxLatitude,sampleMinLatitude,sampleMaxLongitude,sampleMinLongitude):
    '''
    Move data from fileIn_TaxiData to fileOut_taxiData, filtering out those data points, that are
    not in the sample window of min,max latitude and longitude.
    156;2014-02-01 00:00:00.739166+01;POINT(41.8836718276551 12.4877775603346)
    '''
    print("Sampling TaxiData")
    with open(fileIn_TaxiData, "r") as fin, open(fileOut_TaxiData, "w") as fout:
        for line in fin:
            driverID, timestamp, point = line.strip().split(';')
            latitude,longitude = point.strip().replace('POINT(','').replace(')','').split(' ')
            latitude,longitude = float(latitude), float(longitude)
            if filterTaxiDataset.isWithinRange(latitude,longitude,sampleMaxLatitude,sampleMinLatitude,sampleMaxLongitude,sampleMinLongitude):
                fout.write(line)


def GetSampleData(fileIn_TaxiData,fileIn_Edges,fileIn_Nodes,fileOut_TaxiData,fileOut_Edges,fileOut_Nodes,sampleMaxLatitude,sampleMinLatitude,sampleMaxLongitude,sampleMinLongitude):

    sampleTaxiData(fileIn_TaxiData,fileOut_TaxiData,sampleMaxLatitude,sampleMinLatitude,sampleMaxLongitude,sampleMinLongitude)
    sampleEdges(fileIn_Edges,fileOut_Edges,sampleMaxLatitude,sampleMinLatitude,sampleMaxLongitude,sampleMinLongitude)
    sampleNodes(fileIn_Nodes,fileOut_Nodes,sampleMaxLatitude,sampleMinLatitude,sampleMaxLongitude,sampleMinLongitude)


def main():
    '''
    This file should open exiting filteredTaxiData.txt, Edges.txt, osmnxNodes.txt
    and make new files sample_filteredTaxiData.txt, sample_Edges.txt, sample_osmnxNodes.txt
    and transfer data from existing files to new files, if data lies within selected window region.
    selected window region is the sample window chosen for which data is required (for testing)
    '''

    fileIn_TaxiData = "/home/aniket/Desktop/BTP/Travel Time Prediction/filteredTaxiData.txt"
    fileIn_Edges = "/home/aniket/Desktop/BTP/Travel Time Prediction/osmnx/Edges.txt"
    fileIn_Nodes = "/home/aniket/Desktop/BTP/Travel Time Prediction/osmnx/osmnxNodes.txt"

    fileOut_TaxiData = "/home/aniket/Desktop/BTP/Travel Time Prediction/sampleData/sample_filteredTaxiData.txt"
    fileOut_Edges = "/home/aniket/Desktop/BTP/Travel Time Prediction/sampleData/sample_Edges.txt"
    fileOut_Nodes = "/home/aniket/Desktop/BTP/Travel Time Prediction/sampleData/sample_osmnxNodes.txt"

    sampleMaxLatitude = 41.90323
    sampleMinLatitude = 41.90114
    sampleMaxLongitude = 12.48614 
    sampleMinLongitude = 12.47987

    GetSampleData(fileIn_TaxiData,fileIn_Edges,fileIn_Nodes,fileOut_TaxiData,fileOut_Edges,fileOut_Nodes,sampleMaxLatitude,sampleMinLatitude,sampleMaxLongitude,sampleMinLongitude)

    print("done")

if __name__=="__main__":
    main()


