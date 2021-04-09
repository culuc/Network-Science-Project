import sys
sys.path.append('./Modules')
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
import importlib
import timeit
#%%
import randomnet as rndm
import cascade_mod_final as cas

sf2000g23 = rndm.run_multiSF(2000,2.3,30,path='Results4/sf23rep30r4.json')
