from tad_arboles import nodoArbol, insertar_nodo, eliminar_nodo, arbolvacio, remplazar, buscar, preorden, inorden, postorden, por_nivel, altura
from tda_pila import Pila, apilar, desapilar, pila_vacia, en_cima, tamanio, barrido
from tda_colas import Cola, arribo, atencion, cola_vacia, en_frente, tamanio, mover_al_final
from tad_lista import Lista, insertar, lista_vacia, eliminar, tamanio, buscar, insertar_por_prioridad 


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
- Permitir deshacer la última completada y restaurar su estado anterior en SQLite.

Cola — Tickets de soporte
- Registrar solicitudes de los empleados.
- Agregar cada ticket al final mediante arribo().
- Mostrar los usuarios en orden de llegada.
- Atender al primero mediante atencion() y retirarlo de la cola.
"""


"""
Recibir la nueva tarea.
Comparar su prioridad con la primera tarea.
Si corresponde antes, pasa a ser la primera.
Si no, avanzar por la lista.
Buscar el punto donde debe insertarse.
Enlazarla ahí.
Mantener el resto de la lista conectado.
"""

"""
┌──────────────────────┐
│      FRONTEND        │
│ HTML + CSS + JS      │
│                      │
│  Usuario interactúa  │
└──────────┬───────────┘
           │
           │ fetch()
           │ HTTP
           ▼
┌──────────────────────┐
│       BACKEND        │
│      Python          │
│                      │
│ http.server          │
│ lógica del sistema   │
│ TDA Lista            │
│ TDA Pila             │
│ TDA Cola             │
│ TDA Árbol            │
└──────────┬───────────┘
           │
           │ sqlite3
           ▼
┌──────────────────────┐
│    BASE DE DATOS     │
│       SQLite         │
│                      │
│ tareas               │
│ soporte              │
└──────────────────────┘
"""

#El "puente" entre frontend y backend sería HTTP + JSON.
#El puente entre backend y base de datos sería sqlite3.

# prioridad: 1 (alta), 2 (media), 3 (baja)
#  estado actual (Pendiente, En Progreso, Completada). 

lista_tareas = Lista()


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


def eliminar_id(lista_tareas, id): # -------- eliminar tarea -------------
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




#---------------------------------------------------------------------------------------------------------------------------------------------------
    
pila_historial = Pila()

# en un despegable historial de completado 
# el usuario va elegir un id = como tarea1, tarea2, tarea3, y se va a marcar como completada, y se va a mover de la lista a la pila historial.

def completar_tarea(lista_tareas, pila_historial, id):
    """Marca una tarea como completada y la mueve de la lista a la pila."""
    tarea = eliminar_id(lista_tareas, id)

    if tarea is not None:
        tarea["estado_previo"] = tarea["estado"] # estado que tenia antes de completarla, para poder restaurarla si se deshace
        tarea["estado"] = "completada" # marca la tarea como completada
        apilar(pila_historial, tarea)
        print("Tarea completada y movida al historial.")
    else:
        print("No se encontró la tarea para completar.")

def deshacer_ultima_completada(lista_tareas, pila_historial):
    """Desapila la última tarea completada y la restaura a pendientes."""
    if pila_vacia(pila_historial):
        print("No hay tareas completadas para deshacer.")
        return None

    tarea = desapilar(pila_historial)
    tarea["estado"] = tarea["estado_previo"]
    insertar_por_prioridad(lista_tareas, tarea) # ya que dice la consigna volverlo a la lista de pendientes, y como es por prioridad lo vuelvo a insertar por prioridad
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



# Arboles 
# Tarea más compleja y menos compleja lo va a ir ordenando en la lista de tareas / se tiene que pasar al mismo tiempo de lista al arbol
# listar el conjunto mediante inorden


# Despegable menor compleja buscador diciendo si queres la más compleja y menos compleja


