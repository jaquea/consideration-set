# -*- coding: utf-8 -*-
import math

class HeapBinaria():
    ''' clase para manipular una heap binaria '''
    def __init__(self):
        # se inicia con un elemento para que los indices coincidan con las operaciones de busqueda del padre
        self.heap = [None]
        # esta posición es con respecto a las posiciones del arreglo
        # es decir, comienza de cero
        self.posicion_ultimo = 0

    def existe(self, id_nodo):
        ''' indica si el id_nodo está presente en el heap '''
        for elemento in self.heap[1:]:
            if elemento[0] == id_nodo:
                return True
        return False

    def insertar(self, elemento):
        ''' @elemento tupla (id, distancia)'''
        if self.posicion_ultimo == 0:
            # agrego el elemento a la última posición de la lista
            self.heap.append(elemento)
            # indico cual es la posición del último element
            self.posicion_ultimo = 1
        else:
            self.heap.append(elemento)
            self.posicion_ultimo = self.posicion_ultimo + 1

            posicion_padre = int(math.ceil(self.posicion_ultimo/2))
            posicion_hijo = self.posicion_ultimo
            while posicion_padre > 0:
                #id_padre = self.heap[posicion_padre][0]
                distancia_padre = self.heap[posicion_padre][1]

                #id_hijo = self.heap[posicion_hijo][0]
                distancia_hijo = self.heap[posicion_hijo][1]

                if distancia_padre > distancia_hijo:
                    # intercambiar
                    nuevo_hijo = self.heap[posicion_padre]
                    self.heap[posicion_padre] = self.heap[posicion_hijo]
                    self.heap[posicion_hijo] = nuevo_hijo

                    posicion_hijo = posicion_padre
                    # posición nuevo padre
                    posicion_padre = int(math.ceil(posicion_padre/2))
                else:
                    break

        #print(self.heap)

    def extraer(self):

        # si no hay elementos en el heap, no hago nada
        if self.posicion_ultimo == 0:
            return None

        nodo_retornado=self.heap[1]

        posicion_ultimo=self.posicion_ultimo
        self.heap[1] = self.heap[posicion_ultimo]
        self.heap.pop()
        self.posicion_ultimo -= 1

        posicion_padre=1
        posicion_hijo_par = 2
        posicion_hijo_impar = 3

        while posicion_hijo_par<=self.posicion_ultimo:

            distancia_padre=self.heap[posicion_padre][1]
            distancia_hijo_par=self.heap[posicion_hijo_par][1]
            # si existe nodo impar
            if posicion_hijo_impar <= self.posicion_ultimo:
                distancia_hijo_impar=self.heap[posicion_hijo_impar][1]
            else:
                distancia_hijo_impar = distancia_hijo_par

            if (distancia_padre>distancia_hijo_par and distancia_hijo_par<=distancia_hijo_impar):
                ''' dist_padre > dist_hijo_par < dist_hijo_impar '''
                nuevo_hijo=self.heap[posicion_padre]
                self.heap[posicion_padre] = self.heap[posicion_hijo_par]
                self.heap[posicion_hijo_par] = nuevo_hijo

                posicion_padre=posicion_hijo_par
                posicion_hijo_par=2*posicion_padre
                posicion_hijo_impar=2*posicion_padre+1

            elif (distancia_padre > distancia_hijo_impar and distancia_hijo_impar < distancia_hijo_par and posicion_hijo_impar<=self.posicion_ultimo):
                ''' dist_padre > dist_hijo_impar < dist_hijo_par '''
                nuevo_hijo = self.heap[posicion_padre]
                self.heap[posicion_padre] = self.heap[posicion_hijo_impar]
                self.heap[posicion_hijo_impar] = nuevo_hijo

                posicion_padre=posicion_hijo_impar
                posicion_hijo_par=2*posicion_padre
                posicion_hijo_impar=2*posicion_padre+1

            else:
                break

        #print(self.heap)

        return nodo_retornado

'''
# prueba del comportamiento del heap
heap = HeapBinaria()
a = (1, 1000)
b = (2, 500)
c = (3, 3000)
heap.insertar(a)
print heap.heap
heap.insertar(b)
print heap.heap
heap.insertar(c)
print heap.heap
print heap.extraer()
print heap.heap
print heap.extraer()
print heap.heap
print heap.extraer()
print heap.heap
print heap.extraer()
'''