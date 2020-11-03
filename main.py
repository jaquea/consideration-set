import pickle

import csv

import dill

from consideration_set import Consideration_set
from reporte_archivos import Files
import pandas as pd
import json
import os
from path_size import correlacion, process_frame_alt


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

dump_file1 = open('tmp\\viajes_k_shortest_alternativas_desaglosadas_procesados.pkl', 'rb')
viajes_k_shortest_alternativas_desaglosadas_procesados = dill.load(dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\viajes_k_shortest_alternativas_procesados.pkl', 'rb')
viajes_k_shortest_alternativas_procesados = dill.load(dump_file1)
dump_file1.close()

dump_file2 = open('tmp\\viajes_link_penalty_shortest_alternativas_desaglosadas_procesados.pkl', 'rb')
viajes_link_penalty_shortest_alternativas_desaglosadas_procesados = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_link_penalty_shortest_alternativas_procesados.pkl', 'rb')
viajes_link_penalty_shortest_alternativas_procesados = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_labeling_shortest_alternativas_desaglosadas_procesados.pkl', 'rb')
viajes_labeling_shortest_alternativas_desaglosadas_procesados = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_labeling_shortest_alternativas_procesados.pkl', 'rb')
viajes_labeling_shortest_alternativas_procesados = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_link_elimination_shortest_alternativas_desaglosadas_procesados.pkl', 'rb')
viajes_link_elimination_shortest_alternativas_desaglosadas_procesados = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_link_elimination_shortest_alternativas_procesados.pkl', 'rb')
viajes_link_elimination_shortest_alternativas_procesados = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_prediccion_alternativas_desaglosadas_procesados.pkl', 'rb')
viajes_prediccion_alternativas_desaglosadas_procesados = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_prediccion_alternativas_procesados.pkl', 'rb')
viajes_prediccion_alternativas_procesados = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_prediccion_procesados.pkl', 'rb')
viajes_prediccion_procesados = dill.load(dump_file2)
dump_file2.close()

with open(os.path.join('inputs', 'info_servicios.json')) as data_file:
    data = json.loads(data_file.read())
df = pd.DataFrame.from_dict(data, orient='columns')

with open('outputs\\resumen_geografico_OD.csv', 'wb') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(['origen', 'destino', 'x_origen', 'y_origen', 'x_destino', 'y_destino'])

    for origen in viajes:
        for destino in viajes[origen]:
            writer.writerow([origen, destino, paraderos_coord_dic[origen][0], paraderos_coord_dic[origen][1], paraderos_coord_dic[destino][0], paraderos_coord_dic[destino][1]])

'''
with open('outputs\\k_rutas_minimas.csv', 'wb') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(['origen', 'destino', 'camino'])

    for origen in viajes_k_shortest_alternativas_procesados:
        for destino in viajes_k_shortest_alternativas_procesados[origen]:
            for camino in viajes_k_shortest_alternativas_procesados[origen][destino]:
                writer = csv.writer(csvFile)
                writer.writerow([origen, destino, camino])

with open('outputs\\link_penalty.csv', 'wb') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(['origen', 'destino', 'camino'])

    for origen in viajes_link_penalty_shortest_alternativas_procesados:
        for destino in viajes_link_penalty_shortest_alternativas_procesados[origen]:
            for camino in viajes_link_penalty_shortest_alternativas_procesados[origen][destino]:
                writer = csv.writer(csvFile)
                writer.writerow([origen, destino, camino])

with open('outputs\\labeling.csv', 'wb') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(['origen', 'destino', 'camino'])

    for origen in viajes_labeling_shortest_alternativas_procesados:
        for destino in viajes_labeling_shortest_alternativas_procesados[origen]:
            for camino in viajes_labeling_shortest_alternativas_procesados[origen][destino]:
                writer = csv.writer(csvFile)
                writer.writerow([origen, destino, camino])

with open('outputs\\link_elimination.csv', 'wb') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(['origen', 'destino', 'camino'])

    for origen in viajes_link_elimination_shortest_alternativas_procesados:
        for destino in viajes_link_elimination_shortest_alternativas_procesados[origen]:
            for camino in viajes_link_elimination_shortest_alternativas_procesados[origen][destino]:
                writer = csv.writer(csvFile)
                writer.writerow([origen, destino, camino])

###procesamiento para hacer resumen de todos los tipos de conjunto de consideracion excepto el de hyper-ruta que esta hecho en otro apartado
with open('outputs\\resumen_tipos_conj_consideracion.csv', 'wb') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(
        ['origen', 'destino', 'total_viajes', 'viajes_k_rutas_minimas', 'largo_k_rutas_minimas',
         'largo_caminos_usados'])

    for destino in viajes:
        print(destino)
        for ori in viajes[destino]:

            total_viajes = 0

            viajes_en_k_rutas_minimas = 0
            largo_k_rutas_minimas = len(viajes_k_shortest_alternativas_procesados[ori][destino])


            largo_caminos_usados = len(viajes[destino][ori])

            for camino in viajes[destino][ori]:
                n_viajes = viajes[destino][ori][camino]
                total_viajes += n_viajes

                if camino in viajes_k_shortest_alternativas_procesados[ori][destino]:
                    viajes_en_k_rutas_minimas += n_viajes

            row = [ori, destino, total_viajes, viajes_en_k_rutas_minimas, largo_k_rutas_minimas, largo_caminos_usados]

            writer.writerow(row)
'''
#viajes_p = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
#viajes_alternativas_procesados_p = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
#viajes_alternativas_desaglosadas_procesados_p = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))

#viajes_p['T-31-134-SN-20']['T-34-270-SN-30'] = viajes['T-31-134-SN-20']['T-34-270-SN-30']

#viajes_p['M-TB']['T-13-104-PO-15'] = viajes['M-TB']['T-13-104-PO-15']
#viajes_p['M-TB']['T-13-54-SN-60'] = viajes['M-TB']['T-13-54-SN-60']
#viajes_p['L-33-52-155-PO']['L-33-52-5-OP'] = viajes['L-33-52-155-PO']['L-33-52-5-OP']
#viajes_p['T-18-156-PO-37']['M-CS'] = viajes['T-18-156-PO-37']['M-CS']

#viajes_alternativas_procesados_p['E-14-170-NS-5']['L-17-19-35-PO'] = viajes_alternativas_procesados['E-14-170-NS-5']['L-17-19-35-PO']
#viajes_alternativas_procesados_p['T-13-104-PO-15']['M-TB'] = viajes_alternativas_procesados['T-13-104-PO-15']['M-TB']
#viajes_alternativas_procesados_p['T-13-54-SN-60']['M-TB'] = viajes_alternativas_procesados['T-13-54-SN-60']['M-TB']
#viajes_alternativas_procesados_p['L-33-52-5-OP']['L-33-52-155-PO'] = viajes_alternativas_procesados['L-33-52-5-OP']['L-33-52-155-PO']
#viajes_alternativas_procesados_p['M-CS']['T-18-156-PO-37']= viajes_alternativas_procesados['M-CS'] ['T-18-156-PO-37']
#viajes_alternativas_procesados_p['T-34-270-SN-30']['T-31-134-SN-20']= viajes_alternativas_procesados['T-34-270-SN-30']['T-31-134-SN-20']

#viajes_alternativas_desaglosadas_procesados_p['T-34-270-SN-30']['T-31-134-SN-20'] = viajes_alternativas_desaglosadas_procesados['T-34-270-SN-30']['T-31-134-SN-20']
#viajes_alternativas_desaglosadas_procesados_p['T-13-104-PO-15']['M-TB'] = viajes_alternativas_desaglosadas_procesados['T-13-104-PO-15']['M-TB']

#viajes_p['M-TB']['T-13-104-PO-15'] = viajes['M-TB']['T-13-104-PO-15']

#viajes = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
#viajes = viajes_p

#viajes_alternativas_procesados = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
#viajes_alternativas_procesados = viajes_alternativas_procesados_p

#viajes_alternativas_desaglosadas_procesados = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))

def alternativas_maximas(diccionario):
    cant_max_alternativas_observadas = 0
    for o in diccionario:
        for d in diccionario[o]:
            largo_camino = len(diccionario[o][d])
            if largo_camino > cant_max_alternativas_observadas:
                cant_max_alternativas_observadas = largo_camino
    return cant_max_alternativas_observadas

'''
#conjunto de consideracion para hiper-rutas
files_obj = Files(viajes, g, paradero_cercano_dic, dict_servicio_llave_codigoTS)
files_obj.real_trips()

hiperruta_minimo_camino_desglosado, cant_max_alternativas_hiperruta, hiperruta_minimo = files_obj.hyperpath_from_travel_file(dict_tiempos, dict_frecuencia)

PS = process_frame_alt(hiperruta_minimo_camino_desglosado, g)

print('calcule primer diccionario')
PS_correlacion = correlacion(df, PS, dict_tiempos)

Consideration_set_obj = Consideration_set(cant_max_alternativas_hiperruta)
Consideration_set_obj.get_consideration_set(g, hiperruta_minimo_camino_desglosado, viajes, dict_tiempos, dict_frecuencia,
                                            paraderos_coord_dic, hiperruta_minimo,dict_servicio_llave_usuario, g_metro, '1', PS_correlacion)



#viajes_alternativas_desaglosadas_procesados = viajes_alternativas_desaglosadas_procesados_p

'''
'''
###conjunto de consideracion para alternativas observadas###

PS = process_frame_alt(viajes_alternativas_desaglosadas_procesados, g)

print('calcule primer diccionario')
PS_correlacion = correlacion(df, PS, dict_tiempos)

print('ya calcule correlacion')

def alternativas_maximas(diccionario):
    cant_max_alternativas_observadas = 0
    for o in diccionario:
        for d in diccionario[o]:
            largo_camino = len(diccionario[o][d])
            if largo_camino > cant_max_alternativas_observadas:
                cant_max_alternativas_observadas = largo_camino
    return cant_max_alternativas_observadas


Consideration_set_obj = Consideration_set(alternativas_maximas(viajes_alternativas_desaglosadas_procesados))

Consideration_set_obj.get_consideration_set(g, viajes_alternativas_desaglosadas_procesados, viajes, dict_tiempos, dict_frecuencia,
                                            paraderos_coord_dic, viajes_alternativas_procesados,dict_servicio_llave_usuario, g_metro, '2', PS_correlacion)


###conjunto de consideracion para k rutas minimas###

PS = process_frame_alt(viajes_k_shortest_alternativas_desaglosadas_procesados, g)

PS_correlacion = correlacion(df, PS, dict_tiempos)


Consideration_set_obj = Consideration_set(alternativas_maximas(viajes_k_shortest_alternativas_desaglosadas_procesados))

Consideration_set_obj.get_consideration_set(g, viajes_k_shortest_alternativas_desaglosadas_procesados, viajes, dict_tiempos, dict_frecuencia,
                                            paraderos_coord_dic, viajes_k_shortest_alternativas_procesados, dict_servicio_llave_usuario, g_metro, '3', PS_correlacion)
'''
'''
###conjunto de consideracion para alternativas de prediccion###

PS = process_frame_alt(viajes_prediccion_alternativas_desaglosadas_procesados, g)

print('calcule primer diccionario')
PS_correlacion = correlacion(df, PS, dict_tiempos)

print('ya calcule correlacion')

def alternativas_maximas(diccionario):
    cant_max_alternativas_observadas = 0
    for o in diccionario:
        for d in diccionario[o]:
            largo_camino = len(diccionario[o][d])
            if largo_camino > cant_max_alternativas_observadas:
                cant_max_alternativas_observadas = largo_camino
    return cant_max_alternativas_observadas


Consideration_set_obj = Consideration_set(alternativas_maximas(viajes_prediccion_alternativas_desaglosadas_procesados))

Consideration_set_obj.get_consideration_set(g, viajes_prediccion_alternativas_desaglosadas_procesados, viajes_prediccion_procesados, dict_tiempos, dict_frecuencia,
                                            paraderos_coord_dic, viajes_prediccion_alternativas_procesados,dict_servicio_llave_usuario, g_metro, '4', PS_correlacion)
'''

###conjunto de consideracion para labeling###

PS = process_frame_alt(viajes_labeling_shortest_alternativas_desaglosadas_procesados, g)

PS_correlacion = correlacion(df, PS, dict_tiempos)


Consideration_set_obj = Consideration_set(alternativas_maximas(viajes_labeling_shortest_alternativas_desaglosadas_procesados))

Consideration_set_obj.get_consideration_set(g, viajes_labeling_shortest_alternativas_desaglosadas_procesados, viajes, dict_tiempos, dict_frecuencia,
                                            paraderos_coord_dic, viajes_labeling_shortest_alternativas_procesados, dict_servicio_llave_usuario, g_metro, '5', PS_correlacion)
