import dataToGraph

def isWithinRange(latitude,longitude,max_suitable_latitude,min_suitable_latitude,max_suitable_longitude,min_suitable_longitude):
    return (latitude > min_suitable_latitude and latitude < max_suitable_latitude
        and longitude > min_suitable_longitude and longitude < max_suitable_longitude)

def filterDataset(fileIn, fileOut,max_suitable_latitude,min_suitable_latitude,max_suitable_longitude,min_suitable_longitude):
    '''
    From input file, reads all lines and only writes them to output file if the POINT(latitude,longitude)
    lies within range of max and min latitude and longitude values.
    A line looks like this:
    105;2014-02-01 00:00:21.033058+01;POINT(41.8971435606299 12.4729530904655)    
    '''
    with open(fileIn, "r") as fin, open(fileOut, "w") as fout:
        for line in fin:
            latitude, longitude = dataToGraph.lineToPoint(line)
            if isWithinRange(latitude,longitude,max_suitable_latitude,min_suitable_latitude,max_suitable_longitude,min_suitable_longitude):
                fout.write(line)

def main():
    fileIn = "/home/aniket/Desktop/BTP/Travel Time Prediction/Map backup/taxi_february.txt"
    fileOut = "/home/aniket/Desktop/BTP/Travel Time Prediction/filteredTaxiData.txt"
    # Run dataToGraph.py to get these values
    max_suitable_latitude = 41.9123147
    min_suitable_latitude = 41.7623147
    max_suitable_longitude = 12.6046319
    min_suitable_longitude = 12.4546319 

    filterDataset(fileIn,fileOut,max_suitable_latitude,min_suitable_latitude,max_suitable_longitude,min_suitable_longitude)
    print("done")

if __name__=="__main__":
    main()

