class nodoCola():

    def __init__(self):
        self.info = None
        self.sig = None


class Cola():

    def __init__(self):
        self.frente = None
        self.final = None
        self.tamanio = 0


def arribo(cola, dato):

    nodo = nodoCola()
    nodo.info = dato

    if cola.final is None:
        cola.frente = nodo
    else:
        cola.final.sig = nodo

    cola.final = nodo
    cola.tamanio += 1


def atencion(cola):  # Ej : 5 / 10 (primero 5) despues 5.sig apunta al siguiente nodo / cola.finalo apunta al nodo con el 10  

    aux = cola.frente.info
    cola.frente = cola.frente.sig

    if cola.frente is None:
        cola.final = None   #Control para saber si la cola ya esta vacia sino apunta a nada en memoria

    cola.tamanio -= 1
    return aux


def cola_vacia(cola):
    return cola.tamanio == 0


def en_frente(cola):
    return cola.frente.info


def tamanio(cola):
    return cola.tamanio


def mover_al_final(cola):

    dato = atencion(cola)
    arribo(cola, dato)

    return dato