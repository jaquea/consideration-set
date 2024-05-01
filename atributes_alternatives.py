from igraph import *

class Atributes:
    def __init__(self, camino, grafo, g_metro):
        self.camino = camino
        self.g = grafo
        self.tpo_metro = 0
        self.tpo_bus = 0
        self.tpo_caminata_trasbordo = 0
        self.tpo_espera_inicial = 0
        self.tpo_espera_inicial_bus = 0
        self.tpo_espera_inicial_metro = 0
        self.tpo_espera_trasbordo = 0
        self.tpo_espera_trasbordo_bus = 0
        self.tpo_espera_trasbordo_metro = 0
        self.trasbordo_bus_metro = 0
        self.trasbordo_bus_bus = 0
        self.trasbordo_metro_bus = 0
        self.hacinamiento_metro = 0
        self.n_trasbordo_metro = 0
        self.hacinamiento_anden = 0
        self.g_metro = g_metro

    def hacinamiento_metro_metodo(self, n, nodo_anterior_anterior, nodo_anterior, dict_tiempos):

        if n[:2] == 'M-' and nodo_anterior_anterior[:2] == 'M-':

            str1 = nodo_anterior + 'V-I'
            str2 = nodo_anterior + 'V-R'
            str3 = nodo_anterior + 'R-I'
            str4 = nodo_anterior + 'R-R'
            str5 = nodo_anterior + '-I'
            str6 = nodo_anterior + '-R'

            servicios = [str1, str2, str3, str4, str5, str6]
            contador = 0
            suma_n_trasbordo_metro = 0

            for str in servicios:

                serv_dict_hacinamiento = str[:2]+str[-2:]

                if str in dict_tiempos:
                    dif = dict_tiempos[str][n] - dict_tiempos[str][nodo_anterior_anterior]

                    if dif > 0 and dict_tiempos[str][n] > -1 and dict_tiempos[str][nodo_anterior_anterior] > -1:
                        #max_carga_al_salir_el_tren = max([dict_hacinamiento_metro[serv_dict_hacinamiento][metro][0] for metro in dict_hacinamiento_metro[serv_dict_hacinamiento]])
                        #max_carga_en_anden = max([dict_hacinamiento_metro[serv_dict_hacinamiento][metro][1] for metro in dict_hacinamiento_metro[serv_dict_hacinamiento]])
                        #suma_hacinamiento_metro += float(dict_hacinamiento_metro[serv_dict_hacinamiento][nodo_anterior_anterior][0])/max_carga_al_salir_el_tren
                        #suma_hacinamiento_anden += float(dict_hacinamiento_metro[serv_dict_hacinamiento][nodo_anterior_anterior][1])/1
                        suma_n_trasbordo_metro += 1
                        contador += 1.0

            if contador > 0:
                #self.hacinamiento_metro += float(suma_hacinamiento_metro)/contador
                self.n_trasbordo_metro += float(suma_n_trasbordo_metro)/contador
                #self.hacinamiento_anden += float(suma_hacinamiento_anden)/contador


    def tpo_viaje_espera(self, n, nodo_anterior, tipo_nodo_actual, tipo_nodo_anterior, tipo_nodo_anterior_anterior, nodo_anterior_anterior, dict_tiempos, dict_frecuencia,dict_servicio_llave_usuario):

        if tipo_nodo_actual == tipo_nodo_anterior_anterior and tipo_nodo_anterior == 'servicio' and tipo_nodo_actual == 'paradero':

            # si es arco en metro
            if n[:2] == 'M-' and nodo_anterior_anterior[:2] == 'M-':
                n_destino = self.g_metro.vs.find(name2=n).index
                n_origen = self.g_metro.vs.find(name2=nodo_anterior_anterior).index

                # calcular tiempo de espera y tiempo de viaje en metro
                str1 = nodo_anterior + 'V-I'
                str2 = nodo_anterior + 'V-R'
                str3 = nodo_anterior + 'R-I'
                str4 = nodo_anterior + 'R-R'
                str5 = nodo_anterior + '-I'
                str6 = nodo_anterior + '-R'

                servicios = [str1, str2, str3, str4, str5, str6]

                frecuencia = 0
                contador = 0

                for str in servicios:

                    if str in dict_tiempos:
                        dif = dict_tiempos[str][n] - dict_tiempos[str][nodo_anterior_anterior]
                        if dif > 0 and dict_tiempos[str][n] > -1 and dict_tiempos[str][nodo_anterior_anterior] > -1:
                            frecuencia += dict_frecuencia[str][nodo_anterior_anterior]
                            contador += 1

                if frecuencia > 0:
                    tpo_espera = contador / frecuencia

                else:
                    tpo_espera = 0

                tpo_viaje = self.g_metro.shortest_paths_dijkstra(source=n_origen, target=n_destino, weights=self.g_metro.es["peso"],mode=OUT)[0][0] - tpo_espera
                self.tpo_metro += tpo_viaje

                if self.tpo_espera_inicial == 0:
                    self.tpo_espera_inicial += tpo_espera
                    self.tpo_espera_inicial_metro += tpo_espera

                else:
                    self.tpo_espera_trasbordo += tpo_espera
                    self.tpo_espera_trasbordo_metro += tpo_espera

            # si es arco en bus
            else:
                tpo_bus_tmp = 0
                frecuencia_tmp = 0
                contador_servicios = 0
                for serviciosTS in dict_servicio_llave_usuario[nodo_anterior]:
                    diferencia_tiempo = (dict_tiempos[serviciosTS][n] - dict_tiempos[serviciosTS][nodo_anterior_anterior])
                    if diferencia_tiempo>0 and dict_tiempos[serviciosTS][n] > -1 and dict_tiempos[serviciosTS][nodo_anterior_anterior] > -1:
                        contador_servicios += 1
                        tpo_bus_tmp += (dict_tiempos[serviciosTS][n] - dict_tiempos[serviciosTS][nodo_anterior_anterior])
                        frecuencia_tmp += dict_frecuencia[serviciosTS][nodo_anterior_anterior]


                if contador_servicios > 0:
                    self.tpo_bus += tpo_bus_tmp/contador_servicios


                if frecuencia_tmp > 0:
                    tpo_espera = 1 / frecuencia_tmp

                else:
                    tpo_espera = 0

                if self.tpo_espera_inicial == 0:
                    self.tpo_espera_inicial += tpo_espera
                    self.tpo_espera_inicial_bus += tpo_espera

                else:
                    self.tpo_espera_trasbordo += tpo_espera
                    self.tpo_espera_trasbordo_bus += tpo_espera

    def tpo_caminata(self, n, paraderos_coord_dic, tipo_nodo_actual, tipo_nodo_anterior, nodo_anterior):

        if tipo_nodo_actual == tipo_nodo_anterior and tipo_nodo_actual == 'paradero':
            x1 = float(paraderos_coord_dic[n][0])
            y1 = float(paraderos_coord_dic[n][1])

            x2 = float(paraderos_coord_dic[nodo_anterior][0])
            y2 = float(paraderos_coord_dic[nodo_anterior][1])

            dist = abs(x1 - x2) + abs(y1 - y2)

            self.tpo_caminata_trasbordo += (dist * 60 / (1000 * 4))

    def get_atributes(self, dict_tiempos, dict_frecuencia, paraderos_coord_dic, dict_servicio_llave_usuario):

        lista = self.camino.split('/')

        tipo_nodo_anterior = ''
        tipo_nodo_anterior_anterior = ''
        nodo_anterior_anterior = ''
        nodo_anterior = ''
        modo_anterior = ''
        modo_actual = ''

        for n in lista:
            # si el nodo es un paradero
            if n in self.g.vs['name2'] and (self.g.vs["tipo"][self.g.vs.find(name2=n).index]) == 'paradero':
                tipo_nodo_actual = 'paradero'

            # si el nodo es un servicio
            else:
                tipo_nodo_actual = 'servicio'

                # trasbordo a metro
                if nodo_anterior[:2] == 'M-':
                    modo_actual = 'metro'

                    if modo_anterior == 'bus':
                        self.trasbordo_bus_metro += 1

                    elif modo_anterior == 'metro':
                        self.n_trasbordo_metro += 1

                # trasbordo a bus
                else:
                    modo_actual = 'bus'

                    if modo_anterior == 'bus':
                        self.trasbordo_bus_bus += 1

                    if modo_anterior == 'metro':
                        self.trasbordo_metro_bus += 1

            # tiempo de viaje en vehiculo

            self.tpo_viaje_espera(n, nodo_anterior, tipo_nodo_actual, tipo_nodo_anterior, tipo_nodo_anterior_anterior,
                             nodo_anterior_anterior, dict_tiempos, dict_frecuencia,dict_servicio_llave_usuario)

            # tiempo de caminata en trasbordo

            self.tpo_caminata(n, paraderos_coord_dic, tipo_nodo_actual, tipo_nodo_anterior, nodo_anterior)

            #self.hacinamiento_metro_metodo(n, nodo_anterior_anterior, nodo_anterior, dict_hacinamiento_metro, dict_tiempos)

            tipo_nodo_anterior_anterior = tipo_nodo_anterior
            tipo_nodo_anterior = tipo_nodo_actual

            nodo_anterior_anterior = nodo_anterior
            nodo_anterior = n

            modo_anterior = modo_actual

        #para contar trasbordos y no etapa en metro
        if self.n_trasbordo_metro > 0:
            self.n_trasbordo_metro = self.n_trasbordo_metro - 1

        return [self.tpo_metro, self.tpo_bus, self.tpo_caminata_trasbordo, self.tpo_espera_inicial, self.tpo_espera_trasbordo, self.trasbordo_bus_metro, self.trasbordo_bus_bus, self.trasbordo_metro_bus, self.n_trasbordo_metro, self.tpo_espera_inicial_bus, self.tpo_espera_inicial_metro, self.tpo_espera_trasbordo_bus, self.tpo_espera_trasbordo_metro]