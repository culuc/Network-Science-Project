import sys
sys.path.append('./Modules')
import networkx as nx
from matplotlib import pyplot as plt
import numpy as np
import importlib
import timeit

import randomnet as rndm
import cascade_mod_final as cas

k4n1000 = rndm.run_multi(1000,4,10, res=20, path='Results/N1000r4.json')
