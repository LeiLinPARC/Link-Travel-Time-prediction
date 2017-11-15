#===============================COMMENT===========================================
# To create a road map from raw .osm file 
# FIRST run this script osm2roadGraph_Part1.py
# INPUT: = raw .osm file name
# OUTPUT: = .json files with distance as edge weight
# SECOND to complete final roadmap generation  run osm2roadGraph_Part2.py
# INPUT:= .json file which is ouput of this script
# OUTPUT:= roadmap generated from .json using NetworX
#=================================================================================

import xml.sax
import copy
import networkx 
import json
from geopy.distance import vincenty as vin
import sys
#highway_cat = 'motorway|trunk|primary|secondary|tertiary|road|residential|service|motorway_link|trunk_link|primary_link|secondary_link|teriary_link'
def read_osm(filename_or_stream, only_roads=True):
    """Read graph in OSM format from file specified by name or by stream object.

    Parameters
    ----------
    filename_or_stream : filename or stream object

    Returns
    -------
    G : Graph

    Examples
    --------
    G=nx.read_osm(nx.download_osm(-122.33,47.60,-122.31,47.61))
    plot([G.node[n]['data'].lat for n in G], [G.node[n]['data'].lon for n in G], ',')

    """
    osm = OSM(filename_or_stream)
    G = networkx.DiGraph()
 
    highwaytags = ['primary','secondary','tertiary','unclassified','road','living_street','residential']
    for w in osm.ways.itervalues():
        if only_roads and 'highway' not in w.tags:
            continue

        if w.tags['highway'] in highwaytags or w.tags['highway'] == 'motorway':
            G.add_path(w.nds, id=w.id, highway = w.tags['highway'])#{str(k): type(v) for k,v in w.tags.items()})
       
        

        if 'oneway' not in w.tags and  w.tags['highway'] in highwaytags:
            G.add_path(reversed(w.nds), id=w.id, highway = w.tags['highway'])

        elif 'oneway' in w.tags and w.tags['oneway'] != 'yes' and w.tags['oneway'] != '-1' and  w.tags['highway'] in highwaytags:
            G.add_path(reversed(w.nds), id=w.id, highway = w.tags['highway'])

        
    for n_id in G.nodes_iter():
        n = osm.nodes[n_id]
        G.node[n_id] = dict(nodeid=n.id,lon=n.lon,lat=n.lat)
    return G
        
    
class Node:
    def __init__(self, id, lon, lat):
        self.id = id
        self.lon = lon
        self.lat = lat
        self.tags = {}
        
class Way:
    def __init__(self, id, osm):
        self.osm = osm
        self.id = id
        self.nds = []
        self.tags = {}
        
    def split(self, dividers):
        # slice the node-array using this nifty recursive function
        def slice_array(ar, dividers):
            for i in range(1,len(ar)-1):
                try:  
                    if dividers[ar[i]]>1:
                    #print "slice at %s"%ar[i]
                        left = ar[:i+1]
                        right = ar[i:]
                    
                        rightsliced = slice_array(right, dividers)
                    
                        return [left]+rightsliced
                except:
                    pass
            return [ar]
            


        slices = slice_array(self.nds, dividers)
        
        # create a way object for each node-array slice
        ret = []
        i=0
        for slice in slices:
            littleway = copy.copy( self )
            littleway.id += "-%d"%i
            littleway.nds = slice
            ret.append( littleway )
            i += 1
            
        return ret
        
        
 
class OSM:
    def __init__(self, filename_or_stream):
        """ File can be either a filename or stream/file object."""
        nodes = {}
        ways = {}
        
        superself = self
        
        class OSMHandler(xml.sax.ContentHandler):
            @classmethod
            def setDocumentLocator(self,loc):
                pass
            
            @classmethod
            def startDocument(self):
                pass
                
            @classmethod
            def endDocument(self):
                pass
                
            @classmethod
            def startElement(self, name, attrs):
                if name=='node':
                    self.currElem = Node(attrs['id'], float(attrs['lon']), float(attrs['lat']))
                elif name=='way':
                    self.currElem = Way(attrs['id'], superself)
                elif name=='tag':
                    self.currElem.tags[attrs['k']] = attrs['v']
                elif name=='nd':
                    self.currElem.nds.append( attrs['ref'] )
                
            @classmethod
            def endElement(self,name):
                if name=='node':
                    nodes[self.currElem.id] = self.currElem
                elif name=='way':
                    ways[self.currElem.id] = self.currElem
                
            @classmethod
            def characters(self, chars):
                pass
 
        xml.sax.parse(filename_or_stream, OSMHandler)
        
        self.nodes = nodes
        self.ways = ways
        #"""   
        #count times each node is used
        node_histogram = dict.fromkeys( self.nodes.keys(), 0 )
        for way in self.ways.values():
            if len(way.nds) < 2:       #if a way has only one node, delete it out of the osm collection
                del self.ways[way.id]
            else:
                for node in way.nds:
                    node_histogram[node] += 1


        #use that histogram to split all ways, replacing the member set of ways
        new_ways = {}
        for id, way in self.ways.iteritems():
            split_ways = way.split(node_histogram)
            for split_way in split_ways:
                new_ways[split_way.id] = split_way
        self.ways = new_ways
        #"""

