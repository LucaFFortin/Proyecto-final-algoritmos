from tad_arboles import insertar_tarea_arbol,inorden,tarea_menos_compleja,tarea_mas_compleja
from tda_pila import Pila, apilar, desapilar, pila_vacia, obtener_datos as obtener_datos_pila
from tda_colas import Cola, arribo, atencion, cola_vacia, obtener_datos as obtener_datos_cola
from tad_lista import Lista,insertar_por_prioridad,buscar_por_id,actualizar_tarea as actualizar_tarea_lista,completar_tarea as completar_tarea_lista,actualizar_estado_tarea as actualizar_estado_tarea_lista,eliminar_por_id as eliminar_por_id_lista,restaurar_posicion,obtener_datos,vaciar_lista,tamanio as tamanio_lista



lista_tareas = Lista()
pila_historial = Pila()
cola_soporte = Cola()

# ============================ FUNCIONES DE LISTA ENLAZADA =========================================

def agregar_tarea(lista_tareas, id, descripcion, prioridad, estado, complejidad=1):
    """Agrega una tarea a la lista manteniendo el orden por prioridad."""
    dato = {
        "id_tarea": id,
        "descripcion": descripcion,
        "prioridad": prioridad,
        "estado": estado,
        "complejidad": complejidad
    }
    insertar_por_prioridad(lista_tareas, dato)
    print("Tarea agregada correctamente.")


def actualizar_tarea(lista_tareas, id, descripcion, prioridad, estado):
    return actualizar_tarea_lista(lista_tareas, id, descripcion, prioridad, estado)


def actualizar_estado_tarea(lista_tareas, id, estado):
    return actualizar_estado_tarea_lista(lista_tareas, id, estado)


def eliminar_id(lista_tareas, id):
    return eliminar_por_id_lista(lista_tareas, id)

def obtener_todas_las_tareas(lista):
    return obtener_datos(lista)

# ============================ FUNCIONES DE PILAS ================================================

def completar_tarea(lista_tareas, pila_historial, id):
    return completar_tarea_lista(lista_tareas, pila_historial, id)


def deshacer_ultima_completada(lista_tareas, pila_historial):
    """Desapila la última tarea completada y la restaura."""
    if pila_vacia(pila_historial):
        print("No hay tareas completadas para deshacer.")
        return None

    tarea = desapilar(pila_historial)
    tarea["estado"] = tarea["estado_previo"]
    posicion = tarea.pop("posicion_previa", tamanio_lista(lista_tareas))
    restaurar_posicion(lista_tareas, tarea, posicion)
    print("Tarea restaurada a la lista de pendientes.")
    return tarea


def obtener_historial(pila_historial):
    return obtener_datos_pila(pila_historial)

# ============================== FUNCIONES DE COLAS ==============================================


def agregar_solicitud(cola_soporte, id_solicitud, descripcion, prioridad, estado="Pendiente"):
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
    if cola_vacia(cola_solicitudes):
        print("No hay solicitudes para atender.")
        return None
    solicitud = atencion(cola_solicitudes)
    print("Solicitud atendida y removida de la cola.")
    return solicitud


def obtener_solicitudes(cola_soporte):
    return obtener_datos_cola(cola_soporte)


def enviar_tarea_a_mesa_ayuda(lista_tareas, cola_soporte, id_tarea, id_solicitud):
    tarea = buscar_por_id(lista_tareas, id_tarea)
    if tarea is None:
        return None
    descripcion_ticket = f"Tarea {tarea['id_tarea']}: {tarea['descripcion']}"

    return agregar_solicitud(cola_soporte, id_solicitud, descripcion_ticket, tarea["prioridad"], "Pendiente")

# ======================================= OPERACIONES DE LISTAS ARBOLES =================================================

def cargar_lista_en_arbol(lista_tareas):
    """Construye el árbol usando los datos entregados por la TDA Lista."""
    raiz = None
    for tarea in obtener_datos(lista_tareas):
        raiz = insertar_tarea_arbol(raiz, tarea)
    return raiz


def obtener_tareas_arbol(raiz, lista):
    """Recorre el árbol en inorden y agrega las tareas a una lista."""
    inorden(raiz, lista)


def obtener_complejidad():
    raiz = cargar_lista_en_arbol(lista_tareas)
    lista_ordenada = []
    obtener_tareas_arbol(raiz, lista_ordenada)
    return {
        "tareas": lista_ordenada,
        "menor": tarea_menos_compleja(raiz),
        "mayor": tarea_mas_compleja(raiz)
    }


def limpiar_tareas():
    vaciar_lista(lista_tareas)
