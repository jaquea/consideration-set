import pickle
from collections import defaultdict
import csv

import dill

from consideration_set import Consideration_set
from reporte_archivos import Files
import pandas as pd

# se procesan los viajes
dump_file2 = open('tmp\\viajes_procesados.pkl', 'rb')
viajes = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\tiempos.pkl', 'rb')
dict_tiempos = dill.load(dump_file2)
dump_file2.close()

dump_file3 = open('tmp\\frecuencias.pkl', 'rb')
dict_frecuencia = dill.load(dump_file3)
dump_file3.close()

dump_file2 = open('tmp\\paraderos_coord_dic.pkl', 'rb')
paraderos_coord_dic = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\paradero_cercano_dic.pkl', 'rb')
paradero_cercano_dic = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\dict_hacinamiento_metro.pkl', 'rb')
dict_hacinamiento_metro = dill.load(dump_file2)
dump_file2.close()

dump_file1 = open('tmp\\grafo.igraph', 'rb')
g = pickle.load(dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\grafo_metro.igraph', 'rb')
g_metro = pickle.load(dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\dict_servicio_llave_codigoTS.pkl', 'rb')
dict_servicio_llave_codigoTS = dill.load(dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\dict_servicio_llave_usuario.pkl', 'rb')
dict_servicio_llave_usuario = dill.load(dump_file1)
dump_file1.close()


dump_file1 = open('tmp\\viajes_alternativas_desaglosadas_procesados.pkl', 'rb')
viajes_alternativas_desaglosadas_procesados = dill.load(dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\viajes_alternativas_procesados.pkl', 'rb')
viajes_alternativas_procesados = dill.load(dump_file1)
dump_file1.close()


with open('outputs\\resumen_geografico_OD.csv', 'wb') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(['origen', 'destino', 'x_origen', 'y_origen', 'x_destino', 'y_destino'])

    for origen in viajes:
        for destino in viajes[origen]:
            writer.writerow([origen, destino, paraderos_coord_dic[origen][0], paraderos_coord_dic[origen][1], paraderos_coord_dic[destino][0], paraderos_coord_dic[destino][1]])

#viajes_p = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
#viajes_alternativas_procesados_p = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
#viajes_p['M-TB']['T-13-104-PO-15'] = viajes['M-TB']['T-13-104-PO-15']
#viajes_p['M-TB']['T-13-54-SN-60'] = viajes['M-TB']['T-13-54-SN-60']
#viajes_p['L-33-52-155-PO']['L-33-52-5-OP'] = viajes['L-33-52-155-PO']['L-33-52-5-OP']
#viajes_p['T-18-156-PO-37']['M-CS'] = viajes['T-18-156-PO-37']['M-CS']

#viajes_alternativas_procesados_p['E-14-170-NS-5']['L-17-19-35-PO'] = viajes_alternativas_procesados['E-14-170-NS-5']['L-17-19-35-PO']
#viajes_alternativas_procesados_p['T-13-104-PO-15']['M-TB'] = viajes_alternativas_procesados['T-13-104-PO-15']['M-TB']
#viajes_alternativas_procesados_p['T-13-54-SN-60']['M-TB'] = viajes_alternativas_procesados['T-13-54-SN-60']['M-TB']
#viajes_alternativas_procesados_p['L-33-52-5-OP']['L-33-52-155-PO'] = viajes_alternativas_procesados['L-33-52-5-OP']['L-33-52-155-PO']
#viajes_alternativas_procesados_p['M-CS']['T-18-156-PO-37']= viajes_alternativas_procesados['M-CS'] ['T-18-156-PO-37']



#viajes_p['L-17-19-35-PO']['E-14-170-NS-5'] = viajes['L-17-19-35-PO']['E-14-170-NS-5']

#viajes = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
#viajes = viajes_p

#viajes_alternativas_procesados = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
#viajes_alternativas_procesados = viajes_alternativas_procesados_p
'''
#conjunto de consideracion para hiper-rutas
files_obj = Files(viajes, g, paradero_cercano_dic, dict_servicio_llave_codigoTS)
files_obj.real_trips()
hiperruta_minimo_camino_desglosado, cant_max_alternativas_hiperruta, hiperruta_minimo = files_obj.hyperpath_from_travel_file(dict_tiempos, dict_frecuencia)

Consideration_set_obj = Consideration_set(cant_max_alternativas_hiperruta)
Consideration_set_obj.get_consideration_set(g, hiperruta_minimo_camino_desglosado, viajes, dict_tiempos, dict_frecuencia,
                                            paraderos_coord_dic, hiperruta_minimo,dict_servicio_llave_usuario, g_metro, '1')


'''
#conjunto de consideracion para alternativas observada



def alternativas_maximas(diccionario):
    cant_max_alternativas_observadas = 0
    for ori in diccionario:
        for dest in diccionario[ori]:
            largo_alternativas = len(diccionario[ori][dest])
            if largo_alternativas > cant_max_alternativas_observadas:
                cant_max_alternativas_observadas = largo_alternativas
    return cant_max_alternativas_observadas


Consideration_set_obj = Consideration_set(alternativas_maximas(viajes_alternativas_procesados))

Consideration_set_obj.get_consideration_set(g, viajes_alternativas_desaglosadas_procesados, viajes, dict_tiempos, dict_frecuencia,
                                            paraderos_coord_dic, viajes_alternativas_procesados,dict_servicio_llave_usuario, g_metro, '2')

