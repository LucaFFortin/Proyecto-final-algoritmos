
import sqlite3
import os

RUTA_DB = os.path.join(os.path.dirname(__file__), "tareas.db")

ESTADOS_TAREA = ["Pendiente","En Progreso" ,"Completada"]

PRIORIDAD_TAREAS = {
    "baja": 3,
    "media": 2,
    "alta": 1,
}



def conectar():
    """Establece la conexión con la base de datos SQLite."""
    return sqlite3.connect(RUTA_DB)

    


def guardar_tarea(descripcion, prioridad= PRIORIDAD_TAREAS["baja"], complejidad= 2, estado= ESTADOS_TAREA[0]): # para lista 
    """Inserta una tarea nueva en la base de datos."""

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO tareas (
            descripcion,
            prioridad,
            complejidad,
            estado
        )
        VALUES (?, ?, ?, ?)
    """, (
        descripcion,
        prioridad,
        complejidad,
        estado,
    ))

    id_bd = cursor.lastrowid

    conexion.commit()
    conexion.close()

    return id_bd


def obtener_tareas(): # Recupera todas las tareas guardadas.Lista de tareas
    """Obtiene todas las tareas de la base de datos."""

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""SELECT * FROM tareas""")

    filas = cursor.fetchall()

    conexion.close()
    return id_bd


    return filas


def obtener_tarea(id): # Busca una tarea por su ID.Lista de tareas
    """Obtiene una tarea específica por su ID."""

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""SELECT * FROM tareas WHERE id = ?""", (id,))

    tarea = cursor.fetchone()

    conexion.close()
    return datos

    return tarea


def actualizar_estado_tarea(id_bd, estado): # Lista y operación de deshacer para la pila ya que necesita actualizar el estado de la tarea en la base de datos
    """Actualiza el estado de una tarea."""

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""UPDATE tareas SET estado = ? WHERE id = ?""", (estado, id_bd))

    conexion.commit()
    conexion.close()


def modificar_tarea(id,descripcion,prioridad, complejidad, estado): # Lista de tareas
    """Modifica una tarea de la tabla tareas."""

    conexion = conectar()
    cursor = conexion.cursor()

    tarea = obtener_tarea(id)

    if tarea is None:
        conexion.close()
        return None

    if not descripcion:
        descripcion = tarea[1]

    if not prioridad:
        prioridad = tarea[2]

    if not complejidad:
        complejidad = tarea[3]

    if not estado:
        estado = tarea[4]

    cursor.execute("""
        UPDATE tareas
        SET
            descripcion = ?,
            prioridad = ?,
            complejidad = ?,
            estado = ?,
        WHERE id = ?
    """, (
        descripcion,
        prioridad,
        complejidad,
        estado,
        id
    ))

    conexion.commit()
    conexion.close()
    return id_solicitud

    return id


def eliminar_tarea(id): # Lista de tareas
    """Elimina una tarea de la tabla tareas."""

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""DELETE FROM tareas WHERE id = ?""", (id,))

    conexion.commit()
    conexion.close()


#---------------------------------------------------------------------------------------------------------------------------------------------

def guardar_solicitud(descripcion, prioridad=2, estado="Pendiente"): # Para guardar una nueva solicitud en la base de datos. Cola de solicitudes
    """Inserta una nueva solicitud en la base de datos."""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO solicitudes (descripcion, prioridad, estado)
        VALUES (?, ?, ?)
    """, (descripcion, prioridad, estado))

    id_solicitud = cursor.lastrowid

    conexion.commit()
    conexion.close()

    return id_solicitud

def actualizar_estado_solicitud(id_solicitud, estado): # Para actualizar el estado de una solicitud en la base de datos. Cola de solicitudes
    """Actualiza el estado de una solicitud."""

    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""UPDATE solicitudes SET estado = ? WHERE id = ?""", (estado, id_solicitud))

    conexion.commit()
    conexion.close()

def obtener_solicitudes_pendientes(): # Esta función permite reconstruir la cola cuando se inicia el servidor. Cola de solicitudes
    """Obtiene todas las solicitudes pendientes de la base de datos."""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, descripcion, prioridad, estado
        FROM solicitudes
        WHERE estado = 'Pendiente'
        ORDER BY id ASC
    """)

    filas = cursor.fetchall()
    conexion.close()

    return filas
