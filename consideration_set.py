import pandas as pd

from atributes_alternatives import Atributes


class Consideration_set:
    def __init__(self, cant_max_alternativas):
        self.cant_max_alternativas = cant_max_alternativas

    def get_consideration_set(self, g, hiperruta_minimo_desglosada, viajes, dict_tiempos, dict_frecuencia, paraderos_coord_dic,  hiperruta_minimo, dict_servicio_llave_usuario, g_metro):

        posicion = 0
        resultado = pd.DataFrame()

        while posicion <= (self.cant_max_alternativas - 1):

            lista = []

            for o in hiperruta_minimo:
                for d in hiperruta_minimo[o]:
                    # si hay mas caminos que el marcador posicion se agrega c, el camino
                    if len(hiperruta_minimo[o][d]) > posicion:
                        c = hiperruta_minimo_desglosada[o][d][posicion]
                        c_no_desglosado = hiperruta_minimo[o][d][posicion]

                        atributos_obj = Atributes(c, g, g_metro)
                        lista_atributos = atributos_obj.get_atributes(dict_tiempos, dict_frecuencia,
                                                                      paraderos_coord_dic, dict_servicio_llave_usuario)

                        alternativas_ele_hip = [1, c_no_desglosado, viajes[d][o][c_no_desglosado]] + lista_atributos

                        lista.append(alternativas_ele_hip)
                    else:
                        lista.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            cont = posicion + 1

            headers = [''.join(['AVAIL', unicode(cont)]), ''.join(['CAMINO', unicode(cont)]),
                       ''.join(['VIAJES', unicode(cont)]), ''.join(['TPOMETRO', unicode(cont)]),
                       ''.join(['TPOBUS', unicode(cont)]), ''.join(['TPOCAM', unicode(cont)]),
                       ''.join(['TESPINC', unicode(cont)]), ''.join(['TESPINT', unicode(cont)]),
                       ''.join(['BUS_METRO', unicode(cont)]), ''.join(['BUS_BUS', unicode(cont)]),
                       ''.join(['METRO_BUS', unicode(cont)]), ''.join(['HACIN_METRO', unicode(cont)]),
                       ''.join(['METRO_METRO', unicode(cont)]), ''.join(['HACIN_ANDEN', unicode(cont)])]

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

        for i in range(self.cant_max_alternativas):
            new_df[''.join(['CHOICE', unicode(i + 1)])] = 0

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

        new_df.to_csv("outputs\\alternativas_elementales_hiperruta_c.csv", encoding='utf-8', index=False, sep=',')
