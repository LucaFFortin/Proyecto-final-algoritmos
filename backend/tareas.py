from tad_arboles import nodoArbol, insertar_nodo, eliminar_nodo, arbolvacio, remplazar, buscar, preorden, inorden, postorden, por_nivel, altura
from tda_pila import Pila, apilar, desapilar, pila_vacia, en_cima, tamanio, barrido
from tda_colas import Cola, arribo, atencion, cola_vacia, en_frente, tamanio, mover_al_final
from tad_lista import Lista, insertar, lista_vacia, eliminar, tamanio, buscar, insertar_por_prioridad, insertar_por_id


# GET = el cliente solo quiere leer datos del servidor, no quiere modificar nada.
# POST = el cliente quiere enviar datos al servidor, quiere modificar algo en el servidor.

"""
Lista enlazada — Tareas operativas
- Agregar una tarea desde tu formulario.
- Ordenar por prioridad.
- Actualizar el estado o eliminar por ID.
- Mostrar las tareas pendientes en la interfaz.

Pila — Historial de tareas completadas
- Al completar una tarea, quitarla de la lista.
- Guardarla en la cima de la pila.
- Permitir deshacer la última completada y restaurar su estado anterior

Cola — Tickets de soporte
- Registrar solicitudes de los empleados.
- Agregar cada ticket al final mediante arribo().
- Mostrar los usuarios en orden de llegada.
- Atender al primero mediante atencion() y retirarlo de la cola.
"""


#El "puente" entre frontend y backend sería HTTP + JSON.
#El puente entre backend y base de datos sería sqlite3.

# prioridad: 1 (alta), 2 (media), 3 (baja)
#  estado actual (Pendiente, En Progreso, Completada). 

lista_tareas = Lista()


# Agregado de tareas pendientes (TDA Lista Enlazada):




def agregar_tarea(lista_tareas, id, descripcion, prioridad, estado, complejidad = 1):
    """
    Agrega una nueva tarea operativa a la estructura de datos lineal Lista Enlazada, 
    manteniendo el orden algorítmico correspondiente por el identificador del elemento.
    
    Parámetros:
    - lista_tareas: TDA Lista Enlazada que almacena las tareas operativas.
    - id: Identificador único de la tarea.
    - descripcion: Detalle o contenido de la tarea.
    - prioridad: Nivel de prioridad asignado.
    - estado: Estado actual de la tarea (Pendiente, En Progreso, Completada).
    - complejidad: Escala de complejidad técnica (valor por defecto 1).
    """
    
    dato = {
        "id_tarea": id,
        "descripcion": descripcion,
        "prioridad": prioridad,
        "estado": estado,
        "complejidad": complejidad,
    }

    insertar_por_id(lista_tareas, dato)
    print("Tarea agregada correctamente.")





def actualizar_tarea(lista_tareas, id, descripcion, prioridad, estado): 
    """
    Actualiza los datos de una tarea existente en la lista enlazada.
    
    Elimina el nodo original y lo vuelve a reinsertar mediante la primitiva 
    'insertar_por_id' para preservar el ordenamiento algorítmico de la lista.

    Parámetros:
    - lista_tareas: TDA Lista Enlazada de tareas pendientes.
    - id: Identificador único de la tarea a actualizar.
    - descripcion: Nueva descripción de la tarea.
    - prioridad: Nuevo nivel de prioridad.
    - estado: Nuevo estado operativo (Pendiente, En Progreso, etc.).
    """
    aux = lista_tareas.inicio

    while aux is not None and aux.info["id_tarea"] != id:
        aux = aux.sig

    if aux is not None:
        dato = aux.info                  # guardo el diccionario de la tarea
        eliminar(lista_tareas, dato)     # la saco de su posición actual, para asi se acomoda por prioridad al volver a insertarla


        aux.info["descripcion"] = descripcion
        aux.info["prioridad"] = prioridad
        aux.info["estado"] = estado
        insertar_por_id(lista_tareas, dato)
        print("Tarea existente actualizada correctamente.")
    else:
        print("No se encontró la tarea con el ID proporcionado.")


def actualizar_estado_tarea(lista_tareas, id, estado):
    """
    Modifica únicamente el campo estado de una tarea dentro de la lista enlazada.

    Parámetros:
    - lista_tareas: TDA Lista Enlazada.
    - id: Identificador único de la tarea.
    - estado: Nuevo estado a asignar.

    Retorna:
    - El diccionario de la tarea actualizada o None si no se localiza.
    """
    actual = lista_tareas.inicio

    while actual is not None:
        if actual.info["id_tarea"] == id:
            actual.info["estado"] = estado
            return actual.info
        actual = actual.sig

    return None


