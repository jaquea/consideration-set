from collections import defaultdict
import csv

from hyperpath import Hyperpath

class Files:
    def __init__(self, archivo_viajes, grafo, paradero_cercano_dic, dict_servicio_llave_codigoTS):
        self.g = grafo
        self.viajes = archivo_viajes
        self.paradero_cercano_dic = paradero_cercano_dic
        self.dict_servicio_llave_codigoTS = dict_servicio_llave_codigoTS

    def hyperpath_from_travel_file(self, dict_tiempos, dict_frecuencia):

        hiperruta_minimo = defaultdict(lambda: defaultdict(list))
        hiperruta_minimo_camino_desglosado = defaultdict(lambda: defaultdict(list))
        cant_max_alternativas_hiperruta = 0

        cont = 0

        with open('outputs\\resumen.csv', 'wb') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(
                ['origen', 'destino', 'total_viajes', 'viajes_en_hiperruta', 'viajes_en_ruta_min', 'viajes_en_it_min',
                 'largo_hiperruta', 'largo_ruta_minima', 'itinerarios_minimos', 'largo_caminos_usados',
                 'p_correcta_itinerario_minimo', 'p_correcta_hiperruta', 'p_correcta_ruta_minima'])

            for destino in self.viajes:
                cont += 1
                print(destino, cont)
                hyperpath_obj = Hyperpath(self.g, destination=destino, transfer_penalty=16, waiting_penalty=2,
                                          paradero_cercano_dic=self.paradero_cercano_dic, dict_servicio_llave_codigoTS=self.dict_servicio_llave_codigoTS)

                for ori in self.viajes[destino]:

                    viajes_en_it_min = 0
                    viajes_en_hiperruta = 0
                    viajes_en_ruta_min = 0
                    total_viajes = 0

                    p_correcta_itinerario_minimo = 0
                    p_correcta_hiperruta = 0
                    p_correcta_ruta_minima = 0

                    Dict_caminos, hiperruta_minimo_pre, hiperruta_proporcion, hiperruta_minimo_camino_desglosado_pre = hyperpath_obj.get_elemental_paths(ori, destino)

                    itinerario_minimo, itinerario_minimo_proporcion = hyperpath_obj.get_all_shortest_paths(ori, hiperruta_proporcion)
                    Dict_caminos_etapa = hyperpath_obj.get_services_per_stages(ori)
                    ruta_minima, ruta_minima_proporcion = hyperpath_obj.get_aggregate_paths(ori, Dict_caminos,
                                                                                   Dict_caminos_etapa,
                                                                                   dict_tiempos,
                                                                                   dict_frecuencia,
                                                                                   hiperruta_proporcion)

                    hiperruta_minimo[ori][destino] = hiperruta_minimo_pre[ori][destino]
                    hiperruta_minimo_camino_desglosado[ori][destino] = hiperruta_minimo_camino_desglosado_pre[ori][destino]
                    itinerarios_minimos = itinerario_minimo[ori][destino]
                    largo_hiperruta = len(hiperruta_minimo_pre[ori][destino])
                    largo_caminos_usados = len(self.viajes[destino][ori])
                    largo_ruta_minima = len(ruta_minima[ori][destino])

                    if largo_hiperruta > cant_max_alternativas_hiperruta:
                        cant_max_alternativas_hiperruta = largo_hiperruta

                    for camino in self.viajes[destino][ori]:
                        n_viajes = self.viajes[destino][ori][camino]
                        total_viajes += n_viajes

                    for camino in self.viajes[destino][ori]:
                        n_viajes = self.viajes[destino][ori][camino]
                        p_o = float(n_viajes) / float(total_viajes)

                        if camino in itinerario_minimo[ori][destino]:
                            viajes_en_it_min += n_viajes

                            p_e = itinerario_minimo_proporcion[ori][destino][camino]
                            p_correcta_itinerario_minimo += min(p_e, p_o)

                        if camino in hiperruta_minimo_pre[ori][destino]:
                            viajes_en_hiperruta += n_viajes

                            p_e = hiperruta_proporcion[ori][destino][camino]
                            p_correcta_hiperruta += min(p_e, p_o)

                        if camino in ruta_minima[ori][destino]:
                            viajes_en_ruta_min += n_viajes

                            p_e = ruta_minima_proporcion[ori][destino][camino]
                            p_correcta_ruta_minima += min(p_e, p_o)

                    row = [ori, destino, total_viajes, viajes_en_hiperruta, viajes_en_ruta_min, viajes_en_it_min,
                           largo_hiperruta, largo_ruta_minima, itinerarios_minimos, largo_caminos_usados,
                           p_correcta_itinerario_minimo, p_correcta_hiperruta, p_correcta_ruta_minima]

                    writer.writerow(row)

        print('hiperruta_minimo', hiperruta_minimo)
        return hiperruta_minimo_camino_desglosado, cant_max_alternativas_hiperruta, hiperruta_minimo

    def real_trips(self):

        with open('outputs\\viajes_realizados_c.csv', mode='wb') as csvFile:
            writer = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['origen', 'destino', 'camino', 'viajes'])

            for destino in self.viajes:
                for origen in self.viajes[destino]:
                    for camino in self.viajes[destino][origen]:
                        writer = csv.writer(csvFile)
                        writer.writerow([origen, destino, camino, self.viajes[destino][origen][camino]])