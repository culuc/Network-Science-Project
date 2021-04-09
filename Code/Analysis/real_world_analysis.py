#%%
import sys
sys.path.append('./Modules')
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
import importlib
import timeit
import json

#%%
# import cascade_mod as cas
import plot_network as pltn
import randomnet as rndm
import cascade_mod_final as cas
# import cascade_mod_redo2 as casr2
#%%
importlib.reload(pltn)
#%%
importlib.reload(cas)
#%%
importlib.reload(rndm)
#%%
G = nx.read_graphml('Analysis/G_interdependent.graphml')
g1 = nx.read_graphml('Analysis/G_power.graphml')
g2 = nx.read_graphml('Analysis/G_internet.graphml')
# %%
res = cas.attack_network(G,g1,g2,0.5)
#%%
pltn.draw(res, path = 'after_attack_p05.png')

# %%
def run_analysis(G,g1,g2,lb=0.5,ub=1,res=10):
    P = {}
    for p in np.linspace(lb,ub,res,endpoint=True):
        print(p)
        Ga = cas.attack_network(G,g1,g2,p,verbose=False)
        P[p] = rndm.pmcc(Ga,G)
    return P

def run_multi(G,g1,g2,t,lb=0.5,ub=1,res=10,path=None,id=''):
    print(1)
    d = run_analysis(G,g1,g2,lb,ub,res)
    values = np.array(list(d.values()))/t
    keys = list(d.keys())
    for i in range(t-1):
        print(2+i)
        d = run_analysis(G,g1,g2,lb,ub,res)
        values += np.array(list(d.values()))/t
    dic = {k:v for k,v in zip(keys,values)}
    if path:
            with open(path, 'w') as fp:
                json.dump(dic, fp, sort_keys=True, indent=4)
    return dic

# %%
rwa = run_multi(G,g1,g2,30)

# %%
rndm.plot_results(rwa,k=1,path='Results/real-world.png')

# %%
rndm.plot_results(rwa,k=3,path='Results/real-world_k.png')

# %%
rwa2 = run_multi(G,g1,g2,30,0,1,20)

# %%
rndm.plot_results(rwa2,k=1,path='Results/real-world_wide.png')

# %%
rndm.plot_results(rwa2,k=3,path='Results/real-world_wide_k.png')

# %%
nx.info(g2)