def editar_tarea(lista_tareas, id, descripcion, prioridad, complejidad, estado):
    """Actualiza todos los datos editables de una tarea operativa."""
    actual = lista_tareas.inicio

    while actual is not None:
        if actual.info["id_tarea"] == id:
            actual.info.update({
                "descripcion": descripcion,
                "prioridad": prioridad,
                "complejidad": complejidad,
                "estado": estado,
            })
            return actual.info
        actual = actual.sig

    return None


def eliminar_id(lista_tareas, id): 
    """
    Busca y elimina una tarea de la lista enlazada utilizando su ID único.

    Parámetros:
    - lista_tareas: TDA Lista Enlazada.
    - id: Identificador único de la tarea a eliminar.

    Retorna:
    - El diccionario de la tarea eliminada o None si no existe.
    """
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




# MÓDULO 2: HISTORIAL DE TAREAS COMPLETADAS (TDA PILA - LIFO)

# Instancia global de la Pila para registrar el historial
pila_historial = Pila()

def completar_tarea(lista_tareas, pila_historial, id):
    """
    Desenlaza una tarea de la lista de pendientes, guarda su estado previo,
    modifica su estado a 'completada' y la apila en el historial (LIFO).

    Parámetros:
    - lista_tareas: TDA Lista Enlazada de tareas activas.
    - pila_historial: TDA Pila donde se registran las tareas finalizadas.
    - id: Identificador único de la tarea a completar.
    """
    tarea = eliminar_id(lista_tareas, id)

    if tarea is not None:
        tarea["estado_previo"] = tarea["estado"] # estado que tenia antes de completarla, para poder restaurarla si se deshace
        tarea["estado"] = "completada" # marca la tarea como completada
        apilar(pila_historial, tarea)
        print("Tarea completada y movida al historial.")
    else:
        print("No se encontró la tarea para completar.")

def deshacer_ultima_completada(lista_tareas, pila_historial):
    """
    Restaura la última tarea completada (ubicada en la cima de la Pila)
    volviéndola a insertar en la lista enlazada de pendientes.

    Parámetros:
    - lista_tareas: TDA Lista Enlazada de tareas pendientes.
    - pila_historial: TDA Pila con las tareas completadas.

    Retorna:
    - La tarea restaurada o None si el historial está vacío.
    """
    if pila_vacia(pila_historial):
        print("No hay tareas completadas para deshacer.")
        return None

    tarea = desapilar(pila_historial)
    tarea["estado"] = tarea["estado_previo"]
    insertar_por_id(lista_tareas, tarea) # ya que dice la consigna volverlo a la lista de pendientes, y como es por prioridad lo vuelvo a insertar por prioridad
    print("Tarea restaurada a la lista de pendientes.")
    return tarea

# Funciones para formatear las estructuras de Lista enlazada y Cola a una estructura JSON

def obtener_todas_las_tareas(lista): 
    """
    Recorre los nodos de la lista enlazada y extrae su información
    en una lista nativa de Python (ideal para estructurar la respuesta JSON).

    Parámetros:
    - lista: TDA Lista Enlazada.

    Retorna:
    - List de diccionarios con el contenido de cada tarea.
    """
    resultado = []
    actual = lista.inicio
    while actual is not None:
        resultado.append(actual.info)
        actual = actual.sig
    return resultado


def obtener_historial(pila_historial): # PILA le pasa 
    """
    Recorre los elementos de la pila desde la cima hasta la base sin destruirla
    o desapilarla, formateando las tareas para la API JSON.

    Parámetros:
    - pila_historial: TDA Pila.

    Retorna:
    - List de tareas ordenadas desde la más reciente a la más antigua.
    """
    resultado = []
    actual = pila_historial.cima
    while actual is not None:
        resultado.append(actual.info)
        actual = actual.sig
    return resultado


# Atencion de solicitudes (Cola)

# Instancia global de una estructura de tipo Cola donde almacenaremos todas las solicitudes
cola_soporte = Cola()

