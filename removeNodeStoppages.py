import os
import dataToGraph

def RemoveStoppage(fileIn,fileOut):
    prevlat=0
    prevlon=0
    with open(fileIn,"r") as fin, open(fileOut, "w") as fout:
        for line in fin:
            latitude, longitude = dataToGraph.lineToPoint(line)
            if(latitude==prevlat and longitude==prevlon):
                continue
            else:
                prevlat=latitude
                prevlon=longitude
                fout.writelines(line)
                

def main():
    dirIn = '/home/aniket/Desktop/BTP/Travel Time Prediction/sampleData/TaxiData'
    dirOut = '/home/aniket/Desktop/BTP/Travel Time Prediction/sampleData/filteredTaxiData'
    for root, dirs, filenames in os.walk(dirIn):
        for f in filenames:
            fileIn = dirIn + '/' + f
            fileOut = dirOut + '/' + f
            RemoveStoppage(fileIn,fileOut)
            
    print("done")

if __name__=="__main__":
    main()