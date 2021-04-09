import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
import cascade_mod_final as cas
import json
import powerlaw

def new_network(n,k):
    g1 = nx.gnp_random_graph(n,k/n)
    g2 = nx.gnp_random_graph(n,k/n)
    nx.relabel_nodes(g2, lambda x: x + len(g1.nodes()),copy=False)
    for e in g1.edges():
        g1.edges[e]['Value'] = 1
    for e in g2.edges():
        g2.edges[e]['Value'] = 2
    for node in g1.nodes():
        g1.nodes[node]['Value'] = 1
    for node in g2.nodes():
        g2.nodes[node]['Value'] = 2

    G = nx.union(g1,g2)
    n1 = set(g1.nodes())
    n2 = set(g2.nodes())

    while n1:
        a = n1.pop()
        while n2:
            b = n2.pop()
            break
        G.add_edge(a,b, Value=3)
    return G, g1, g2
#%%
def new_networkSF(n,gamma):
    g1 = generateSFNetwork(n=n, gamma=gamma)
    g2 = generateSFNetwork(n=n, gamma=gamma)
    nx.relabel_nodes(g2, lambda x: x + len(g1.nodes()),copy=False)
    for e in g1.edges():
        g1.edges[e]['Value'] = 1
    for e in g2.edges():
        g2.edges[e]['Value'] = 2
    for node in g1.nodes():
        g1.nodes[node]['Value'] = 1
    for node in g2.nodes():
        g2.nodes[node]['Value'] = 2

    G = nx.union(g1,g2)
    n1 = set(g1.nodes())
    n2 = set(g2.nodes())

    while n1:
        a = n1.pop()
        while n2:
            b = n2.pop()
            break
        G.add_edge(a,b, Value=3)
    return G, g1, g2

#%% function to generate scale free networks with given lambda
def is_graphic_Erdos_Gallai(degree_sequence_to_test):
    degree_sequence = sorted(degree_sequence_to_test,reverse=True)
    S = sum(degree_sequence)
    n = len(degree_sequence)
    if S%2 != 0:
        return False
    for r in range(1, n):
        M = 0
        S = 0
        for i in range(1, r+1):
            S += degree_sequence[i-1]
        for i in range(r+1, n+1):
            M += min(r, degree_sequence[i-1])
        if S > r * (r-1) + M:
            return False
    return True


def ConfigurationModel(degrees, relax = False):
    # assume that we are given a graphical degree sequence
    if not is_graphic_Erdos_Gallai(degrees):
        return 0
    
    # create empty network with n nodes
    n = len(degrees)
    g = nx.Graph()
    
    # generate link stubs based on degree sequence
    stubs = []
    for i in range(n):
        for k in range(degrees[i]):
            stubs.append(i)
    
    # connect randomly chosen pairs of link stubs
    # note: if relax is True, we conceptually allow self-loops 
    # and multi-edges, but do not add them to the network/
    # This implies that the generated network may not have 
    # exactly sum(degrees)/2 links, but it ensures that the algorithm 
    # always finishes.
    while(len(stubs)>0):
        v, w = np.random.choice(stubs, 2, replace=False)
        if relax or (v!=w and ((v,w) not in g.edges.keys())):
            # do not add self-loops and multi-edges
            if (v!=w and ((v,w) not in g.edges.keys())):
                g.add_edge(v,w)
            stubs.remove(v)
            stubs.remove(w)
    return g

#%% 
def generateSFNetwork(n=1000, gamma=2.1):
    #degrees_zipf = [1]
    degrees_powerlaw = [1]
    while not is_graphic_Erdos_Gallai(degrees_powerlaw):
        #degrees_zipf = [int(x) for x in np.random.zipf(gamma, n)]
        degrees_powerlaw = powerlaw.Power_Law(xmin=2, parameters=[gamma]).generate_random(n).astype('int')
    g = ConfigurationModel(degrees_powerlaw, relax = True)
    return g

