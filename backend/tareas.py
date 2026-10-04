from tad_arboles import nodoArbol, insertar_nodo, eliminar_nodo, arbolvacio, remplazar, buscar, preorden, inorden, postorden, por_nivel, altura
from tda_pila import Pila, apilar, desapilar, pila_vacia, en_cima, tamanio, barrido
from tda_colas import Cola, arribo, atencion, cola_vacia, en_frente, tamanio, mover_al_final
from tad_lista import Lista, insertar, lista_vacia, eliminar, tamanio, buscar, insertar_por_prioridad 

# GET = el cliente solo quiere leer datos del servidor, no quiere modificar nada.
# POST = el cliente quiere enviar datos al servidor, quiere modificar algo en el servidor.

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

tareas = {
    "tarea1": {"descripcion": "Revisar conexión de red", "prioridad": 1, "estado": "pendiente"},
    "tarea2": {"descripcion": "Configurar computadora", "prioridad": 2, "estado": "pendiente"},
    "tarea3": {"descripcion": "Instalar impresora", "prioridad": 3, "estado": "pendiente"},
}

lista_tareas = Lista()
tareas_completadas = Pila()
solicitudes_soporte = Cola()

for tarea, info in tareas.items():

    dato = {
        "id_tarea": tarea,
        "descripcion": info["descripcion"],
        "prioridad": info["prioridad"],
        "estado": info["estado"]
    }

    if (info["estado"] == "completada"):
        apilar(tareas_completadas, dato)
    

    insertar_por_prioridad(lista_tareas, dato)


# Agregado de tareas pendientes (TDA Lista Enlazada):




def agregar_tarea(lista_tareas, id, descripcion, prioridad, estado, responsable=""): # -------- agregar tarea -------------
        dato = {
            "id_tarea": id,
            "descripcion": descripcion,
            "prioridad": prioridad,
            "estado": estado,
            "responsable": responsable
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
    else:
        print("No se encontró la tarea para eliminar con el ID proporcionado.")

    return dato 




#---------------------------------------------------------------------------------------------------------------------------------------------------
    
pila_historial = Pila()


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

def obtener_todas_las_tareas(lista):
    """Recorre los nodos de la lista enlazada y devuelve una lista común para JSON."""
    resultado = []
    actual = lista.inicio
    while actual is not None:
        resultado.append(actual.info)
        actual = actual.sig
    return resultado