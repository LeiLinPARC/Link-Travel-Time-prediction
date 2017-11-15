import matplotlib.pyplot as plt

def drawMap(fileEdgeList):
    '''
    Reads the edgeList and draws a map   
    12.4825947 41.9026259, 12.4816662 41.9023843
    '''
    count_edges = 0
    with open(fileEdgeList,'r') as fin:
        for line in fin:
            point1, point2 = line.strip().split(',')
            lon1 = float(point1.strip().split(' ')[0])
            lat1 = float(point1.strip().split(' ')[1])
            lon2 = float(point2.strip().split(' ')[0])
            lat2 = float(point2.strip().split(' ')[1])
            plt.scatter([lat1, lat2], [lon1, lon2], s=[0.01,0.01],c=['r','r'])
            plt.plot([lat1, lat2], [lon1, lon2], color='b', linestyle='-', linewidth=0.5)            
            plt.plot([lat1, lat2], [lon1, lon2],'ro')
            count_edges += 1
            if count_edges%1000 == 0:
                print("%d lines drawn"%count_edges)
                if count_edges == 5000:
                    break
        plt.show()            
        plt.savefig('roadMap.png',dpi=1000)

def main():
    fileEdgeList = "/home/aniket/Desktop/BTP/Travel Time Prediction/sampleData/sample_Edges.txt"
    drawMap(fileEdgeList)

if __name__=="__main__":
    main()

