class nodoLista(object):
    """Clase nodo lista."""

    info, sig = None, None          #info= dato que guarda = 10, hola / sig un puntero al siguiente nodo de la lista 


class Lista(object):
    """Clase lista simplemente enlazada."""

    def __init__(self):
        """Crea una lista vacía."""
        self.inicio = None  #en el inicio es nada 
        self.tamanio = 0


class nodoListaDoble(object):
    """Clase nodo para lista doblemente enlazada."""

    ant, info, sig = None, None, None


class ListaDoble(object):
    """Clase lista doblemente enlazada."""

    def __init__(self):
        """Crea una lista doble vacía."""
        self.inicio = None
        self.fin = None
        self.tamanio = 0

class NodoListaCircular(object):
    """Clase nodo para lista circular."""

    info, sig = None, None


class ListaCircular(object):
    """Clase lista circular simplemente enlazada."""

    def __init__(self):
        """Crea una lista circular vacía."""
        self.inicio = None
        self.fin = None
        self.tamanio = 0



def insertar(lista, dato):
    """Inserta el dato pasado en la lista."""
    nodo = nodoLista()
    nodo.info = dato

    if (lista.inicio is None) or (lista.inicio.info > dato):
        nodo.sig = lista.inicio
        lista.inicio = nodo
    else:
        ant = lista.inicio
        act = lista.inicio.sig

        while (act is not None and act.info < dato):
            ant = ant.sig
            act = act.sig

        nodo.sig = act
        ant.sig = nodo

    lista.tamanio += 1


def insertar_por_prioridad(lista, dato):
    """Inserta el dato pasado en la lista."""
    nodo = nodoLista()
    nodo.info = dato

    if (lista.inicio is None) or (lista.inicio.info["prioridad"] > dato["prioridad"]): # puse solamente para que compare por priodad ya que uso diccionarios no me deja
        nodo.sig = lista.inicio
        lista.inicio = nodo
    else:
        ant = lista.inicio
        act = lista.inicio.sig

        while (act is not None and act.info["prioridad"] < dato["prioridad"]):
            ant = ant.sig
            act = act.sig

        nodo.sig = act
        ant.sig = nodo

    lista.tamanio += 1


def lista_vacia(lista):
    """Devuelve true si la lista esta vacia."""
    return lista.inicio is None


def eliminar(lista, clave):
    """Elimina un elemento de la lista y lo devuelve si lo encuentra."""
    dato = None

    if (lista.inicio.info == clave):
        dato = lista.inicio.info
        lista.inicio = lista.inicio.sig
        lista.tamanio -= 1
    else:
        anterior = lista.inicio
        actual = lista.inicio.sig

        while (actual is not None and actual.info != clave):
            anterior = anterior.sig
            actual = actual.sig

        if (actual is not None):
            dato = actual.info
            anterior.sig = actual.sig
            lista.tamanio -= 1

    return dato


def tamanio(lista):
    """Devuelve el número de elementos de la lista."""
    return lista.tamanio


def buscar(lista, buscado):
    """Devuelve la dirección del elemento buscado."""
    aux = lista.inicio

    while (aux is not None and aux.info != buscado):
        aux = aux.sig

    return aux


def barrido(lista):
    """Realiza un barrido de la lista mostrando sus valores."""
    aux = lista.inicio

    while (aux is not None):
        print(aux.info)
        aux = aux.sig

def criterio(dato, campo=None):
    """Determina el campo por el cual se debe comparar el dato."""
    dic = {}

    if (hasattr(dato, '__dict__')):
        dic = dato.__dict__

    if campo is None or campo not in dic:
        return dato
    else:
        return dic[campo]

def insertar_posicion(lista, dato, i):
    nodo = nodoLista() 
    nodo.info = dato

    if i <= 0 or lista.inicio is None:
        nodo.sig = lista.inicio     # si pones en la posicion 0 algo negativo o es none no hace falta recorrer nada 
        lista.inicio = nodo #pasa a ser el inicio de la lista 
    else:
        ant = lista.inicio          #sino inserta en otra posicion
        act = lista.inicio.sig
        contador = 1

        while act is not None and contador < i:
            ant = ant.sig   #anterior
            act = act.sig   #actual
            contador += 1   #encontre la posicion exacta que quiero reemplazar 

        nodo.sig = act #se actualiza con el actual y el ant se va quedar con el de antes 
        ant.sig = nodo

    lista.tamanio += 1   #incrementa el tamaño de la lista con respecto a los datos que se vayan poniendo

def insertar_final(lista, dato):
    """Inserta el dato al final de la lista, respetando el orden de carga."""
    insertar_posicion(lista, dato, tamanio(lista))


def insertar_final_circular(lista, dato):
    """Inserta el dato al final de la lista circular, respetando el orden de carga."""
    nodo = NodoListaCircular()
    nodo.info = dato

    if lista.inicio is None:
        # primer nodo: se apunta a sí mismo
        nodo.sig = nodo
        lista.inicio = nodo
        lista.fin = nodo
    else:
        nodo.sig = lista.inicio       # el nuevo nodo cierra el círculo apuntando al primero
        lista.fin.sig = nodo          # el anterior último ahora apunta al nuevo nodo
        lista.fin = nodo              # el nuevo nodo pasa a ser el último

    lista.tamanio += 1

def tamanio_circular(lista):
    """Devuelve el número de elementos de la lista circular."""
    return lista.tamanio

def es_vacia_circular(lista):
    """Devuelve True si la lista circular está vacía."""
    return lista.inicio is None
