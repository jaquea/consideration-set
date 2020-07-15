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
        self.g.add_vertex(name='9', name2='T//naranjo', tipo='servicio')
        self.g.add_vertex(name='10', name2='T/amarillo', tipo='servicio')
        self.g.add_vertex(name='11', name2='T/azul', tipo='servicio')
        self.g.add_vertex(name='14', name2='T/rojo', tipo='servicio')

        # nodos servicio que pasan por D
        self.g.add_vertex(name='15', name2='D/verde', tipo='servicio')
        self.g.add_vertex(name='16', name2='D/morado', tipo='servicio')
        self.g.add_vertex(name='17', name2='D/rojo', tipo='servicio')

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

    def test_format_paths(self):
        """grafo de ejemplo paper jacque se testea el formateo de los caminos sin penalizacion alguna"""
        transfer_penalty = 0
        waiting_penalty = 1
        hyperpath_obj = Hyperpath(self.g, destination=self.destination, transfer_penalty=transfer_penalty,
                                  waiting_penalty=waiting_penalty)
        origin_index = hyperpath_obj._hyperpath.vs.find(name2='O').index
        destination_index = hyperpath_obj._hyperpath.vs.find(name2=self.destination).index

        path_set = hyperpath_obj.find_all_paths(origin_index, destination_index, maxlen=None, mode='OUT')
        format_path = hyperpath_obj.format_paths(path_set)
        list_expected_result = ['O/naranjo/T/rojo/D', 'O/amarillo/T/rojo/D', 'O/azul/T/rojo/D', 'O/verde/D']
        self.assertListEqual(format_path, list_expected_result)

    def test_format_paths_transfer_penalty(self):
        """grafo de ejemplo paper jacque se testea el formateo de los caminos penalizando trasbordo"""
        transfer_penalty = 16
        waiting_penalty = 1
        hyperpath_obj = Hyperpath(self.g, destination=self.destination, transfer_penalty=transfer_penalty,
                                  waiting_penalty=waiting_penalty)
        origin_index = hyperpath_obj._hyperpath.vs.find(name2='O').index
        destination_index = hyperpath_obj._hyperpath.vs.find(name2=self.destination).index

        path_set = hyperpath_obj.find_all_paths(origin_index, destination_index, maxlen=None, mode='OUT')
        format_path = hyperpath_obj.format_paths(path_set)
        list_expected_result = ['O/verde/D']
        self.assertListEqual(format_path, list_expected_result)

    def test_format_paths_waiting_penalty(self):
        """grafo de ejemplo paper jacque se testea el formateo de los caminos penalizando tiempo de espera"""
        transfer_penalty = 0
        waiting_penalty = 10
        hyperpath_obj = Hyperpath(self.g, destination=self.destination, transfer_penalty=transfer_penalty,
                                  waiting_penalty=waiting_penalty)
        origin_index = hyperpath_obj._hyperpath.vs.find(name2='O').index
        destination_index = hyperpath_obj._hyperpath.vs.find(name2=self.destination).index

        path_set = hyperpath_obj.find_all_paths(origin_index, destination_index, maxlen=None, mode='OUT')
        format_path = hyperpath_obj.format_paths(path_set)
        list_expected_result = ['O/verde/D', 'O/morado/D']
        self.assertListEqual(format_path, list_expected_result)




