from tda_colas import Cola, arribo, atencion, cola_vacia

class nodoArbol(object):
    """Clase nodo árbol."""

    def __init__(self, info):
        """Crea un nodo con la información cargada."""
        self.izq = None
        self.der = None
        self.info = info

class nodoArbol_indice(object):
    

    def __init__(self, texto, pagina):
        """Crea un nodo con la información cargada."""
        self.izq = None
        self.der = None
        self.texto = texto # guardo el texto y pagina 
        self.pagina = pagina 

class nodoArbol_heroe_villano(object):
    

    def __init__(self, info, opcion):
        """Crea un nodo con la información cargada."""
        self.izq = None
        self.der = None
        self.opcion = opcion
        self.info = info

def insertar_nodo_villano_heroe(raiz, heroe_villano, opcion):
    """Inserta un dato al árbol."""
    if(raiz is None):
        raiz = nodoArbol_heroe_villano(heroe_villano, opcion)
    elif(heroe_villano < raiz.info):
        raiz.izq = insertar_nodo_villano_heroe(raiz.izq, heroe_villano, opcion)
    else:
        raiz.der = insertar_nodo_villano_heroe(raiz.der, heroe_villano, opcion)
    return raiz

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


def inorden(raiz):
    """Realiza el barrido inorden del árbol."""
    if(raiz is not None):
        inorden(raiz.izq)
        print(raiz.info)
        inorden(raiz.der)

def inorden_villano_heroe(raiz):
    """Realiza el barrido inorden de los heroes y villanos."""
    if(raiz is not None):
        inorden_villano_heroe(raiz.izq)
        print(raiz.info, raiz.opcion)
        inorden_villano_heroe(raiz.der)



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


def altura(raiz):
    if raiz is None:
        return -1
    else:
        altura_izq = altura(raiz.izq)
        altura_der = altura(raiz.der)
        return 1 + max(altura_izq, altura_der) # cuando el nodo existe 
    
# altura(3) = 1 + max(0, -1)
#altura(3) = 1 + 0
#altura(3) = 1

def altura_isquierda_derecha(raiz): # necesitas la altura de sus hijos para cuando ya algun hijo sea None corte la recursion
    if raiz is None:
        print ("Ya esta vacio el arbol")
    else:
        altura_izq = altura(raiz.izq)
        altura_der = altura(raiz.der)
        print(f"Altura del subárbol izquierdo: {altura_izq}")
        print(f"Altura del subárbol derecho: {altura_der}")

"""
    5 --> raiz 

3     8                 como 3 da 1 y 8 da 0 no tiene hijos si suma 1 del return mas el 1 del 3 te da que tiene un total de altura de 2 

1 hijo de 3 este 3 no tiene hijo derecho None 3 tiene altura de 1 
no tiene hijos altura = 0
"""