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


def atencion(cola):
    """Retira y devuelve el primer elemento de la cola."""
    if cola_vacia(cola):
        return None

    aux = cola.frente.info
    cola.frente = cola.frente.sig

    if cola.frente is None:
        cola.final = None   

    cola.tamanio -= 1
    return aux


def cola_vacia(cola):
    return cola.tamanio == 0


def en_frente(cola):
    """Devuelve el elemento del frente sin retirarlo."""
    if cola_vacia(cola):
        return None
    return cola.frente.info


def tamanio(cola):
    return cola.tamanio


def mover_al_final(cola):

    dato = atencion(cola)
    arribo(cola, dato)

    return dato

# ================= OPERACION USADA TASKFLOW ========================
def obtener_datos(cola):
    """Devuelve los datos en orden FIFO sin vaciar la cola."""
    auxiliar = Cola()
    resultado = []

    while not cola_vacia(cola):
        dato = atencion(cola)
        resultado.append(dato)
        arribo(auxiliar, dato)

    while not cola_vacia(auxiliar):
        arribo(cola, atencion(auxiliar))

    return resultado


