from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
import networkx as nx

# Create basemap of region Germany to draw nettwork onto
def draw(G, path=None):
    plt.figure(figsize=(6, 12))
    m = Basemap(
            projection='merc',
            llcrnrlon=5,
            llcrnrlat=46,
            urcrnrlon=16,
            urcrnrlat=56,
            lat_ts=0,
            resolution='i',
            suppress_ticks=True)
    # map network nodes to position relative to basemap, remove nodes that don't have location
    G2 = G.copy()
    pos = {}
    for n in G.nodes():
        # remove nodes that do not have lat,long info
        if 'Longitude' not in G.node[n].keys():
            G2.remove_node(n)
            continue
        long = G.node[n]['Longitude']
        lat = G.node[n]['Latitude']
        pos[n] = m(long,lat)


    #get values for drawing nodes,edges in color
    values = [G2.node[n]['Value'] for n in G2.nodes()]
    values_edges = [G2.edges[e]['Value'] for e in G2.edges()]

    # draw network
    graph = G2
    nx.draw_networkx_nodes(G = graph, pos = pos, node_list = graph.nodes(), node_color = values, alpha = 0.4, node_size=10,cmap=plt.get_cmap('Pastel1'))
    # nx.draw_networkx_nodes(G = graph, pos = pos, node_list = nodelist['G2'], node_color = 'y', alpha = 0.2, node_size=10)
    nx.draw_networkx_edges(G = graph, 
        pos = pos, 
        edge_color=values_edges,
        cmap=plt.get_cmap('Pastel1'),
        arrows=False,
        width=2
        )
    # m.drawcoastlines(color='black',linewidth=0.5)
    m.drawcountries(color='black',linewidth=1)
    # m.fillcontinents(color="#FFDDCC", lake_color='#DDEEFF')
    # m.drawmapboundary(fill_color="#DDEEFF")
    m.shadedrelief()
    if path:
        plt.savefig(path,dpi=300,bbox_inches='tight')
    plt.show()
