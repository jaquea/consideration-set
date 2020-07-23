# -*- encoding: utf-8 -*-
import unittest

from igraph import *

from hyperpath import Hyperpath


class TestHyperpath(unittest.TestCase):

    def setUp(self):
        self.g = Graph(directed=True)
        # nodos paraderos
        self.g.add_vertex(name='1', name2='O', tipo='paradero')
        self.g.add_vertex(name='2', name2='T', tipo='paradero')
        self.g.add_vertex(name='3', name2='D', tipo='paradero')

        # nodos servicio que pasan por O
        self.g.add_vertex(name='4', name2='O/naranjo', tipo='servicio')
        self.g.add_vertex(name='5', name2='O/amarillo', tipo='servicio')
        self.g.add_vertex(name='6', name2='O/azul', tipo='servicio')
        self.g.add_vertex(name='7', name2='O/verde', tipo='servicio')
        self.g.add_vertex(name='8', name2='O/morado', tipo='servicio')

        # nodos servicio que pasan por T
        self.g.add_vertex(name='9', name2='T/naranjo', tipo='servicio')
        self.g.add_vertex(name='10', name2='T/amarillo', tipo='servicio')
        self.g.add_vertex(name='11', name2='T/azul', tipo='servicio')
        self.g.add_vertex(name='14', name2='T/rojo', tipo='servicio')

        # nodos servicio que pasan por D
        self.g.add_vertex(name='15', name2='D/verde', tipo='servicio')
        self.g.add_vertex(name='16', name2='D/morado', tipo='servicio')
        self.g.add_vertex(name='17', name2='D/rojo', tipo='servicio')

        #diccionario tiempo y frecuencia

        self.dict_tiempos = defaultdict(lambda: defaultdict(lambda: -1))
        self.dict_frecuencia = defaultdict(lambda: defaultdict(lambda: 0))

        self.dict_frecuencia['naranjo']['O'] = float(5.0/60)
        self.dict_frecuencia['naranjo']['T'] = float(5.0 / 60)

        self.dict_tiempos['naranjo']['O'] = 0
        self.dict_tiempos['naranjo']['T'] = 6

        self.dict_frecuencia['amarillo']['O'] = float(5.0 / 60)
        self.dict_frecuencia['amarillo']['T'] = float(5.0 / 60)

        self.dict_tiempos['amarillo']['O'] = 0
        self.dict_tiempos['amarillo']['T'] = 5.5

        self.dict_frecuencia['azul']['O'] = float(5.0 / 60)
        self.dict_frecuencia['azul']['T'] = float(5.0 / 60)

        self.dict_tiempos['azul']['O'] = 0
        self.dict_tiempos['azul']['T'] = 5

        self.dict_frecuencia['rojo']['T'] = float(10.0 / 60)
        self.dict_frecuencia['rojo']['D'] = float(10.0 / 60)

        self.dict_tiempos['rojo']['T'] = 0
        self.dict_tiempos['rojo']['D'] = 10

        self.dict_frecuencia['verde']['O'] = float(10.0 / 60)
        self.dict_frecuencia['verde']['D'] = float(10.0 / 60)

        self.dict_tiempos['verde']['O'] = 0
        self.dict_tiempos['verde']['D'] = 25

        self.dict_frecuencia['morado']['O'] = float(10.0 / 60)
        self.dict_frecuencia['morado']['D'] = float(10.0 / 60)

        self.dict_tiempos['morado']['O'] = 0
        self.dict_tiempos['morado']['D'] = 45

        # arcos subida en O
        self.g.add_edge('1', '4', frecuencia=float(5.0/60), tpo_viaje=0, peso=(60.0 / 5) + 0)
        self.g.add_edge('1', '5', frecuencia=float(5.0/60), tpo_viaje=0, peso=(60.0 / 5) + 0)
        self.g.add_edge('1', '6', frecuencia=float(5.0/60), tpo_viaje=0, peso=(60.0/ 5) + 0)
        self.g.add_edge('1', '7', frecuencia=float(10.0/60), tpo_viaje=0, peso=(60.0 / 10) + 0)
        self.g.add_edge('1', '8', frecuencia=float(5.0/60), tpo_viaje=0, peso=(60.0 / 5) + 0)

        # arcos bajada en O
        self.g.add_edge('4', '1', frecuencia=float('inf')/60, tpo_viaje=0, peso=(60 / float('inf')) + 0)
        self.g.add_edge('5', '1', frecuencia=float('inf')/60, tpo_viaje=0, peso=(60 / float('inf')) + 0)
        self.g.add_edge('6', '1', frecuencia=float('inf')/60, tpo_viaje=0, peso=(60 / float('inf')) + 0)
        self.g.add_edge('7', '1', frecuencia=float('inf')/60, tpo_viaje=0, peso=(60 / float('inf')) + 0)
        self.g.add_edge('8', '1', frecuencia=float('inf')/60, tpo_viaje=0, peso=(60 / float('inf')) + 0)

        # arcos subida en T
        self.g.add_edge('2', '9', frecuencia=float(5.0/60), tpo_viaje=0, peso=(60 / 5) + 0)
        self.g.add_edge('2', '10', frecuencia=float(5.0/60), tpo_viaje=0, peso=(60 / 5) + 0)
        self.g.add_edge('2', '11', frecuencia=float(5.0/60), tpo_viaje=0, peso=(60 / 5) + 0)
        self.g.add_edge('2', '14', frecuencia=float(10.0/60), tpo_viaje=0, peso=(60 / 10) + 0)

        # arcos bajada en T
        self.g.add_edge('9', '2', frecuencia=float('inf'), tpo_viaje=0, peso=(1 / float('inf')) + 0)
        self.g.add_edge('10', '2', frecuencia=float('inf'), tpo_viaje=0, peso=(1 / float('inf')) + 0)
        self.g.add_edge('11', '2', frecuencia=float('inf'), tpo_viaje=0, peso=(1 / float('inf')) + 0)
        self.g.add_edge('14', '2', frecuencia=float('inf'), tpo_viaje=0, peso=(1 / float('inf')) + 0)

        # arcos subida en D
        self.g.add_edge('3', '15', frecuencia=float(10.0/60.0), tpo_viaje=0, peso=(60 / 10) + 0)
        self.g.add_edge('3', '16', frecuencia=float(5.0/60), tpo_viaje=0, peso=(60 / 5) + 0)
        self.g.add_edge('3', '17', frecuencia=float(10.0/60), tpo_viaje=0, peso=(60 / 10) + 0)

        # arcos bajada en D
        self.g.add_edge('15', '3', frecuencia=float('inf'), tpo_viaje=0, peso=(1 / float('inf')) + 0)
        self.g.add_edge('16', '3', frecuencia=float('inf'), tpo_viaje=0, peso=(1 / float('inf')) + 0)
        self.g.add_edge('17', '3', frecuencia=float('inf'), tpo_viaje=0, peso=(1 / float('inf')) + 0)

        # servicio naranjo
        self.g.add_edge('4', '9', frecuencia=float('inf'), tpo_viaje=6, peso=(1 / float('inf')) + 6)
        self.g.add_edge('9', '4', frecuencia=float('inf'), tpo_viaje=6, peso=(1 / float('inf')) + 6)

        # servicio amarillo
        self.g.add_edge('5', '10', frecuencia=float('inf'), tpo_viaje=5.5, peso=(1 / float('inf')) + 5.5)
        self.g.add_edge('10', '5', frecuencia=float('inf'), tpo_viaje=5.5, peso=(1 / float('inf')) + 5.5)

        # servicio azul
        self.g.add_edge('6', '11', frecuencia=float('inf'), tpo_viaje=5, peso=(1 / float('inf')) + 5)
        self.g.add_edge('11', '6', frecuencia=float('inf'), tpo_viaje=5, peso=(1 / float('inf')) + 5)

        # servicio verde
        self.g.add_edge('7', '15', frecuencia=float('inf'), tpo_viaje=25, peso=(1 / float('inf')) + 25)

        # servicio morado
        self.g.add_edge('8', '16', frecuencia=float('inf'), tpo_viaje=45, peso=(1 / float('inf')) + 45)

        # servicio rojo
        self.g.add_edge('14', '17', frecuencia=float('inf'), tpo_viaje=10, peso=(1 / float('inf')) + 10)
        self.g.add_edge('17', '14', frecuencia=float('inf'), tpo_viaje=10, peso=(1 / float('inf')) + 10)

        self.destination = 'D'

        self.paradero_cercano_dic = defaultdict(list)

        for v in self.g.vs:
            self.paradero_cercano_dic[v['name2']] = v['name2']




    def test_grafo_2_nodos(self):
        """Hyper-ruta de grafo con 2 nodos que debería retornar el mismo grafo"""
        g = Graph(directed=True)
        g.add_vertex(name='1', name2='nodo 1', tipo='paradero')
        g.add_vertex(name='2', name2='nodo 2', tipo='paradero')
        g.add_edge('1', '2', frecuencia=2, tpo_viaje=4, peso=(1 / 2) + 4)

        destination = 'nodo 2'
        transfer_penalty = 0
        waiting_penalty = 1
        hyperpath_obj = Hyperpath(g, destination=destination, transfer_penalty=transfer_penalty,
                                  waiting_penalty=waiting_penalty)

        self.assertEqual(hyperpath_obj.destination, destination)
        self.assertEqual(hyperpath_obj.transfer_penalty, transfer_penalty)
        self.assertEqual(hyperpath_obj.waiting_penalty, waiting_penalty)

        self.assertEqual(len(hyperpath_obj._hyperpath.vs), 2)
        self.assertEqual(len(hyperpath_obj._hyperpath.es), 1)

    def test_grafo_prueba_basico(self):
        """Hyper-ruta de ejemplo en paper jacque que debe retornar el mismo grafo original"""
        transfer_penalty = 0
        waiting_penalty = 1
        hyperpath_obj = Hyperpath(self.g, destination=self.destination, transfer_penalty=transfer_penalty,
                                  waiting_penalty=waiting_penalty)
        self.assertEqual(hyperpath_obj.destination, self.destination)
        self.assertEqual(hyperpath_obj.transfer_penalty, transfer_penalty)
        self.assertEqual(hyperpath_obj.waiting_penalty, waiting_penalty)
        self.assertEqual(len(hyperpath_obj._hyperpath.vs), len(self.g.vs))

    def test_format_paths_transfer_penalty(self):
        """grafo de ejemplo paper jacque se testea el formateo de los caminos penalizando trasbordo"""
        transfer_penalty = 16
        waiting_penalty = 1
        hyperpath_obj = Hyperpath(self.g, destination=self.destination, transfer_penalty=transfer_penalty,
                                  waiting_penalty=waiting_penalty)
        Dict_caminos, hiperruta_minimo, hiperruta_proporcion = hyperpath_obj.get_elemental_paths('O', self.destination,
                                                                                                 self.paradero_cercano_dic)
        list_expected_result = ['O/verde/D']
        self.assertListEqual(hiperruta_minimo['O']['D'], list_expected_result)

    def test_get_elemental_paths(self):
        """grafo de ejemplo paper jacque se testea el formateo de los caminos penalizando tiempo de espera"""
        transfer_penalty = 0
        waiting_penalty = 10
        hyperpath_obj = Hyperpath(self.g, destination=self.destination, transfer_penalty=transfer_penalty,
                                  waiting_penalty=waiting_penalty)
        Dict_caminos, hiperruta_minimo, hiperruta_proporcion = hyperpath_obj.get_elemental_paths('O', self.destination,
                                                                                                 self.paradero_cercano_dic)
        list_expected_result = ['O/verde/D', 'O/morado/D']
        self.assertListEqual(hiperruta_minimo['O']['D'], list_expected_result)

    def test_get_elemental_paths(self):
        transfer_penalty = 0
        waiting_penalty = 2
        hyperpath_obj = Hyperpath(self.g, destination=self.destination, transfer_penalty=transfer_penalty,
                                  waiting_penalty=waiting_penalty)
        Dict_caminos, hiperruta_minimo, hiperruta_proporcion = hyperpath_obj.get_elemental_paths('O', self.destination, self.paradero_cercano_dic)

        list_expected_result = ['O/naranjo/T/rojo/D', 'O/amarillo/T/rojo/D', 'O/azul/T/rojo/D']
        self.assertListEqual(Dict_caminos['O']['D']['O/T/D'], list_expected_result)

        list_expected_result = ['O/verde/D']
        self.assertListEqual(Dict_caminos['O']['D']['O/D'], list_expected_result)

        list_expected_result = ['O/naranjo/T/rojo/D', 'O/amarillo/T/rojo/D', 'O/azul/T/rojo/D', 'O/verde/D']
        self.assertListEqual(hiperruta_minimo['O']['D'], list_expected_result)

        self.assertEqual(hiperruta_proporcion['O']['D']['O/verde/D'], 0.4)
        self.assertEqual(hiperruta_proporcion['O']['D']['O/azul/T/rojo/D'], 0.2)
        self.assertEqual(hiperruta_proporcion['O']['D']['O/naranjo/T/rojo/D'], 0.2)
        self.assertEqual(hiperruta_proporcion['O']['D']['O/amarillo/T/rojo/D'], 0.2)

    def test_get_all_shortest_paths(self):

        transfer_penalty = 0
        waiting_penalty = 1
        hyperpath_obj = Hyperpath(self.g, destination=self.destination, transfer_penalty=transfer_penalty,
                                  waiting_penalty=waiting_penalty)

        Dict_caminos, hiperruta_minimo, hiperruta_proporcion = hyperpath_obj.get_elemental_paths('O', self.destination,
                                                                                                 self.paradero_cercano_dic)

        camino_minimo, itinerario_minimo_proporcion = hyperpath_obj.get_all_shortest_paths('O', self.paradero_cercano_dic, hiperruta_proporcion)

        self.assertListEqual(camino_minimo['O']['D'], ['O/verde/D'])

    def test_get_aggregate_paths(self):

        transfer_penalty = 0
        waiting_penalty = 1
        hyperpath_obj = Hyperpath(self.g, destination=self.destination, transfer_penalty=transfer_penalty,
                                  waiting_penalty=waiting_penalty)

        Dict_caminos, hiperruta_minimo, hiperruta_proporcion = hyperpath_obj.get_elemental_paths('O', self.destination, self.paradero_cercano_dic)

        Dict_caminos_etapa = hyperpath_obj.get_services_per_stages('O', self.paradero_cercano_dic)

        ruta_minima, ruta_minima_proporcion = hyperpath_obj.get_aggregate_paths('O', Dict_caminos, Dict_caminos_etapa, self.dict_tiempos, self.dict_frecuencia, hiperruta_proporcion)

        self.assertListEqual(ruta_minima['O']['D'], ['O/naranjo/T/rojo/D', 'O/amarillo/T/rojo/D', 'O/azul/T/rojo/D'])



