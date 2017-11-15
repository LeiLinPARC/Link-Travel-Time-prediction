import osmnx as ox
import numpy as np
ox.config(log_file=True, log_console=True, use_cache=True)
G=ox.graph_from_bbox(41.9123147,41.7623147,12.6046319,12.4546319,network_type='drive',infrastructure='way["highway"]',simplify=False)
G=ox.simplify.simplify_graph(G, strict=False)
nodes = ox.graph_to_gdfs(G, edges=False)
edges = ox.graph_to_gdfs(G, nodes=False)
extract=nodes[['x','y']]
extract_edges=edges[['geometry']]
outputDir = '/home/aniket/Desktop/BTP/Travel Time Prediction/osmnx'
np.savetxt(outputDir + '/osmnxNodes.txt', extract.values, fmt='%f')
np.savetxt(outputDir + '/osmnxEdges.txt', extract_edges.values, fmt='%s')
fig,ax=ox.plot_graph(G,node_color='b',edge_color='r')
