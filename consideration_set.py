import pandas as pd

from atributes_alternatives import Atributes
from path_size import process_frame_alt, correlacion
from collections import defaultdict


class Consideration_set:
    def __init__(self, cant_max_alternativas):
        self.cant_max_alternativas = cant_max_alternativas

    def get_consideration_set(self, g, hiperruta_minimo_desglosada, viajes, dict_tiempos, dict_frecuencia, paraderos_coord_dic,  hiperruta_minimo, dict_servicio_llave_usuario, g_metro, numero, PS_correlacion, viajes_alternativas_procesados, viajes_alternativas_desaglosadas_procesados):

        posicion = 0
        resultado = pd.DataFrame()

        while posicion <= (self.cant_max_alternativas - 1):

            lista = []
            contador = 0

            for o in hiperruta_minimo:
                for d in hiperruta_minimo[o]:
                    contador += 1
                    # si hay mas caminos que el marcador posicion se agrega c, el camino
                    if len(hiperruta_minimo[o][d]) > posicion:
                        c = hiperruta_minimo_desglosada[o][d][posicion]
                        c_no_desglosado = hiperruta_minimo[o][d][posicion]

                        correlacion_camino = PS_correlacion[o][d][c]


                        atributos_obj = Atributes(c, g, g_metro)
                        lista_atributos = atributos_obj.get_atributes(dict_tiempos, dict_frecuencia,
                                                                      paraderos_coord_dic, dict_servicio_llave_usuario)

                        alternativas_ele_hip = [1, c_no_desglosado, viajes[d][o][c_no_desglosado]] + lista_atributos + [correlacion_camino, 0]

                        lista.append(alternativas_ele_hip)

                    else:
                        lista.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0])

            cont = posicion + 1

            headers = [''.join(['AVAIL', unicode(cont)]), ''.join(['CAMINO', unicode(cont)]),
                       ''.join(['VIAJES', unicode(cont)]), ''.join(['TPOMETRO', unicode(cont)]),
                       ''.join(['TPOBUS', unicode(cont)]), ''.join(['TPOCAM', unicode(cont)]),
                       ''.join(['TESPINC', unicode(cont)]), ''.join(['TESPINT', unicode(cont)]),
                       ''.join(['BUS_METRO', unicode(cont)]), ''.join(['BUS_BUS', unicode(cont)]),
                       ''.join(['METRO_BUS', unicode(cont)]), ''.join(['METRO_METRO', unicode(cont)]),
                       ''.join(['TESPINCBUS', unicode(cont)]), ''.join(['TESPINCMETRO', unicode(cont)]),
                       ''.join(['TESPINTBUS', unicode(cont)]), ''.join(['TESPINTMETRO', unicode(cont)]),
                       ''.join(['PSC', unicode(cont)]), ''.join(['CHOICE', unicode(cont)])]

            dataframe = pd.DataFrame(lista, columns=headers)
            resultado = pd.concat([resultado, dataframe], axis=1, sort=False)
            posicion += 1

        # Agrego los atributos de origen y destino
        lista = []
        for o in hiperruta_minimo:
            for d in hiperruta_minimo[o]:
                viajes_totales = sum([viajes[d][o][camino] for camino in viajes[d][o]])
                viajes_en_hiperruta = sum([viajes[d][o][camino] for camino in hiperruta_minimo[o][d]])
                lista.append([o, d, viajes_totales, viajes_en_hiperruta])
        dataframe = pd.DataFrame(lista, columns=['ORIGEN', 'DESTINO', 'viajes_totales', 'viajes_en_hiperruta'])
        resultado = pd.concat([resultado, dataframe], axis=1, sort=False)

        contador_viajes = 0
        for i in range(self.cant_max_alternativas):
            contador_viajes += resultado[''.join(['VIAJES', unicode(i + 1)])]

        new_df = resultado.loc[resultado.index.repeat(contador_viajes)].reset_index(drop=True)

        contador = 0

        for index, row in resultado.iterrows():

            lista_viajes = []

            for i in range(self.cant_max_alternativas):
                lista_viajes.append(row[''.join(['VIAJES', unicode(i + 1)])])

            choice = 1
            for l in lista_viajes:
                cont = choice
                choice += 1
                for i in range(l):
                    new_df.at[i + contador, ''.join(['CHOICE', unicode(cont)])] = 1
                contador += l

        if numero == '1':
            new_df.to_csv("outputs\\alternativas_elementales_hiperruta_v2.csv", encoding='utf-8', index=False, sep=',')

        if numero == '2':
            new_df.to_csv("outputs\\alternativas_elementales_observadas_v2.csv", encoding='utf-8', index=False, sep=',')

        if numero == '3':
            new_df.to_csv("outputs\\alternativas_elementales_k_rutas_minimas_v2.csv", encoding='utf-8', index=False,
                          sep=',')

        if numero == '4':
            new_df.to_csv("outputs\\alternativas_elementales_prediccion_v2.csv", encoding='utf-8', index=False, sep=',')

        if numero == '5':
            new_df.to_csv("outputs\\alternativas_elementales_labeling_v2.csv", encoding='utf-8', index=False, sep=',')

        if numero == '6':
            new_df.to_csv("outputs\\alternativas_elementales_link_penalty_v2.csv", encoding='utf-8', index=False, sep=',')

        if numero == '7':
            new_df.to_csv("outputs\\alternativas_elementales_link_elimination_v2.csv", encoding='utf-8', index=False,
                          sep=',')

        # conjunto con alternativa observada
        for o in viajes_alternativas_procesados:
            for d in viajes_alternativas_procesados[o]:
                if o not in hiperruta_minimo or d not in hiperruta_minimo[o]:
                    continue
                cont = len(hiperruta_minimo[o][d])
                for camino in viajes_alternativas_procesados[o][d]:
                    if camino not in hiperruta_minimo[o][d]:
                        posicion = viajes_alternativas_procesados[o][d].index(camino)
                        c = viajes_alternativas_desaglosadas_procesados[o][d][posicion]
                        c_no_desglosado = camino
                        correlacion_camino = PS_correlacion[o][d][c]
                        atributos_obj = Atributes(c, g, g_metro)
                        lista_atributos = atributos_obj.get_atributes(dict_tiempos, dict_frecuencia,
                                                                      paraderos_coord_dic,
                                                                      dict_servicio_llave_usuario)

                        alternativas_ele_hip = [1, c_no_desglosado,
                                                viajes[d][o][c_no_desglosado]] + lista_atributos + [
                                                   correlacion_camino, 0]

                        lista = alternativas_ele_hip

                        cont += 1

                        if cont > self.cant_max_alternativas:
                            self.cant_max_alternativas = cont

                        headers = [''.join(['AVAIL', unicode(cont)]), ''.join(['CAMINO', unicode(cont)]),
                                   ''.join(['VIAJES', unicode(cont)]), ''.join(['TPOMETRO', unicode(cont)]),
                                   ''.join(['TPOBUS', unicode(cont)]), ''.join(['TPOCAM', unicode(cont)]),
                                   ''.join(['TESPINC', unicode(cont)]), ''.join(['TESPINT', unicode(cont)]),
                                   ''.join(['BUS_METRO', unicode(cont)]), ''.join(['BUS_BUS', unicode(cont)]),
                                   ''.join(['METRO_BUS', unicode(cont)]), ''.join(['METRO_METRO', unicode(cont)]),
                                   ''.join(['TESPINCBUS', unicode(cont)]), ''.join(['TESPINCMETRO', unicode(cont)]),
                                   ''.join(['TESPINTBUS', unicode(cont)]), ''.join(['TESPINTMETRO', unicode(cont)]),
                                   ''.join(['PSC', unicode(cont)]), ''.join(['CHOICE', unicode(cont)])]

                        #dataframe = pd.DataFrame([lista], columns=headers)

                        #fila_agregar = resultado[(resultado['ORIGEN'] == o) & (resultado['DESTINO'] == d)]

                        # Iterate through both lists simultaneously and update or create attributes
                        for attribute, value in zip(headers, lista):
                            condition = (resultado['ORIGEN'] == o) & (resultado['DESTINO'] == d)
                            resultado.loc[condition, attribute] = value

                        # pegamos dataframes horizontalmente
                        #df_agregar = pd.concat([fila_agregar, dataframe], axis=1, sort=False)
                        #df_agregar = fila_agregar

        #contador_viajes = viajes[d][o][c_no_desglosado]
        #new_df_agregar = df_agregar.loc[df_agregar.index.repeat(contador_viajes)].reset_index(drop=True)

        #resultado.to_csv("outputs\\new_df_agregar.csv", encoding='utf-8', index=False, sep=',')

        #new_df = new_df.append(new_df_agregar, sort=False)

        # Replace NaN values with 0
        resultado.fillna(0, inplace=True)

        new_df = resultado.loc[resultado.index.repeat(resultado["viajes_totales"])].reset_index(drop=True)

        contador = 0

        for index, row in resultado.iterrows():

            lista_viajes = []

            for i in range(self.cant_max_alternativas):
                lista_viajes.append(row[''.join(['VIAJES', unicode(i + 1)])])

            choice = 1
            for l in lista_viajes:
                cont = choice
                choice += 1
                for i in range(int(l)):
                    new_df.at[i + contador, ''.join(['CHOICE', unicode(cont)])] = 1
                contador += l

        if numero == '1':
            new_df.to_csv("outputs\\alternativas_elementales_hiperruta_obs.csv", encoding='utf-8', index=False, sep=',')

        if numero == '2':
            new_df.to_csv("outputs\\alternativas_elementales_observadas_obs.csv", encoding='utf-8', index=False, sep=',')

        if numero == '3':
            new_df.to_csv("outputs\\alternativas_elementales_k_rutas_minimas_obs.csv", encoding='utf-8', index=False, sep=',')

        if numero == '4':
            new_df.to_csv("outputs\\alternativas_elementales_prediccion_obs.csv", encoding='utf-8', index=False, sep=',')

        if numero == '5':
            new_df.to_csv("outputs\\alternativas_elementales_labeling_obs.csv", encoding='utf-8', index=False, sep=',')

        if numero == '6':
            new_df.to_csv("outputs\\alternativas_elementales_link_penalty_obs.csv", encoding='utf-8', index=False, sep=',')

        if numero == '7':
            new_df.to_csv("outputs\\alternativas_elementales_link_elimination_obs.csv", encoding='utf-8', index=False, sep=',')


