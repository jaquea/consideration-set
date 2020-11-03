# coding=utf-8
# se debe ejecutar despues de proces_viajes.py
# se genera el archivo viajes procesados que permite entregar los viajes por par OD en base al radio de 100 mts por cada par de paraderos OD
import utm
import dill
from collections import defaultdict
import os
import pickle
import time

from constants import PROJECT_DIR

dump_file2 = open('tmp\\viajes_prediccion_reales.pkl', 'rb')
viajes_prediccion_reales = dill.load(dump_file2)
dump_file2.close()

dump_file1 = open('tmp\\viajes_prediccion_alternativas_desagregadas.pkl', 'rb')
viajes_prediccion_alternativas_desaglosadas = dill.load(dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\viajes_prediccion_alternativas.pkl', 'rb')
viajes_prediccion_alternativas = dill.load(dump_file1)
dump_file1.close()

dump_file1 = open('tmp\\viajes_alternativas_procesados.pkl', 'rb')
viajes_alternativas_procesados = dill.load(dump_file1)
dump_file1.close()

dump_file2 = open('tmp\\paradero_cercano_dic.pkl', 'rb')
paradero_cercano_dic = dill.load(dump_file2)
dump_file2.close()

print(len(viajes_prediccion_alternativas_desaglosadas))

viajes_prediccion_procesados = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
viajes_prediccion_alternativas_desaglosadas_procesados  = defaultdict(lambda: defaultdict(list))
viajes_prediccion_alternativas_procesados  = defaultdict(lambda: defaultdict(list))

cont = 0
for origen in viajes_alternativas_procesados:
    for destino in viajes_alternativas_procesados[origen]:
        cont +=1

        print('origen', origen, 'destino', destino)
        start_time = time.clock()
        grupo_subida = paradero_cercano_dic[origen]
        grupo_bajada = paradero_cercano_dic[destino]
        tuplas = [(x, y) for x in grupo_subida for y in grupo_bajada]

        for par in tuplas:
            if par[0] in viajes_prediccion_reales and par[1] in viajes_prediccion_reales[par[0]]:
                for camino in viajes_prediccion_reales[par[0]][par[1]]:
                    viajes_prediccion_procesados[destino][origen][camino] = viajes_prediccion_reales[par[0]][par[1]][camino]

                for camino in viajes_prediccion_alternativas_desaglosadas[par[0]][par[1]]:
                    if camino not in viajes_prediccion_alternativas_desaglosadas_procesados[origen][destino]:
                        viajes_prediccion_alternativas_desaglosadas_procesados[origen][destino].append(camino)

                for camino in viajes_prediccion_alternativas[par[0]][par[1]]:
                    if camino not in viajes_prediccion_alternativas_procesados[origen][destino]:
                        viajes_prediccion_alternativas_procesados[origen][destino].append(camino)

print(len(viajes_prediccion_alternativas_desaglosadas_procesados))
print(len(viajes_prediccion_alternativas_procesados))
dump_file2 = open('tmp\\viajes_prediccion_alternativas_desaglosadas_procesados.pkl', 'wb')
dill.dump(viajes_prediccion_alternativas_desaglosadas_procesados, dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_prediccion_alternativas_procesados.pkl', 'wb')
dill.dump(viajes_prediccion_alternativas_procesados, dump_file2)
dump_file2.close()

dump_file2 = open('tmp\\viajes_prediccion_procesados.pkl', 'wb')
dill.dump(viajes_prediccion_procesados, dump_file2)
dump_file2.close()


