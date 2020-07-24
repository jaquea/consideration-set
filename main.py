import pickle
from collections import defaultdict

import dill

from atributes_alternatives import Atributes
from hyperpath import Hyperpath

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

viajes_p = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
viajes_p['M-TB']['T-20-200-SN-25'] = viajes['M-TB']['T-20-200-SN-25']

viajes = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0)))
viajes = viajes_p

# genero y leo grafo
dump_file1 = open('tmp\\grafo.igraph', 'rb')
g = pickle.load(dump_file1)
dump_file1.close()

dump_file2 = open('tmp\\paradero_cercano_dic.pkl', 'rb')
paradero_cercano_dic = dill.load(dump_file2)
dump_file2.close()
'''
with open('tmp\\resumen.csv', mode='w') as csvFile:
    writer = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['origen', 'destino', 'total_viajes', 'viajes_en_hiperruta', 'viajes_en_ruta_min', 'viajes_en_it_min', 'largo_hiperruta', 'largo_ruta_minima', 'itinerarios_minimos', 'largo_caminos_usados', 'p_correcta_itinerario_minimo', 'p_correcta_hiperruta', 'p_correcta_ruta_minima'])
'''

alternativas_ele_hip = defaultdict(list)
cant_max_alternativas = 0

cont = 0
for destino in viajes:
    cont += 1
    print(destino, cont)

    hyperpath_obj = Hyperpath(g, destination=destino, transfer_penalty=16,
                              waiting_penalty=2)

    for ori in viajes[destino]:

        viajes_en_it_min = 0
        viajes_en_hiperruta = 0
        viajes_en_ruta_min = 0
        total_viajes = 0

        p_correcta_itinerario_minimo = 0
        p_correcta_hiperruta = 0
        p_correcta_ruta_minima = 0

        Dict_caminos, hiperruta_minimo, hiperruta_proporcion = hyperpath_obj.get_elemental_paths(ori, destino,
                                                                                                 paradero_cercano_dic)
        itinerario_minimo, itinerario_minimo_proporcion = hyperpath_obj.get_all_shortest_paths(ori,
                                                                                               paradero_cercano_dic,
                                                                                               hiperruta_proporcion)
        Dict_caminos_etapa = hyperpath_obj.get_services_per_stages(ori, paradero_cercano_dic)
        ruta_minima, ruta_minima_proporcion = hyperpath_obj.get_aggregate_paths(ori, Dict_caminos, Dict_caminos_etapa,
                                                                                dict_tiempos, dict_frecuencia,
                                                                                hiperruta_proporcion)

        print('hiperruta_minimo', hiperruta_minimo)
        itinerarios_minimos = itinerario_minimo[ori][destino]
        largo_hiperruta = len(hiperruta_minimo[ori][destino])
        largo_caminos_usados = len(viajes[destino][ori])
        largo_ruta_minima = len(ruta_minima[ori][destino])

        if largo_hiperruta > cant_max_alternativas:
            cant_max_alternativas = largo_hiperruta

        for camino in viajes[destino][ori]:
            n_viajes = viajes[destino][ori][camino]
            total_viajes += n_viajes

        for camino in viajes[destino][ori]:
            n_viajes = viajes[destino][ori][camino]
            p_o = float(n_viajes) / float(total_viajes)

            if camino in itinerario_minimo[ori][destino]:
                viajes_en_it_min += n_viajes

                p_e = itinerario_minimo_proporcion[ori][destino][camino]
                p_correcta_itinerario_minimo += min(p_e, p_o)

            if camino in hiperruta_minimo[ori][destino]:
                viajes_en_hiperruta += n_viajes

                p_e = hiperruta_proporcion[ori][destino][camino]
                p_correcta_hiperruta += min(p_e, p_o)

                atributos_obj = Atributes(camino, g)
                lista_atributos = atributos_obj.get_atributes(dict_tiempos, dict_frecuencia, paraderos_coord_dic)

                alternativas_ele_hip[camino] = [1, camino, viajes[destino][ori][camino]] + lista_atributos

                print([1, camino, viajes[destino][ori][camino]] + lista_atributos)

            if camino in ruta_minima[ori][destino]:
                viajes_en_ruta_min += n_viajes

                p_e = ruta_minima_proporcion[ori][destino][camino]
                p_correcta_ruta_minima += min(p_e, p_o)
'''
        with io.open('tmp\\resumen.csv', 'a', newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([ori, destino, total_viajes, viajes_en_hiperruta, viajes_en_ruta_min, viajes_en_it_min,
                         largo_hiperruta, largo_ruta_minima, itinerarios_minimos, largo_caminos_usados,
                         p_correcta_itinerario_minimo, p_correcta_hiperruta, p_correcta_ruta_minima])
csvFile.close()
'''
