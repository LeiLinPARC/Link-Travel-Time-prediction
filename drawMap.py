import matplotlib.pyplot as plt

def drawMap(fileEdgeList):
    '''
    Reads the edgeList and draws a map   
    '''
    count_edges = 0
    with open(fileEdgeList,'r') as fin:
        for line in fin:
            point1, point2, weight = line.strip().split(',')
            lat1 = float(point1.split('_')[0])
            lon1 = float(point1.split('_')[1])
            lat2 = float(point2.split('_')[0])
            lon2 = float(point2.split('_')[1])
            plt.scatter([lat1, lat2], [lon1, lon2], s=[0.01,0.01],c=['r','r'])
            plt.plot([lat1, lat2], [lon1, lon2], color='b', linestyle='-', linewidth=0.5)
            count_edges += 1
            if count_edges%1000 == 0:
                print("%d lines drawn"%count_edges)
                if count_edges == 5000:
                    break
        plt.savefig('roadMap.png',dpi=1000)

def main():
    fileEdgeList = "/home/aniket/Desktop/BTP/Travel Time Prediction/output/Rome.edgelist"
    drawMap(fileEdgeList)

if __name__=="__main__":
    main()

