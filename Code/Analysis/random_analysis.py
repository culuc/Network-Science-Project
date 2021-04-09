#%%
import sys
sys.path.append('./Modules')
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
import json

#%%

import randomnet as rndm
import cascade_mod_final as cas

#%%
N,n1,n2 = rndm.new_network(5,3)
A = cas.attack_network(N,n1,n2,0.8)
#%%
rndm.draw(N)
#%%
rndm.draw(N, path = 'example_before2.png')
#%%
rndm.draw(A, path = 'example_after2.png')


# %% ER random networks
N250r4 = rndm.import_json('Results/remote/N250r4.json')
N500r4 = rndm.import_json('Results/remote/N500r4.json')
N1000r4 = rndm.import_json('Results/remote/N1000r4.json')
N2000r4 = rndm.import_json('Results/remote/N2000r4.json')
N4000r4 = rndm.import_json('Results/remote/N4000r4.json')
N8000r4 = rndm.import_json('Results/remote/N8000r4.json')

# %% Plot results
rndm.plot_results(N250r4,N500r4,N1000r4,N2000r4,N4000r4,N8000r4, k=4, labels=['250','500','1000','2000','4000','8000'],theopred=True,alpha=0.5,path='Results/random1HD.png')


# %%
rndm.plot_results(N250r4,N500r4,N1000r4,N2000r4,N4000r4,N8000r4, k=4, labels=['250','500','1000','2000','4000','8000'],theopred=True,alpha=0.5,xlim=(2,3),path='Results/random1HDshort.png')



# %% Scale Free networks
sf3 = rndm.import_json('Results/remote/sf3.json')
sf27 = rndm.import_json('Results/remote/sf27.json')
sf23 = rndm.import_json('Results/remote/sf23rep30r4.json')
# %%
#%%
N2000 = rndm.import_json('Results/remote/N2000.json')
#%%
rndm.plot_results(N2000,sf3,sf27,sf23, labels = ['ER','$\lambda = 3$','$\lambda = 2.7$','$\lambda = 2.3$'],path='Results/partII.png',alpha=0.7)
