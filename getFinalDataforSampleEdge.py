import pandas as pd

def filterDataset(fileIn,fileOut,sampleEdge):
    '''
    From input file, reads all lines and only writes them to output file if 
    edge is same as sampleEdge
    A line looks like this:
    96;41.902347_12.483671 41.902739_12.485308;2014-02-13 19:12:46.678922+01;70.865886    
    '''
    with open(fileIn, "r") as fin, open(fileOut, "w") as fout:
        fout.write("timestamp;duration\n")
        for line in fin:
            edge = line.strip().split(';')[1]
            if edge == sampleEdge:
                time = line.split(';')[-2]
                duration = line.split(';')[-1]
                fout.write(time + ';' + duration)

def sortTimestamps(fileOut,fileOutSorted):
    '''
    Read csv files in pandas dataframes, Sort on basis on Time stamps, write back to file
    '''
    df = pd.read_csv(fileOut,parse_dates=['timestamp'],sep=';')
    df = df.sort_values(by='timestamp')
    df.to_csv(fileOutSorted,index=False)

def main():
    fileIn = '/home/aniket/Desktop/BTP/Travel Time Prediction/sampleData/finalData.txt'
    fileOut = '/home/aniket/Desktop/BTP/Travel Time Prediction/sampleData/finalDataForSampleEdge.csv'
    fileOutSorted = '/home/aniket/Desktop/BTP/Travel Time Prediction/sampleData/finalDataForSampleEdgeSorted.csv'
    sampleEdge = '41.902347_12.483671 41.902739_12.485308'

    filterDataset(fileIn,fileOut,sampleEdge)
    sortTimestamps(fileOut,fileOutSorted)
    print("done")

if __name__=="__main__":
    main()

