#%%
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

#%% Read power grid edgelist
power = nx.read_edgelist('project/Germany_grid_data/0.2/branches.csv',data=(('X',float),('Pmax',float),),)


# %%
power.nodes(data=True)

# %% Read power grid nodes
df = pd.read_csv('project/Germany_grid_data/0.2/nodes.csv',sep=None, index_col='Name')
# df.head()


# %% Add node info to power grid network
# Labels for lat,long are wrongly labeled in power dataset
for n in power.nodes():
    if n in df.index:
        power.node[n]['Latitude'] = df.loc[n]['Lon']
        power.node[n]['Longitude'] = df.loc[n]['Lat']

# %% Read internet network
G_internet = nx.read_graphml('project/Dfn.graphml.xml')

# %%
G_internet.nodes(data=True)

# %%
#nx.draw(G_internet)

# %% Add indicator to network edges to draw in different colors
for e in power.edges():
    power.edges[e]['Value'] = 1

for e in G_internet.edges():
    G_internet.edges[e]['Value'] = 2

# %% function to connect spacially close nodes -- only takes into consideration nodes that provide lat,long info
def make_interdependent(G1,G2,thresh):
    nodes1 = G1.nodes()
    nodes2 = G2.nodes()
    G = nx.union(G1,G2)
    counter = 0
    dist = []
    nodelist = {'G1':[],'G2':[]}

    for n1 in nodes1:
        G.node[n1]['Value'] = 1 # add value to draw
        if not 'Latitude' in G.node[n1].keys():
            continue
        nodelist['G1'].append(n1)
        for n2 in nodes2:
            G.node[n2]['Value'] = 2 # add value to draw
            if not 'Latitude' in G.node[n2].keys():
                continue
            nodelist['G2'].append(n2)
            lat = np.abs(G.node[n1]['Latitude']-G.node[n2]['Latitude'])
            # print('Lat:', G.node[n1]['Latitude'],G.node[n2]['Latitude'])
            long = np.abs(G.node[n1]['Longitude']-G.node[n2]['Longitude'])
            # print('Long:',G.node[n1]['Longitude'],G.node[n2]['Longitude'])
            #print(lat,long)
            dist.append((lat,long))
            if (lat < thresh) & (long < thresh):
                G.add_edge(n1,n2, Value=3)
                counter += 1
    return G,counter,dist,nodelist

#%%
G,t,l, nodelist = make_interdependent(power,G_internet,0.1)
#%%
nx.write_graphml(G,'./Project/G_interdependent.graphml')
nx.write_graphml(power,'./Project/G_power.graphml')
nx.write_graphml(G_internet,'./Project/G_internet.graphml')

# %% Create basemap of region Germany to draw nettwork onto
plt.figure(figsize=(20, 40))
m = Basemap(
        projection='merc',
        llcrnrlon=5,
        llcrnrlat=46,
        urcrnrlon=16,
        urcrnrlat=56,
        lat_ts=0,
        resolution='i',
        suppress_ticks=True)
#%% map network nodes to position relative to basemap
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


#%% get values for drawing nodes,edges in color
values = [G2.node[n]['Value'] for n in G2.nodes()]
values_edges = [G2.edges[e]['Value'] for e in G2.edges()]

# %% draw network
graph = G2
# nx.draw_networkx_nodes(G = graph, pos = pos, node_list = graph.nodes(), node_color = values, alpha = 0.4, node_size=10,cmap=plt.get_cmap('Pastel1'))
# nx.draw_networkx_nodes(G = graph, pos = pos, node_list = nodelist['G2'], node_color = 'y', alpha = 0.2, node_size=10)
nx.draw_networkx_edges(G = graph, 
    pos = pos, 
    edge_color=values_edges,
    cmap=plt.get_cmap('Pastel1'),
    arrows=False,
    width=0.5
    )
# m.drawcoastlines(color='black',linewidth=0.5)
m.drawcountries(color='black',linewidth=0.5)
# m.fillcontinents(color="#FFDDCC", lake_color='#DDEEFF')
# m.drawmapboundary(fill_color="#DDEEFF")
m.shadedrelief()
# %%
