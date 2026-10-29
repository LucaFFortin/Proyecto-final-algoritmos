from tda_pila import apilar

class nodoLista(object):
    """Clase nodo lista."""

    info, sig = None, None          


class Lista(object):
    """Clase lista simplemente enlazada."""

    def __init__(self):
        """Crea una lista vacía."""
        self.inicio = None 
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

    if (lista.inicio is None) or (lista.inicio.info["prioridad"] >= dato["prioridad"]): # puse solamente para que compare por priodad ya que uso diccionarios no me deja
        nodo.sig = lista.inicio
        lista.inicio = nodo
    else:
        ant = lista.inicio
        act = lista.inicio.sig

        while (act is not None and act.info["prioridad"] <= dato["prioridad"]):
            ant = ant.sig
            act = act.sig

        nodo.sig = act
        ant.sig = nodo



def lista_vacia(lista):
    """Devuelve true si la lista esta vacia."""
    return lista.inicio is None


def eliminar(lista, clave):
    """Elimina un elemento de la lista y lo devuelve si lo encuentra."""
    dato = None

    if lista.inicio is None:
        return None

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


def tamanio_circular(lista):
    """Devuelve el número de elementos de la lista circular."""
    return lista.tamanio

def es_vacia_circular(lista):
    """Devuelve True si la lista circular está vacía."""
    return lista.inicio is None

# ==================== OPERACIONES PARA TASKFLOW ====================


def insertar_por_prioridad(lista, dato):  
    """Inserta el dato pasado en la lista."""
    nodo = nodoLista()
    nodo.info = dato

    if (lista.inicio is None) or (lista.inicio.info["prioridad"] >= dato["prioridad"]): 
        lista.inicio = nodo
    else:
        ant = lista.inicio
        act = lista.inicio.sig

        while (act is not None and act.info["prioridad"] <= dato["prioridad"]):
            ant = ant.sig
            act = act.sig

        nodo.sig = act
        ant.sig = nodo

    lista.tamanio += 1

def buscar_por_id(lista, id_tarea):
    """Busca una tarea por ID dentro de la lista."""
    actual = lista.inicio
    while actual is not None:
        if actual.info["id_tarea"] == id_tarea:
            return actual.info
        actual = actual.sig
    return None


def actualizar_tarea(lista_tareas, id, descripcion, prioridad, estado):
    """Actualiza una tarea y vuelve a insertarla según su prioridad."""
    aux = lista_tareas.inicio

    while aux is not None and aux.info["id_tarea"] != id:
        aux = aux.sig

    if aux is not None:
        dato = aux.info
        eliminar(lista_tareas, dato)
        dato["descripcion"] = descripcion
        dato["prioridad"] = prioridad
        dato["estado"] = estado
        insertar_por_prioridad(lista_tareas, dato)
        print("Tarea existente actualizada correctamente.")
        return dato

    print("No se encontró la tarea con el ID proporcionado.")
    return None


def actualizar_estado_tarea(lista_tareas, id, estado):
    """Actualiza solamente el estado de una tarea."""
    actual = lista_tareas.inicio

    while actual is not None:
        if actual.info["id_tarea"] == id:
            actual.info["estado"] = estado
            return actual.info
        actual = actual.sig

    return None


def eliminar_por_id(lista_tareas, id):
    """Busca una tarea por ID y la elimina."""
    aux = lista_tareas.inicio

    while aux is not None and aux.info["id_tarea"] != id:
        aux = aux.sig

    if aux is not None:
        dato = aux.info
        eliminar(lista_tareas, dato)
        print("Tarea eliminada correctamente.")
        return dato

    print("No se encontró la tarea para eliminar con el ID proporcionado.")
    return None



def completar_tarea(lista_tareas, pila_historial, id):
    """Completa una tarea, guarda su posición y la apila en el historial."""
    actual = lista_tareas.inicio
    posicion = 0

    while actual is not None and actual.info["id_tarea"] != id:
        actual = actual.sig
        posicion += 1

    if actual is None:
        print("No se encontró la tarea para completar.")
        return None

    tarea = actual.info
    tarea["posicion_previa"] = posicion
    tarea["estado_previo"] = tarea["estado"]

    eliminar(lista_tareas, tarea)
    tarea["estado"] = "completada"
    apilar(pila_historial, tarea)

    print("Tarea completada y movida al historial.")
    return tarea


def restaurar_posicion(lista_tareas, tarea, posicion):
    """Restaura una tarea en su posición anterior si conserva el orden por prioridad."""
    anterior = None
    actual = lista_tareas.inicio
    indice = 0

    while actual is not None and indice < posicion:
        anterior = actual
        actual = actual.sig
        indice += 1

    prioridad = tarea["prioridad"]
    prioridad_anterior_valida = (anterior is None or anterior.info["prioridad"] <= prioridad)
    prioridad_siguiente_valida = (actual is None or prioridad <= actual.info["prioridad"])

    if prioridad_anterior_valida and prioridad_siguiente_valida:
        nodo = nodoLista()
        nodo.info = tarea
        nodo.sig = actual

        if anterior is None:
            lista_tareas.inicio = nodo
        else:
            anterior.sig = nodo

        lista_tareas.tamanio += 1
    else:
        insertar_por_prioridad(lista_tareas, tarea)


def obtener_datos(lista):
    """Recorre la lista y devuelve sus datos en una lista de Python."""
    resultado = []
    actual = lista.inicio
    while actual is not None:
        resultado.append(actual.info)
        actual = actual.sig
    return resultado


