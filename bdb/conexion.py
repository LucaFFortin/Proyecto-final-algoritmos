import sqlite3
import os

RUTA_DB = os.path.join(os.path.dirname(__file__), "tareas.db")

ESTADOS_TAREA = ["Pendiente", "Completada"]
PRIORIDAD_TAREAS = {
    "baja": 3,
    "media": 2,
    "alta": 1,
}
def conectar():
    return sqlite3.connect(RUTA_DB)

def crear_tabla():
    """Crea la tabla si no existe y agrega responsable a instalaciones anteriores."""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        DROP TABLE IF EXISTS tareas;

        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT,
            responsable TEXT,
            prioridad INTEGER,
            complejidad INTEGER,
            estado TEXT,
            estado_pasado TEXT,
            nodo_anterior INTEGER,
            nodo_siguiente INTEGER,
        );
    """)

    cursor.execute("PRAGMA table_info(tareas)")
    columnas = [fila[1] for fila in cursor.fetchall()]


    cursor.execute(
        """ALTER TABLE tareas ADD COLUMN estado_pasado TEXT DEFAULT ''
        ALTER TABLE tareas ADD COLUMN nodo_anterior TEXT DEFAULT ''
        ALTER TABLE tareas ADD COLUMN nodo_siguiente TEXT DEFAULT ''
        """)

    conexion.commit()
    conexion.close()

def guardar_tarea(descripcion, responsable="", prioridad=PRIORIDAD_TAREAS["baja"], complejidad=2, estado=ESTADOS_TAREA[0], estado_anterior="", nodo_anterior=0, nodo_siguiente=0):
    """Inserta una tarea nueva en la base de datos."""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO tareas (descripcion, responsable, prioridad, complejidad, estado, estado_anterior, nodo_anterior, nodo_siguiente)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
        (descripcion, responsable, prioridad, complejidad, estado, estado_anterior, nodo_anterior, nodo_siguiente)
    )

    conexion.commit()
    conexion.close()
    return id_bd


def obtener_tareas():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM tareas
    """)

    filas = cursor.fetchall()
    conexion.close()
    return datos


def actualizar_estado_tarea(id_bd, estado):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM tareas
        WHERE id = ?
    """, (id))

    tarea = cursor.fetchone()
    conexion.close()


def modificar_tarea(id, descripcion, responsable, prioridad, complejidad, estado, estado_anterior, nodo_anterior, nodo_siguiente):
    """Modifica una tarea de la tabla tareas"""
    conexion = conectar()
    cursor = conexion.cursor()

    tarea = obtener_tarea(id)
    estado_anterior = tarea[5]
    if not descripcion: descripcion = tarea[1]
    if not responsable: responsable = tarea[2]
    if not prioridad: prioridad = tarea[3]
    if not complejidad: complejidad = tarea[4]
    if not estado: 
        estado = tarea[5]
        estado_anterior = ''

    cursor.execute("""
        UPDATE tareas
        SET descripcion = ?, responsable = ?, prioridad = ?, complejidad = ?, estado = ?, estado_anterior = ?, nodo_anterior = ?, nodo_siguiente = ?
        WHERE id = ?
    """, (descripcion, prioridad, complejidad, estado, estado_anterior, nodo_anterior, nodo_siguiente, id))

    conexion.commit()
    conexion.close()
    return id_solicitud


def eliminar_tarea(id):
    """Elimina una tarea de la tabla tareas"""
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, descripcion, prioridad, estado FROM solicitudes ORDER BY id")
    datos = cursor.fetchall()
    conexion.close()
    return datos

    cursor.execute("""
        DELETE FROM TAREAS
        WHERE id = ?
    """, (id))

def actualizar_estado_solicitud(id_solicitud, estado):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("UPDATE solicitudes SET estado = ? WHERE id = ?", (estado, id_solicitud))
    conexion.commit()
    conexion.close()


inicializar_bd()
