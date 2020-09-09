from igraph import *
from HeapBinaria import HeapBinaria
import pickle
import dill
import pandas as pd
import random
import utm
import matplotlib.pyplot as pl
import time

dump_file2 = open('tiempos.pkl', 'rb')
dict_tiempos = dill.load(dump_file2)
dump_file2.close()

dump_file3 = open('frecuencias.pkl', 'rb')
dict_frecuencia = dill.load(dump_file3)
dump_file3.close()


print(dict_tiempos['T405 00I']['E-20-53-PO-95'])
print(dict_tiempos['T405 00I']['T-14-128-PO-20'])

print(dict_frecuencia['T405 00I']['E-20-53-PO-95'])
