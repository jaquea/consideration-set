import pickle
import csv

import dill

from consideration_set import Consideration_set
from reporte_archivos import Files
import pandas as pd
import json
import os
from path_size import correlacion, process_frame_alt
from collections import defaultdict
import copy

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

# Aca estan los conjuntos de consideracion de los viajes observados con la cantidad desemanas establecidas en el archivo
#proces_viajes2.py. Corresponden a datos observados en el 80% de los pares OD
dump_file1 = open('tmp\\viajes_alternativas_desaglosadas_procesados.pkl', 'rb')
viajes_alternativas_desaglosadas_procesados = dill.load(dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\viajes_alternativas_procesados.pkl', 'rb')
viajes_alternativas_procesados = dill.load(dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\viajes_simulation_shortest_alternativas_desaglosadas_procesados.pkl', 'rb')
viajes_simulation_shortest_alternativas_desaglosadas_procesados = dill.load(dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\viajes_simulation_shortest_alternativas_procesados.pkl', 'rb')
viajes_simulation_shortest_alternativas_procesados = dill.load(dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\viajes_simulation_shortest_alternativas_desaglosadas_procesados_observed_parameters.pkl', 'rb')
viajes_simulation_shortest_alternativas_desaglosadas_procesados_observed_parameters = dill.load(dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\viajes_simulation_shortest_alternativas_procesados_observed_parameters.pkl', 'rb')
viajes_simulation_shortest_alternativas_procesados_observed_parameters = dill.load(dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\viajes_k_shortest_alternativas_desaglosadas_procesados.pkl', 'rb')
viajes_k_shortest_alternativas_desaglosadas_procesados = dill.load(dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\viajes_k_shortest_alternativas_procesados.pkl', 'rb')
viajes_k_shortest_alternativas_procesados = dill.load(dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\viajes_k_shortest_alternativas_desaglosadas_procesados_observed_parameters.pkl', 'rb')
viajes_k_shortest_alternativas_desaglosadas_procesados_observed_parameters = dill.load(dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\viajes_k_shortest_alternativas_procesados_observed_parameters.pkl', 'rb')
viajes_k_shortest_alternativas_procesados_observed_parameters = dill.load(dump_file1)
dump_file1.close()

dump_file2 = open('tmp\\viajes_link_penalty_shortest_alternativas_desaglosadas_procesados.pkl', 'rb')
viajes_link_penalty_shortest_alternativas_desaglosadas_procesados = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_link_penalty_shortest_alternativas_procesados.pkl', 'rb')
viajes_link_penalty_shortest_alternativas_procesados = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_link_penalty_shortest_alternativas_desaglosadas_procesados_observed_parameters.pkl', 'rb')
viajes_link_penalty_shortest_alternativas_desaglosadas_procesados_observed_parameters = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_link_penalty_shortest_alternativas_procesados_observed_parameters.pkl', 'rb')
viajes_link_penalty_shortest_alternativas_procesados_observed_parameters = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_labeling_shortest_alternativas_desaglosadas_procesados.pkl', 'rb')
viajes_labeling_shortest_alternativas_desaglosadas_procesados = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_labeling_shortest_alternativas_procesados.pkl', 'rb')
viajes_labeling_shortest_alternativas_procesados = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_labeling_shortest_alternativas_desaglosadas_procesados_observed_parameters.pkl', 'rb')
viajes_labeling_shortest_alternativas_desaglosadas_procesados_observed_parameters = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_labeling_shortest_alternativas_procesados_observed_parameters.pkl', 'rb')
viajes_labeling_shortest_alternativas_procesados_observed_parameters = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_link_elimination_shortest_alternativas_desaglosadas_procesados.pkl', 'rb')
viajes_link_elimination_shortest_alternativas_desaglosadas_procesados = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_link_elimination_shortest_alternativas_procesados.pkl', 'rb')
viajes_link_elimination_shortest_alternativas_procesados = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_link_elimination_shortest_alternativas_desaglosadas_procesados_observed_parameters.pkl', 'rb')
viajes_link_elimination_shortest_alternativas_desaglosadas_procesados_observed_parameters = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_link_elimination_shortest_alternativas_procesados_observed_parameters.pkl', 'rb')
viajes_link_elimination_shortest_alternativas_procesados_observed_parameters = dill.load(dump_file2)
dump_file2.close()

#archivos para prediccion

dump_file2 = open('tmp\\viajes_prediccion_alternativas_desaglosadas_procesados.pkl', 'rb')
viajes_prediccion_alternativas_desaglosadas_procesados = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_prediccion_alternativas_procesados.pkl', 'rb')
viajes_prediccion_alternativas_procesados = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_prediccion_procesados.pkl', 'rb')
viajes_prediccion_procesados = dill.load(dump_file2)
dump_file2.close()

#prediccion link_elimination
dump_file2 = open('tmp\\viajes_link_elimination_shortest_alternativas_desaglosadas_procesados_prediccion.pkl', 'rb')
viajes_link_elimination_shortest_alternativas_desaglosadas_procesados_prediccion = dill.load(dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_link_elimination_shortest_alternativas_procesados_prediccion.pkl', 'rb')
viajes_link_elimination_shortest_alternativas_procesados_prediccion = dill.load(dump_file2)
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
viajes_p = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
viajes_alternativas_procesados_p = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
viajes_alternativas_desaglosadas_procesados_p = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
viajes_labeling_shortest_alternativas_desaglosadas_procesados_p = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
viajes_labeling_shortest_alternativas_procesados_p = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))

viajes_p['T-13-12-NS-25']['M-MQ'] = viajes['T-13-12-NS-25']['M-MQ']
viajes_alternativas_procesados_p['T-13-12-NS-25']['M-MQ'] = viajes_alternativas_procesados['T-13-12-NS-25']['M-MQ']
viajes_alternativas_desaglosadas_procesados_p['T-13-12-NS-25']['M-MQ'] = viajes_alternativas_desaglosadas_procesados['T-13-12-NS-25']['M-MQ']

viajes_labeling_shortest_alternativas_desaglosadas_procesados_p['T-13-12-NS-25']['M-MQ'] = viajes_labeling_shortest_alternativas_desaglosadas_procesados['T-13-12-NS-25']['M-MQ']
viajes_labeling_shortest_alternativas_procesados_p['T-13-12-NS-25']['M-MQ'] = viajes_labeling_shortest_alternativas_procesados['T-13-12-NS-25']['M-MQ']

viajes_p['M-CS']['L-1-26-5-OP'] = viajes['M-CS']['L-1-26-5-OP']
viajes_alternativas_procesados_p['M-CS']['L-1-26-5-OP'] = viajes_alternativas_procesados['M-CS']['L-1-26-5-OP']
viajes_alternativas_desaglosadas_procesados_p['M-CS']['L-1-26-5-OP'] = viajes_alternativas_desaglosadas_procesados['M-CS']['L-1-26-5-OP']

viajes_labeling_shortest_alternativas_desaglosadas_procesados_p['M-CS']['L-1-26-5-OP'] = viajes_labeling_shortest_alternativas_desaglosadas_procesados['M-CS']['L-1-26-5-OP']
viajes_labeling_shortest_alternativas_procesados_p['M-CS']['L-1-26-5-OP'] = viajes_labeling_shortest_alternativas_procesados['M-CS']['L-1-26-5-OP']

print(viajes_alternativas_procesados_p['M-CS']['L-1-26-5-OP'])

print(viajes_labeling_shortest_alternativas_desaglosadas_procesados_p['M-CS']['L-1-26-5-OP'])

viajes_link_elimination_shortest_alternativas_desaglosadas_procesados_prediccion_p['L-13-96-20-OP']['L-17-16-30-NS'] = viajes_link_elimination_shortest_alternativas_desaglosadas_procesados['L-13-96-20-OP']['L-17-16-30-NS']
viajes_link_elimination_shortest_alternativas_procesados_prediccion_p['L-13-96-20-OP']['L-17-16-30-NS'] = viajes_link_elimination_shortest_alternativas_procesados['L-13-96-20-OP']['L-17-16-30-NS']

viajes = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
viajes = viajes_p

viajes_alternativas_procesados = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
viajes_alternativas_procesados = viajes_alternativas_procesados_p

viajes_alternativas_desaglosadas_procesados = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
viajes_alternativas_desaglosadas_procesados = viajes_alternativas_desaglosadas_procesados_p

viajes_link_elimination_shortest_alternativas_procesados = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
viajes_link_elimination_shortest_alternativas_procesados = viajes_link_elimination_shortest_alternativas_procesados_p

viajes_link_elimination_shortest_alternativas_desaglosadas_procesados = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
viajes_link_elimination_shortest_alternativas_desaglosadas_procesados = viajes_link_elimination_shortest_alternativas_desaglosadas_procesados_p

viajes_link_elimination_shortest_alternativas_procesados_prediccion = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
viajes_link_elimination_shortest_alternativas_procesados_prediccion = viajes_link_elimination_shortest_alternativas_procesados_prediccion_p

viajes_link_elimination_shortest_alternativas_desaglosadas_procesados_prediccion = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
viajes_link_elimination_shortest_alternativas_desaglosadas_procesados_prediccion = viajes_link_elimination_shortest_alternativas_desaglosadas_procesados_prediccion_p

'''
def alternativas_maximas(diccionario):
    cant_max_alternativas_observadas = 0
    for o in diccionario:
        for d in diccionario[o]:
            largo_camino = len(diccionario[o][d])
            if largo_camino > cant_max_alternativas_observadas:
                cant_max_alternativas_observadas = largo_camino
    return cant_max_alternativas_observadas


###procesamiento para hacer resumen de todos los tipos de conjunto de consideracion excepto el de hyper-ruta que esta hecho en otro apartado
def resumen(diccionario_conj, direccion_csv, diccionario_viajes):
    with open(direccion_csv, 'wb') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(
            ['origen', 'destino', 'total_viajes', 'viajes_conj_generado', 'largo_conj_generado',
             'largo_caminos_usados', 'alt_viajes_en_conj', 'alt_conj_en_viajes'])

        for destino in diccionario_viajes:
            for ori in diccionario_viajes[destino]:

                total_viajes = 0
                viajes_en_k_rutas_minimas = 0
                alt_viajes_en_conj = 0
                alt_conj_en_viajes = 0
                largo_k_rutas_minimas = len(diccionario_conj[ori][destino])
                caminos_viajes = []

                largo_caminos_usados = len(diccionario_viajes[destino][ori])

                for camino in diccionario_viajes[destino][ori]:
                    n_viajes = diccionario_viajes[destino][ori][camino]
                    total_viajes += n_viajes
                    caminos_viajes.append(camino)

                    if camino in diccionario_conj[ori][destino]:
                        viajes_en_k_rutas_minimas += n_viajes
                        alt_viajes_en_conj += 1

                if ori in diccionario_conj and destino in diccionario_conj[ori]:
                    for camino in diccionario_conj[ori][destino]:
                        if camino in caminos_viajes:
                            alt_conj_en_viajes += 1


                row = [ori, destino, total_viajes, viajes_en_k_rutas_minimas, largo_k_rutas_minimas,
                       largo_caminos_usados, alt_viajes_en_conj, alt_conj_en_viajes]

                writer.writerow(row)


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
###conjunto de consideracion para alternativas observadas###
'''
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
                                            paraderos_coord_dic, viajes_alternativas_procesados,dict_servicio_llave_usuario, g_metro, '2', PS_correlacion,
                                            viajes_alternativas_procesados, viajes_alternativas_desaglosadas_procesados)

'''
###conjunto de consideracion para simulacion###
'''
PS = process_frame_alt(viajes_simulation_shortest_alternativas_desaglosadas_procesados, g)

PS_correlacion = correlacion(df, PS, dict_tiempos)


Consideration_set_obj = Consideration_set(viajes_simulation_shortest_alternativas_desaglosadas_procesados))

Consideration_set_obj.get_consideration_set(g, viajes_simulation_shortest_alternativas_desaglosadas_procesados, viajes, dict_tiempos, dict_frecuencia,
                                            paraderos_coord_dic, viajes_simulation_shortest_alternativas_procesados, dict_servicio_llave_usuario, g_metro, '3', PS_correlacion, viajes_alternativas_procesados, viajes_alternativas_desaglosadas_procesados)
'''

###conjunto de consideracion para simulacion with observed parameters###
'''
PS = process_frame_alt(viajes_simulation_shortest_alternativas_desaglosadas_procesados_observed_parameters, g)

PS_correlacion = correlacion(df, PS, dict_tiempos)


Consideration_set_obj = Consideration_set(viajes_simulation_shortest_alternativas_desaglosadas_procesados_observed_parameters))

Consideration_set_obj.get_consideration_set(g, viajes_simulation_shortest_alternativas_desaglosadas_procesados_observed_parameters, viajes, dict_tiempos, dict_frecuencia,
                                            paraderos_coord_dic, viajes_simulation_shortest_alternativas_procesados_observed_parameters, dict_servicio_llave_usuario, g_metro, '3', PS_correlacion, viajes_alternativas_procesados, viajes_alternativas_desaglosadas_procesados)
'''

###conjunto de consideracion para k rutas minimas###
'''
PS = process_frame_alt(viajes_k_shortest_alternativas_desaglosadas_procesados, g)

PS_correlacion = correlacion(df, PS, dict_tiempos)


Consideration_set_obj = Consideration_set(alternativas_maximas(viajes_k_shortest_alternativas_desaglosadas_procesados))

Consideration_set_obj.get_consideration_set(g, viajes_k_shortest_alternativas_desaglosadas_procesados, viajes, dict_tiempos, dict_frecuencia,
                                            paraderos_coord_dic, viajes_k_shortest_alternativas_procesados, dict_servicio_llave_usuario, g_metro, '3', PS_correlacion, viajes_alternativas_procesados, viajes_alternativas_desaglosadas_procesados)
'''
###conjunto de consideracion para k rutas minimas_observed_parameters###

PS = process_frame_alt(viajes_k_shortest_alternativas_desaglosadas_procesados_observed_parameters, g)

PS_correlacion = correlacion(df, PS, dict_tiempos)


Consideration_set_obj = Consideration_set(alternativas_maximas(viajes_k_shortest_alternativas_desaglosadas_procesados_observed_parameters))

Consideration_set_obj.get_consideration_set(g, viajes_k_shortest_alternativas_desaglosadas_procesados_observed_parameters, viajes, dict_tiempos, dict_frecuencia,
                                            paraderos_coord_dic, viajes_k_shortest_alternativas_procesados_observed_parameters, dict_servicio_llave_usuario, g_metro, '3', PS_correlacion, viajes_alternativas_procesados, viajes_alternativas_desaglosadas_procesados)
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
                                            paraderos_coord_dic, viajes_prediccion_alternativas_procesados,dict_servicio_llave_usuario, g_metro, '4', PS_correlacion,
                                            viajes_prediccion_procesados, viajes_prediccion_alternativas_desaglosadas_procesados)
'''

'''
###conjunto de consideracion para labeling###

PS = process_frame_alt(viajes_labeling_shortest_alternativas_desaglosadas_procesados, g)

PS_correlacion = correlacion(df, PS, dict_tiempos)

print("correlation calculada")

print(alternativas_maximas(viajes_labeling_shortest_alternativas_desaglosadas_procesados))

Consideration_set_obj = Consideration_set(alternativas_maximas(viajes_labeling_shortest_alternativas_desaglosadas_procesados))

Consideration_set_obj.get_consideration_set(g, viajes_labeling_shortest_alternativas_desaglosadas_procesados, viajes, dict_tiempos, dict_frecuencia,
                                            paraderos_coord_dic, viajes_labeling_shortest_alternativas_procesados, dict_servicio_llave_usuario, g_metro, '5', PS_correlacion, viajes_alternativas_procesados, viajes_alternativas_desaglosadas_procesados)

#resumen

resumen(viajes_labeling_shortest_alternativas_procesados, 'outputs\\resumen_labeling.csv', viajes)
'''
###conjunto de consideracion para labeling_observed_parameters###
'''
PS = process_frame_alt(viajes_labeling_shortest_alternativas_desaglosadas_procesados_observed_parameters, g)

PS_correlacion = correlacion(df, PS, dict_tiempos)


Consideration_set_obj = Consideration_set(alternativas_maximas(viajes_labeling_shortest_alternativas_desaglosadas_procesados_observed_parameters))

Consideration_set_obj.get_consideration_set(g, viajes_labeling_shortest_alternativas_desaglosadas_procesados_observed_parameters, viajes, dict_tiempos, dict_frecuencia,
                                            paraderos_coord_dic, viajes_labeling_shortest_alternativas_procesados_observed_parameters, dict_servicio_llave_usuario, g_metro, '5', PS_correlacion, viajes_alternativas_procesados, viajes_alternativas_desaglosadas_procesados)

#resumen

resumen(viajes_labeling_shortest_alternativas_procesados, 'outputs\\resumen_labeling.csv', viajes)
'''
'''

###conjunto de consideracion para link penalty###

PS = process_frame_alt(viajes_link_penalty_shortest_alternativas_desaglosadas_procesados, g)

PS_correlacion = correlacion(df, PS, dict_tiempos)


Consideration_set_obj = Consideration_set(alternativas_maximas(viajes_link_penalty_shortest_alternativas_desaglosadas_procesados))

Consideration_set_obj.get_consideration_set(g, viajes_link_penalty_shortest_alternativas_desaglosadas_procesados, viajes, dict_tiempos, dict_frecuencia,
                                            paraderos_coord_dic, viajes_link_penalty_shortest_alternativas_procesados, dict_servicio_llave_usuario, g_metro, '6', PS_correlacion, viajes_alternativas_procesados, viajes_alternativas_desaglosadas_procesados)

#resumen

resumen(viajes_link_penalty_shortest_alternativas_procesados, 'outputs\\resumen_link_penalty.csv', viajes)
'''

###conjunto de consideracion para link penalty_observed_parameters###
'''
PS = process_frame_alt(viajes_link_penalty_shortest_alternativas_desaglosadas_procesados_observed_parameters, g)

PS_correlacion = correlacion(df, PS, dict_tiempos)


Consideration_set_obj = Consideration_set(alternativas_maximas(viajes_link_penalty_shortest_alternativas_desaglosadas_procesados_observed_parameters))

Consideration_set_obj.get_consideration_set(g, viajes_link_penalty_shortest_alternativas_desaglosadas_procesados_observed_parameters, viajes, dict_tiempos, dict_frecuencia,
                                            paraderos_coord_dic, viajes_link_penalty_shortest_alternativas_procesados_observed_parameters, dict_servicio_llave_usuario, g_metro, '6', PS_correlacion, viajes_alternativas_procesados, viajes_alternativas_desaglosadas_procesados)

#resumen

resumen(viajes_link_penalty_shortest_alternativas_procesados, 'outputs\\resumen_link_penalty.csv', viajes)
'''

'''
###conjunto de consideracion para link elimination###

PS = process_frame_alt(viajes_link_elimination_shortest_alternativas_desaglosadas_procesados, g)

PS_correlacion = correlacion(df, PS, dict_tiempos)

Consideration_set_obj = Consideration_set(alternativas_maximas(viajes_link_elimination_shortest_alternativas_desaglosadas_procesados))

alternativa_observada = True

viajes_copia = copy.deepcopy(viajes)

Consideration_set_obj.get_consideration_set(g, viajes_link_elimination_shortest_alternativas_desaglosadas_procesados, viajes_copia, dict_tiempos, dict_frecuencia,
                                            paraderos_coord_dic, viajes_link_elimination_shortest_alternativas_procesados, dict_servicio_llave_usuario, g_metro, '7', PS_correlacion,
                                            viajes_alternativas_procesados, viajes_alternativas_desaglosadas_procesados)

#resumen

resumen(viajes_link_elimination_shortest_alternativas_procesados, 'outputs\\resumen_link_elimination.csv', viajes)

'''
'''
###conjunto de consideracion para link elimination_observed_parameters###

PS = process_frame_alt(viajes_link_elimination_shortest_alternativas_desaglosadas_procesados_observed_parameters, g)

PS_correlacion = correlacion(df, PS, dict_tiempos)

Consideration_set_obj = Consideration_set(alternativas_maximas(viajes_link_elimination_shortest_alternativas_desaglosadas_procesados_observed_parameters))

alternativa_observada = True

viajes_copia = copy.deepcopy(viajes)

Consideration_set_obj.get_consideration_set(g, viajes_link_elimination_shortest_alternativas_desaglosadas_procesados_observed_parameters, viajes_copia, dict_tiempos, dict_frecuencia,
                                            paraderos_coord_dic, viajes_link_elimination_shortest_alternativas_procesados_observed_parameters, dict_servicio_llave_usuario, g_metro, '7', PS_correlacion,
                                            viajes_alternativas_procesados, viajes_alternativas_desaglosadas_procesados)

#resumen

resumen(viajes_link_elimination_shortest_alternativas_procesados_observed_parameters, 'outputs\\resumen_link_elimination_observed_parameters.csv', viajes)
'''
'''
#prediccion_link_elimination

print('viajes_link_elimination_shortest_alternativas_desaglosadas_procesados_prediccion', viajes_link_elimination_shortest_alternativas_desaglosadas_procesados_prediccion)
PS = process_frame_alt(viajes_link_elimination_shortest_alternativas_desaglosadas_procesados_prediccion, g)

PS_correlacion = correlacion(df, PS, dict_tiempos)

Consideration_set_obj = Consideration_set(alternativas_maximas(viajes_link_elimination_shortest_alternativas_desaglosadas_procesados_prediccion))

alternativa_observada = False

Consideration_set_obj.get_consideration_set(g, viajes_link_elimination_shortest_alternativas_desaglosadas_procesados_prediccion, viajes_prediccion_procesados, dict_tiempos, dict_frecuencia,
                                            paraderos_coord_dic, viajes_link_elimination_shortest_alternativas_procesados_prediccion, dict_servicio_llave_usuario, g_metro, '8', PS_correlacion, alternativa_observada, viajes_alternativas_procesados, viajes_alternativas_desaglosadas_procesados)

'''