from igraph import *

from HeapBinaria import HeapBinaria

class Shortest:
    def __init__(self, grafo, destination, origin):
        self.g = grafo
        self.destination = destination
        self.origin = origin

