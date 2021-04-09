#%%
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# %%
def cascade_fail(G, g1, g2, target, verbose):

    G2 = G.copy()

    # detetct and delete neighboring node if it is from the other network
    hood = G.nodes[target]['Value']
    for neigh in G.neighbors(target):
        if G.nodes[neigh]['Value'] != hood:
            G2.remove_node(neigh)
            if neigh in g1.nodes():
                g1.remove_node(neigh)
            if neigh in g2.nodes():
                g2.remove_node(neigh)
            if verbose:
                print('deleted neighbour',neigh)

    # remove target node, update original refrence sub-networks
    G2.remove_node(target)
    if target in g1.nodes():
        g1.remove_node(target)
    if target in g2.nodes():
        g2.remove_node(target)

    return G2,g1,g2


#%%
def attack_network(G,g1,g2,p, verbose=True):
    # we keep and update the  sub-networks to detect the connected compnents
    g1 = g1.copy()
    g2 = g2.copy()
    G = G.copy()

    # random attack of the network g1 (or A in paper) by specifying probability (1-p) that each individual node is deleted
    candidates = set()
    for node in g1.nodes():
        if np.random.random() < 1-p:
            candidates.add(node)

    # keep & unpdate reference dict of candidate nodes to be deleted. Do so until all nodes are deleted via the cascading failure process
    while candidates:
        target = candidates.pop()
        if verbose:
            print('attacking', target)
        G,g1,g2 = cascade_fail(G,g1,g2,target=target, verbose=verbose)
        nodes_updated = set(G.nodes())
        candidates.intersection_update(nodes_updated)
    

    # recursively detect clusters and remove connecting links from neigboring network by switching g1=g2 and g2=g1
    # G3,g1,g2 = cascade_rec(G2,g1,g2,1,verbose)

    G2,g1,g2 = cascade_rec(G,g1,g2,1,verbose)

    return G2

# %% 
def cascade_rec(G,g1,g2,counter,verbose):
    # recursively detect own (g1) connceted components and delete the links between them from other network (g2)

    removed = 0

    # get list of connected components for g1 
    components = list(nx.connected_components(g1))

    # get a set of all edges in g2. For each edge, check if the two nodes have a foreign neighor (from g1) in diffent clusters. If yes, delete this link.
    edges = set(g2.edges())
    while edges:
        a,b = edges.pop()
        # print(a,b)
        n1 = foreign_neighbors(a,G)
        n2 = foreign_neighbors(b,G)
        if n1 == {None} or n2 == {None}:
            continue 
        for comp in components:
            if (n1.issubset(comp) and not n2.issubset(comp)) or (not n1.issubset(comp) and n2.issubset(comp)):
                G.remove_edge(a,b)
                g2.remove_edge(a,b)

                removed = 1
                if verbose:
                    print('Removed', tuple((a, b)))
                break
      
    # if we removed an edge, continue looking from other networks' perspective
    if removed == 1:
        cascade_rec(G,g2,g1,1,verbose)

    # if unsucessful, try again once with other network, decrease counter by one to evetualy stop recursion process
    if removed == 0 and counter>0:
        cascade_rec(G,g2,g1,counter-1,verbose)

    return G,g1,g2


def foreign_neighbors(node,G):
    # this computes a unique list of all foreign neigbors in a node, i.e. nodes that initially came from a different network
    foreign = []
    hood = G.nodes[node]['Value']
    s = set(G.neighbors(node))
    while s:
        x = s.pop()
        if G.nodes[x]['Value'] != hood:
            foreign.append(x)
    if len(foreign) == 0:
        foreign = [None]
    return set(foreign)