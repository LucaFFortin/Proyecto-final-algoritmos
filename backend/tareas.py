from tad_arboles import nodoArbol, insertar_nodo, eliminar_nodo, arbolvacio, remplazar, buscar, preorden, inorden, postorden, por_nivel, altura
from tda_pila import Pila, apilar, desapilar, pila_vacia, en_cima, tamanio, barrido
from tda_colas import Cola, arribo, atencion, cola_vacia, en_frente, tamanio, mover_al_final
from tad_lista import nodoLista, Lista, insertar, lista_vacia, eliminar, tamanio, buscar, insertar_por_prioridad 


# prioridad: 1 (alta), 2 (media), 3 (baja)
#  estado actual (Pendiente, En Progreso, Completada). 

lista_tareas = Lista()
pila_historial = Pila()
cola_soporte = Cola()

# ============================ FUNCIONES DE LISTA ENLAZADA =========================================

# Agregado de tareas pendientes (TDA Lista Enlazada):




def agregar_tarea(lista_tareas, id, descripcion, prioridad, estado, complejidad=1): # -------- agregar tarea -------------
    dato = {
        "id_tarea": id,
        "descripcion": descripcion,
        "prioridad": prioridad,
        "estado": estado,
        "complejidad": complejidad
    }

    insertar_por_prioridad(lista_tareas, dato)
    print("Tarea agregada correctamente.")





def actualizar_tarea(lista_tareas, id, descripcion, prioridad, estado): # -------- actualizar tarea -------------
    aux = lista_tareas.inicio

    while aux is not None and aux.info["id_tarea"] != id:
        aux = aux.sig

    if aux is not None:
        dato = aux.info                  # guardo el diccionario de la tarea
        eliminar(lista_tareas, dato)     # la saco de su posición actual, para asi se acomoda por prioridad al volver a insertarla


        aux.info["descripcion"] = descripcion
        aux.info["prioridad"] = prioridad
        aux.info["estado"] = estado
        insertar_por_prioridad(lista_tareas, dato)
        print("Tarea existente actualizada correctamente.")
    else:
        print("No se encontró la tarea con el ID proporcionado.")


def actualizar_estado_tarea(lista_tareas, id, estado):
    """Actualiza el estado de una tarea que sigue en la lista enlazada."""
    actual = lista_tareas.inicio

    while actual is not None:
        if actual.info["id_tarea"] == id:
            actual.info["estado"] = estado
            return actual.info
        actual = actual.sig

    return None


def eliminar_id(lista_tareas, id): # -------- eliminar tarea -------------
    aux = lista_tareas.inicio

    while aux is not None and aux.info["id_tarea"] != id:
        aux = aux.sig


def eliminar_id(lista_tareas, id):
    return eliminar_por_id_lista(lista_tareas, id)

def obtener_todas_las_tareas(lista):
    return obtener_datos(lista)



#---------------------------------------------------------------------------------------------------------------------------------------------------
    
pila_historial = Pila()

# en un despegable historial de completado 
# el usuario va elegir un id = como tarea1, tarea2, tarea3, y se va a marcar como completada, y se va a mover de la lista a la pila historial.
def completar_tarea(lista_tareas, pila_historial, id):
    """Completa una tarea y guarda su posición original."""
    actual = lista_tareas.inicio
    posicion = 0

    while actual is not None and actual.info["id_tarea"] != id:
        actual = actual.sig
        posicion += 1

    if actual is None:
        print("No se encontró la tarea para completar.")
        return

    tarea = actual.info
    tarea["posicion_previa"] = posicion
    tarea["estado_previo"] = tarea["estado"]

    eliminar(lista_tareas, tarea)

    tarea["estado"] = "completada"
    apilar(pila_historial, tarea)

    print("Tarea completada y movida al historial.")

def restaurar_posicion(lista_tareas, tarea, posicion):
    """Restaura la posición original si respeta las prioridades."""

    anterior = None
    actual = lista_tareas.inicio
    indice = 0

    while actual is not None and indice < posicion: # mientras actual sea un nodo para recorrer and indice < posicion seria que no llegamos a donde queriamos 
        anterior = actual
        actual = actual.sig
        indice += 1

    prioridad = tarea["prioridad"]

    # Comprobar que la posición respete el orden de prioridades.
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
        # Si la posición original ya no es válida,
        # mantener el orden obligatorio por prioridad.
        insertar_por_prioridad(lista_tareas, tarea)


def deshacer_ultima_completada(lista_tareas, pila_historial):
    """Desapila la última tarea completada y la restaura a pendientes."""
    if pila_vacia(pila_historial):
        print("No hay tareas completadas para deshacer.")
        return None

    tarea = desapilar(pila_historial)
    tarea["estado"] = tarea["estado_previo"]

    posicion = tarea.pop("posicion_previa", lista_tareas.tamanio)
    restaurar_posicion(lista_tareas, tarea, posicion)
    print("Tarea restaurada a la lista de pendientes.")
    return tarea