# %%
def draw(G,path=None):
    values = [G.nodes[node]['Value'] for node in G.nodes()]
    values_edges = [G.edges[e]['Value'] for e in G.edges()]
    pos = nx.spring_layout(G,weight='Value')

    nx.draw_networkx(G,
        node_color=values,
        edge_color=values_edges,
        #pos = pos,
        cmap=plt.get_cmap('Pastel1'))

    if path:
        plt.savefig(path,dpi=300,bbox_inches='tight')


# %%
def pmcc(G_new, G_orig):
    # probablitiy of mutually connected component
    l = len(G_orig)
    cc = list(nx.connected_components(G_new))
    if len(cc) > 0:
        ret = len(max(cc,key=len))/l
    else:
        ret = 0
    return ret

# %%
def pmcc_old(G_new):
    l = len(G_new)
    cc = list(nx.connected_components(G_new))
    if len(cc) > 0:
        ret = len(max(cc,key=len))/l
    else:
        ret = 0
    return ret

#%%
def run_analysisSF(G,g1,g2,lb=0.5,ub=1,res=10):
    P = {}
    for p in np.linspace(lb,ub,res,endpoint=True):
        print(p)
        Ga = cas.attack_network(G,g1,g2,p,verbose=False)
        P[p] = pmcc(Ga,G)
    return P

def run_multiSF(N,gamma,t,lb=0.5,ub=1,res=10,path=None):
    R, r1, r2 = new_networkSF(N,gamma)
    print(1)
    d = run_analysis(R,r1,r2,lb,ub,res)
    values = np.array(list(d.values()))/t
    keys = list(d.keys())
    for i in range(t-1):
        print(2+i)
        d = run_analysis(R,r1,r2,lb,ub,res)
        values += np.array(list(d.values()))/t
    dic = {k:v for k,v in zip(keys,values)}
    if path:
        with open(path, 'w') as fp:
            json.dump(dic, fp, sort_keys=True, indent=4)
    return dic
#%%
def run_analysis(G,g1,g2,lb=0.5,ub=1,res=10):
    P = {}
    for p in np.linspace(lb,ub,res,endpoint=True):
        print(p)
        Ga = cas.attack_network(G,g1,g2,p,verbose=False)
        P[p] = pmcc(Ga,G)
    return P

def run_multi(N,k,t,lb=0.5,ub=1,res=10,path=None):
    R, r1, r2 = new_network(N,k)
    print(1)
    d = run_analysis(R,r1,r2,lb,ub,res)
    values = np.array(list(d.values()))/t
    keys = list(d.keys())
    for i in range(t-1):
        print(2+i)
        d = run_analysis(R,r1,r2,lb,ub,res)
        values += np.array(list(d.values()))/t
    dic = {k:v for k,v in zip(keys,values)}
    if path:
        # with open(path,'a') as f:
        #     f.write('N'+str(N)+'k'+str(k)+'t'+str(t)+', ')
        #     f.write(str(dic))
        #     f.write('\n')
        with open(path, 'w') as fp:
            json.dump(dic, fp, sort_keys=True, indent=4)
    return dic

#%%
def plot_results(*results, k=1, path=None, labels=None,xlim=None,alpha=1,theopred = False, linetype='o-'):
    if theopred:
        plt.vlines(2.4554,0,1,linestyles='-.',label='theoretical prediction',alpha=0.3)
    for i,r in enumerate(results):
        x = np.array(list(r.keys()))*k
        y = list(r.values())
        if labels:
            plt.plot(x,y,linetype,label=labels[i],alpha=alpha)
            plt.legend()
        else:
            plt.plot(x,y,linetype,alpha=alpha)
    if k>1:
        plt.xlabel('$p \langle k \\rangle$')
    else:
        plt.xlabel('$p$')
    # plt.ylabel('$\mu_\infty$')
    plt.ylabel('$P_\infty$')
    # plt.xlim(left=2.5)
    if xlim:
        plt.xlim(xlim)
    if path:
        plt.savefig(path,dpi=300,bbox_inches='tight')
    plt.show()


# %%
def save_results(output,path):
     with open(path, 'w') as fp:
            json.dump(output, fp, sort_keys=True, indent=4)

# %%
def import_json(path):
    with open(path, 'r') as fp:
        d = json.load(fp)
    d2 = {float(k):v for k,v in d.items()}
    return d2