def agregar_solicitud(cola_soporte, id_solicitud, descripcion, prioridad, estado="Pendiente"):
    """
    Registra un ticket de soporte en el final de la cola (estrategia FIFO).

    Parámetros:
    - cola_soporte: TDA Cola de atención.
    - id_solicitud: Identificador del ticket.
    - descripcion: Motivo de la asistencia técnica.
    - prioridad: Grado de prioridad técnica.
    - estado: Estado inicial (por defecto 'Pendiente').

    Retorna:
    - Diccionario con los datos del ticket encolado.
    """
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
    """
    Atiende al primer usuario en turno retirando la solicitud del frente de la cola.

    Parámetros:
    - cola_solicitudes: TDA Cola de solicitudes.

    Retorna:
    - Diccionario del ticket atendido o None si no hay turnos.
    """
    if cola_vacia(cola_solicitudes):
        print("No hay solicitudes para atender.")
        return None

    solicitud = atencion(cola_solicitudes)
    print("Solicitud atendida y removida de la cola.")
    return solicitud

def obtener_solicitudes(cola_soporte):
    """
    Inspecciona los elementos presentes en la cola desde el frente hasta el final
    sin modificar ni vaciar la estructura.

    Parámetros:
    - cola_soporte: TDA Cola.

    Retorna:
    - List de solicitudes respetando el estricto orden de llegada.
    """
    resultado = []
    actual = cola_soporte.frente

    while actual is not None:
        resultado.append(actual.info)
        actual = actual.sig

    return resultado

# Arboles 

def insertar_tarea_arbol(raiz, tarea):
    """
    Inserta recursivamente un nodo en el BST ordenándolo según la escala 
    de complejidad técnica de la tarea.

    Parámetros:
    - raiz: Puntero a la raíz del árbol (o subárbol actual).
    - tarea: Diccionario que contiene los datos de la tarea a indexar.

    Retorna:
    - Nodo raíz del árbol actualizado.
    """
    if raiz is None:
        return nodoArbol(tarea)

    complejidad = tarea["complejidad"]
    complejidad_raiz = raiz.info["complejidad"]

    if complejidad < complejidad_raiz:
        raiz.izq = insertar_tarea_arbol(raiz.izq, tarea)
    else:
        raiz.der = insertar_tarea_arbol(raiz.der, tarea)

    return raiz


def cargar_lista_en_arbol(lista_tareas):
    """
    Recorre la lista enlazada e inserta cada una de sus tareas en un BST 
    para posibilitar la indexación y consultas por complejidad.

    Parámetros:
    - lista_tareas: TDA Lista Enlazada.

    Retorna:
    - Raíz del Árbol Binario de Búsqueda construido.
    """
    raiz = None
    actual = lista_tareas.inicio

    while actual is not None:
        raiz = insertar_tarea_arbol(raiz, actual.info)
        actual = actual.sig

    return raiz

def tarea_menos_compleja(raiz):
    """
    Localiza de forma eficiente la tarea con menor nivel de complejidad.
    Búsqueda algorítmica: Recorre el extremo izquierdo del BST.

    Parámetros:
    - raiz: Raíz del BST.

    Retorna:
    - Diccionario de la tarea menos compleja o None si el árbol está vacío.
    """
    if raiz is None:
        return None

    while raiz.izq is not None:
        raiz = raiz.izq

    return raiz.info

def tarea_mas_compleja(raiz):
    """
    Localiza de forma eficiente la tarea con mayor nivel de complejidad.
    Búsqueda algorítmica: Recorre el extremo derecho del BST.

    Parámetros:
    - raiz: Raíz del BST.

    Retorna:
    - Diccionario de la tarea más compleja o None si el árbol está vacío.
    """
    if raiz is None:
        return None

    while raiz.der is not None:
        raiz = raiz.der

    return raiz.info


def obtener_tareas_arbol(raiz, lista):
    """
    Realiza un recorrido inorden (Izquierda - Raíz - Derecha) del BST para 
    obtener un listado de tareas ordenado ascendentemente por complejidad.

    Parámetros:
    - raiz: Nodo actual del BST.
    - lista: Colección en la cual se acumulan los datos ordenados.
    """
    if raiz is not None:
        obtener_tareas_arbol(raiz.izq, lista)
        lista.append(raiz.info)
        obtener_tareas_arbol(raiz.der, lista)

def obtener_complejidad():
    """
    Construye el BST a partir de la lista enlazada y genera un informe 
    con las métricas requeridas: tareas ordenadas por inorden, menor y mayor complejidad.

    Parámetros:
    - lista_tareas: TDA Lista Enlazada de tareas pendientes.

    Retorna:
    - Diccionario estructurado con las métricas y el conjunto ordenado.
    """
    raiz = cargar_lista_en_arbol(lista_tareas)
    lista_ordenada = []
    obtener_tareas_arbol(raiz, lista_ordenada)

    return {
        "tareas": lista_ordenada,
        "menor": tarea_menos_compleja(raiz),
        "mayor": tarea_mas_compleja(raiz)
    }