# ---------------------------------------------------------------------------------------------------------------------------------------------------

def obtener_todas_las_tareas(lista): # lo manda a los que seria al JSON en forma de lista (LISTAS)
    """Recorre los nodos de la lista enlazada y devuelve una lista común para JSON."""
    resultado = []
    actual = lista.inicio
    while actual is not None:
        resultado.append(actual.info)
        actual = actual.sig
    return resultado

# --------------------------------------------------------------------------------------------------------------------------------------------

def obtener_historial(pila_historial): # PILA le pasa 
    """Devuelve las tareas completadas desde la cima de la pila sin vaciarla."""
    resultado = []
    actual = pila_historial.cima
    while actual is not None:
        resultado.append(actual.info)
        actual = actual.sig
    return resultado


# Atencion de solicitudes (Cola)
# supongamos que entramos a la funcionalidad de solicitudes el empleado va a ingresar una solicitud 
# donde esto va a ser manejado por una cola (tendria que a ver un apartado de solicitudes)
# si fue atendido se le apreta un boton atendido y se saca de la lista 

cola_soporte = Cola()

def agregar_solicitud(cola_soporte, id_solicitud, descripcion, prioridad, estado="Pendiente"):
    """Agrega una solicitud al final de la cola respetando el orden de llegada."""
    dato = {
        "id_solicitud": id_solicitud,
        "descripcion": descripcion,
        "prioridad": prioridad,
        "estado": estado,
    }
    arribo(cola_soporte, dato)
    print("Solicitud agregada a la cola.")
    return dato


def atender_solicitud(cola_solicitudes):
    """Atiende la primera solicitud en la cola."""
    if cola_vacia(cola_solicitudes):
        print("No hay solicitudes para atender.")
        return None
    solicitud = atencion(cola_solicitudes)
    print("Solicitud atendida y removida de la cola.")
    return solicitud

def obtener_solicitudes(cola_soporte):
    """Devuelve las solicitudes sin modificar la cola."""
    resultado = []
    actual = cola_soporte.frente

    while actual is not None:
        resultado.append(actual.info)
        actual = actual.sig

    return resultado


def enviar_tarea_a_mesa_ayuda(lista_tareas, cola_soporte, id_tarea, id_solicitud):
    """Busca una tarea en la lista y la convierte en solicitud."""

    actual = lista_tareas.inicio

    while actual is not None:
        tarea = actual.info

        if tarea["id_tarea"] == id_tarea:
            return agregar_solicitud(
                cola_soporte,
                id_solicitud,
                tarea["descripcion"],
                tarea["prioridad"],
                "Pendiente"
            )

        actual = actual.sig

    return None


# Arboles 
# Tarea más compleja y menos compleja lo va a ir ordenando en la lista de tareas / se tiene que pasar al mismo tiempo de lista al arbol
# listar el conjunto mediante inorden


# Despegable menor compleja buscador diciendo si queres la más compleja y menos compleja



def insertar_tarea_arbol(raiz, tarea):
    """Inserta una tarea en el árbol según su complejidad."""
    if raiz is None:
        return nodoArbol(tarea)

def enviar_tarea_a_mesa_ayuda(lista_tareas, cola_soporte, id_tarea, id_solicitud):
    tarea = buscar_por_id(lista_tareas, id_tarea)
    if tarea is None:
        return None
    descripcion_ticket = f"Tarea {tarea['id_tarea']}: {tarea['descripcion']}"

    return agregar_solicitud(cola_soporte, id_solicitud, descripcion_ticket, tarea["prioridad"], "Pendiente")

# ======================================= OPERACIONES DE LISTAS ARBOLES =================================================

def cargar_lista_en_arbol(lista_tareas):
    """Construye el árbol recorriendo la lista sin modificarla."""
    raiz = None
    for tarea in obtener_datos(lista_tareas):
        raiz = insertar_tarea_arbol(raiz, tarea)
    return raiz

def tarea_menos_compleja(raiz):
    if raiz is None:
        return None

    while raiz.izq is not None:
        raiz = raiz.izq

    return raiz.info

def tarea_mas_compleja(raiz):
    if raiz is None:
        return None

    while raiz.der is not None:
        raiz = raiz.der

    return raiz.info


def obtener_tareas_arbol(raiz, lista):
    """Recorre el árbol en inorden y agrega las tareas a una lista."""
    if raiz is not None:
        obtener_tareas_arbol(raiz.izq, lista)
        lista.append(raiz.info)
        obtener_tareas_arbol(raiz.der, lista)

def obtener_complejidad():
    """Devuelve las tareas ordenadas por complejidad usando el árbol."""
    raiz = cargar_lista_en_arbol(lista_tareas)
    lista_ordenada = []
    obtener_tareas_arbol(raiz, lista_ordenada)
    return {
        "tareas": lista_ordenada,
        "menor": tarea_menos_compleja(raiz),
        "mayor": tarea_mas_compleja(raiz)
    }

# abria que poner la logica de lista y que la cola agarre la ID de esta tarea en especifico 

