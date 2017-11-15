## ===COMMENT=============================================================================
# 1st Run osm2roadGraph_Part1.py with the raw .osm filefile name INPUT which will create 
# intermediate .json file as OUTPUT with distance as edge weight followed by which 
# run this osm2roadGraph_Part2.py file with those .json as INPUT which will 
# fially create the road graph with NetworkX
##========================================================================================

import networkx as nx
import json
import sys
import matplotlib.pyplot as plt

def main():
    
#    filename = "../output/tograph_withdist_manhattan.json"
    cityname = "Rome"
    filename = '/home/aniket/Desktop/BTP/Travel Time Prediction/output/tograph_withdist_'+cityname+'.json'

    with open(filename,'r') as fin:
        roadnet = json.load(fin)

    roadnodes = []
    for k in roadnet.keys():
        roadnodes.append(k)
        for n in roadnet[k]:
            roadnodes.append(n[0])
    
    nodeset = list(set(roadnodes))
    
    DG=nx.DiGraph()
    DG.add_nodes_from(nodeset)

    cnt = 1
    for k in roadnet.keys():
#        print k
        for n in roadnet[k]:
            DG.add_edge(k,n[0],weight=n[1])


    for n,nbr in DG.adjacency_iter():
        for nbr,eattr in nbr.items():
            wt = eattr['weight']
#            print('(%s, %s, %s)' % (n,nbr,str(wt)))
            cnt = cnt + 1

#        print

    xx = [comp for comp in nx.strongly_connected_component_subgraphs(DG)]
    comp_sz = [comp.order() for comp in xx]

    '''
    for comp in xx:
        if comp.order()==818:
            for s in  comp.nodes():
                print s
            exit


    '''
    mynodes = DG.nodes();
    with open('/home/aniket/Desktop/BTP/Travel Time Prediction/output/rome_nodes.txt','w') as fout:
        for n in mynodes:
            fout.write(n+"\n")

    nx.write_edgelist(DG,'/home/aniket/Desktop/BTP/Travel Time Prediction/output/'+cityname+'.edgelist.gz',delimiter=",",data=True)
    NG = nx.read_edgelist('/home/aniket/Desktop/BTP/Travel Time Prediction/output/'+cityname+'.edgelist.gz',create_using=nx.DiGraph(),delimiter = ",",nodetype=str, data=True)

    scnt=1
    for n,nbr in NG.adjacency_iter():
        for nbr,eattr in nbr.items():
            wt = eattr['weight']
#            print('(%s, %s, %s)' % (n,nbr,str(wt)))
            scnt = scnt + 1
#        print

#    print comp_sz
    print len(nodeset)
#    print sum(comp_sz)
    print cnt
    print scnt
    print "done"
    pos = nx.spring_layout(DG)
    nx.draw_networkx_nodes(DG,pos)
    nx.draw_networkx_edges(DG,pos)
    plt.show()
    

if __name__=="__main__":
    main()

