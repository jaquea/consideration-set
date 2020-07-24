import pandas as pd


class Consideration_set:
    def __init__(self, cant_max_alternativas):
        self.cant_max_alternativas = cant_max_alternativas

    def get_consideration_set(self, hiperruta_minimo, alternativas_ele_hip, viajes):

        posicion = 0
        resultado = pd.DataFrame()

        while posicion <= (self.cant_max_alternativas - 1):

            lista = []

            for o in hiperruta_minimo:
                for d in hiperruta_minimo[o]:
                    # si hay mas caminos que el marcador posicion se agrega c, el camino
                    if len(hiperruta_minimo[o][d]) > posicion:
                        c = hiperruta_minimo[o][d][posicion]
                        lista.append(alternativas_ele_hip[c])
                    else:
                        lista.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

            cont = posicion + 1

            headers = [''.join(['AVAIL', unicode(cont)]), ''.join(['CAMINO', unicode(cont)]),
                       ''.join(['VIAJES', unicode(cont)]), ''.join(['TPOMETRO', unicode(cont)]),
                       ''.join(['TPOBUS', unicode(cont)]), ''.join(['TPOCAM', unicode(cont)]),
                       ''.join(['TESPINC', unicode(cont)]), ''.join(['TESPINT', unicode(cont)]),
                       ''.join(['BUS_METRO', unicode(cont)]), ''.join(['BUS_BUS', unicode(cont)]),
                       ''.join(['METRO_BUS', unicode(cont)])]

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

        contador_viajes = resultado['VIAJES1']
        for i in range(self.cant_max_alternativas):
            contador_viajes += resultado[''.join(['VIAJES', unicode(i+1)])]

        contador_viajes = contador_viajes - resultado['VIAJES1']

        new_df = resultado.loc[resultado.index.repeat(contador_viajes)].reset_index(drop=True)

        contador = 0

        for i in range(self.cant_max_alternativas):
            new_df[''.join(['CHOICE', unicode(i + 1)])] = 0

        for index, row in resultado.iterrows():
            viajes1 = row['VIAJES1']
            viajes2 = row['VIAJES2']
            viajes3 = row['VIAJES3']
            viajes4 = row['VIAJES4']
            viajes5 = row['VIAJES5']
            viajes6 = row['VIAJES6']
            viajes7 = row['VIAJES7']
            viajes8 = row['VIAJES8']
            viajes9 = row['VIAJES9']

            lista_viajes = [viajes1, viajes2, viajes3, viajes4, viajes5, viajes6, viajes7, viajes8, viajes9]

            choice = 1
            for l in lista_viajes:
                cont = choice
                choice += 1
                for i in range(l):
                    new_df.at[i + contador, ''.join(['CHOICE', unicode(cont)])] = 1
                contador += l

        new_df.to_csv("outputs\\alternativas_elementales_hiperruta.csv", encoding='utf-8', index=False, sep=',')