from tda_colas import Cola, arribo, atencion, cola_vacia

class nodoArbol(object):
    """Clase nodo árbol."""

    def __init__(self, info):
        """Crea un nodo con la información cargada."""
        self.izq = None
        self.der = None
        self.info = info


def insertar_nodo(raiz, dato):
    """Inserta un dato al árbol."""
    if(raiz is None):
        raiz = nodoArbol(dato)
    elif(dato < raiz.info):
        raiz.izq = insertar_nodo(raiz.izq, dato)
    else:
        raiz.der = insertar_nodo(raiz.der, dato)
    return raiz



def eliminar_nodo(raiz, clave):
    """Elimina un elemento del árbol y lo devuelve si lo encuentra."""
    x = None
    if(raiz is not None):
        if(clave < raiz.info):
            raiz.izq, x = eliminar_nodo(raiz.izq, clave)
        elif(clave > raiz.info):
            raiz.der, x = eliminar_nodo(raiz.der, clave)
        else:
            x = raiz.info
            if(raiz.izq is None):
                raiz = raiz.der
            elif(raiz.der is None):
                raiz = raiz.izq
            else:
                raiz.izq, aux = remplazar(raiz.izq)
                raiz.info = aux.info
    return raiz, x


def remplazar(raiz):
    """Determina el nodo que remplazará al que se elimina."""
    aux = None
    if(raiz.der is None):
        aux = raiz
        raiz = raiz.izq
    else:
        raiz.der, aux = remplazar(raiz.der)
    return raiz, aux


def arbolvacio(raiz):
    """Devuelve true si el árbol esta vacio."""
    return raiz is None


def buscar(raiz, clave):
    """Devuelve la direccion del elemento buscado."""
    pos = None
    if(raiz is not None):
        if(raiz.info == clave):
            pos = raiz
        elif clave < raiz.info:
            pos = buscar(raiz.izq, clave)
        else:
            pos = buscar(raiz.der, clave)
    return pos


def preorden(raiz):
    """Realiza el barrido preorden del árbol."""
    if(raiz is not None):
        print(raiz.info)
        preorden(raiz.izq)
        preorden(raiz.der)


def inorden(raiz, lista):
    """Recorre el árbol en inorden y guarda los datos en una lista."""
    if raiz is not None:
        inorden(raiz.izq, lista)
        lista.append(raiz.info)
        inorden(raiz.der, lista)


def postorden(raiz):
    """Realiza el barrido postorden del árbol."""
    if(raiz is not None):
        postorden(raiz.der)
        print(raiz.info)
        postorden(raiz.izq)


def por_nivel(raiz):
    """Realiza el barrido por nivel del árbol."""
    pendientes = Cola()
    arribo(pendientes, raiz)
    while(not cola_vacia(pendientes)):
        nodo = atencion(pendientes)
        print(nodo.info)
        if(nodo.izq is not None):
            arribo(pendientes, nodo.izq)
        if(nodo.der is not None):
            arribo(pendientes, nodo.der)


# ==================== OPERACIONES PARA TASKFLOW ====================

def insertar_tarea_arbol(raiz, tarea):
    """Inserta una tarea en el árbol según su complejidad."""
    if raiz is None:
        return nodoArbol(tarea)

    if tarea["complejidad"] < raiz.info["complejidad"]:
        raiz.izq = insertar_tarea_arbol(raiz.izq, tarea)
    else:
        raiz.der = insertar_tarea_arbol(raiz.der, tarea)

    return raiz


def tarea_menos_compleja(raiz):
    """Devuelve la tarea de menor complejidad."""
    if raiz is None:
        return None

    while raiz.izq is not None:
        raiz = raiz.izq

    return raiz.info


def tarea_mas_compleja(raiz):
    """Devuelve la tarea de mayor complejidad."""
    if raiz is None:
        return None

    while raiz.der is not None:
        raiz = raiz.der

    return raiz.info