def main():

#    fname = "../dataset/map_final.osm"
#    fname = "../dataset/map_manhattan.osm"
    cityname = "Rome"
    fname = '/home/aniket/Desktop/BTP/Travel Time Prediction/map'
#    fname = "../dataset/manhattan_baseline.osm"

    G=read_osm(fname)

    #[G.node[n]['data'].lat for n in G]    

    cnt = 1
    
    print "nodes = %d" % len(G.nodes())
    print "edges = %d" % len(G.edges())


    roadnodes = {}
    roadgraph = {}
    rdnd = {}
    
    ndcnt = 0

    for n in G:
        ndcnt = ndcnt + 1
        roadnodes[str(G.node[n]['nodeid'])]=dict(lon=str(G.node[n]['lon']),lat=str(G.node[n]['lat']))
        #roadnodes[str(cnt)]=dict(lon=str(G.node[n]['lon']),lat=str(G.node[n]['lat']))
        
        #print "==="    

    s = []
    snt = 1
    fromgraph = {}
    tograph = {}
    tographwithdist = {}
    edgegraph = {}
    with open("/home/aniket/Desktop/BTP/Travel Time Prediction/output/"+cityname+".txt",'w') as fout:
        # from_loc+to_loc  
        for e in G.edges():
            line = roadnodes[str(e[0])]['lat']+","+roadnodes[str(e[0])]['lon']+","+roadnodes[str(e[1])]['lat']+","+roadnodes[str(e[1])]['lon'] 
            fromnode =  roadnodes[str(e[0])]['lat']+"_"+roadnodes[str(e[0])]['lon']
            tonode = roadnodes[str(e[1])]['lat']+"_"+roadnodes[str(e[1])]['lon']
            
            s1 = (float(roadnodes[str(e[0])]['lat']),float(roadnodes[str(e[0])]['lon']))
            d1 = (float(roadnodes[str(e[1])]['lat']),float(roadnodes[str(e[1])]['lon']))
            dist = vin(s1,d1).miles
            

            if tonode in fromgraph.keys():
                fromgraph[tonode].append(fromnode)
            else:
                fromgraph[tonode] = []
                fromgraph[tonode].append(fromnode)

            if fromnode in tograph.keys():
                tograph[fromnode].append(tonode)
            else:
                tograph[fromnode] = []
                tograph[fromnode].append(tonode)

            if fromnode in tographwithdist.keys():
                tographwithdist[fromnode].append((tonode,dist))
            else:
                tographwithdist[fromnode] = []
                tographwithdist[fromnode].append((tonode,dist))

            edgekey = fromnode+"_"+tonode
            if edgekey in edgegraph.keys():
                continue
            else:
                edgegraph[edgekey] = 1
                fout.write(line+"\n")
#                print "e: "+str(snt)
                snt = snt + 1

    fromgraphjson = '/home/aniket/Desktop/BTP/Travel Time Prediction/output/fromgraph_'+cityname+'.json'
    tographjson = '/home/aniket/Desktop/BTP/Travel Time Prediction/output/tograph_'+cityname+'.json'
    edgegraphjson = '/home/aniket/Desktop/BTP/Travel Time Prediction/output/edgegraph_'+cityname+'.json'


    with open(fromgraphjson,'w') as ffrom,open(tographjson,'w') as fto,open(edgegraphjson,'w') as fedge:
        json.dump(tograph,fto)
        json.dump(fromgraph,ffrom)
        json.dump(edgegraph,fedge)

    tographWithDist = '/home/aniket/Desktop/BTP/Travel Time Prediction/output/tograph_withdist_'+cityname+'.json'

    with open(tographWithDist,'w') as fout:
        json.dump(tographwithdist,fout)


    cnt = 1
    for n in G:
        rdnd[str(cnt)]=dict(lon=str(G.node[n]['lon']),lat=str(G.node[n]['lat']))
        #roadnodes[str(cnt)]=dict(lon=str(G.node[n]['lon']),lat=str(G.node[n]['lat']))
        cnt = cnt+1
#        print "n: "+str(cnt)
            

    roadnodesfile = '/home/aniket/Desktop/BTP/Travel Time Prediction/output/roadnodes_'+cityname+'.json'
    with open(roadnodesfile,'w') as fout:
        json.dump(rdnd,fout)
    
    nndset = []
    ecnt = 1

    edgegraphB4fname = '/home/aniket/Desktop/BTP/Travel Time Prediction/output/edgegraph_B4'+cityname+'.json' 
    with open(edgegraphB4fname,'w') as fout:
        for k in edgegraph.keys():
            fout.write(k+"\n")
            temp = k.split("_")
            ffnd = temp[0]+"_"+temp[1]
            ttnd = temp[2]+"_"+temp[3]
            nndset.append(ffnd)
            nndset.append(ttnd)
            ecnt = ecnt + 1

    print "nodes: %d " %ndcnt
    print "nodes : %d" %len(set(nndset))
    print "edges : %d" %ecnt
    print "nodes: "+str(cnt)
    print "edges: "+str(snt)
    print "tograph %d" %len(tograph)
    print "done"

if __name__=="__main__":
    main()
