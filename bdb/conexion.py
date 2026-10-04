import sqlite3
import os

# Esto asegura que tareas.db se cree siempre al lado de este archivo conexion.py
RUTA_BD = os.path.join(os.path.dirname(__file__), "tareas.db")

ESTADOS_TAREA = ["Pendiente", "Completada"]
PRIORIDAD_TAREAS = {
    "baja": 3,
    "media": 2,
    "alta": 1,
}
def conectar():
    """Crea y devuelve la conexión con la base de datos."""
    return sqlite3.connect(RUTA_BD)

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
            estado TEXT,
            estado_pasado TEXT,
            nodo_anterior INTEGER,
            nodo_siguiente INTEGER,
        );
    """)

    # Si la base ya existía con la estructura anterior, agregamos
    # solamente la columna nueva sin borrar las tareas existentes.
    cursor.execute("PRAGMA table_info(tareas)")
    columnas = [fila[1] for fila in cursor.fetchall()]


    cursor.execute(
        """ALTER TABLE tareas ADD COLUMN estado_pasado TEXT DEFAULT ''
        ALTER TABLE tareas ADD COLUMN nodo_anterior TEXT DEFAULT ''
        ALTER TABLE tareas ADD COLUMN nodo_siguiente TEXT DEFAULT ''
        """)

    conexion.commit()
    conexion.close()

def guardar_tarea(descripcion, responsable="", prioridad=PRIORIDAD_TAREAS["baja"], estado=ESTADOS_TAREA[0], estado_anterior="", nodo_anterior=0, nodo_siguiente=0):
    """Inserta una tarea nueva en la base de datos."""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO tareas (descripcion, responsable, prioridad, estado, estado_anterior, nodo_anterior, nodo_siguiente)
        VALUES (?, ?, ?, ?, ?, ?, ?)""", 
        (descripcion, responsable, prioridad, estado, estado_anterior, nodo_anterior, nodo_siguiente)
    )

    conexion.commit()
    conexion.close()

def obtener_tareas():
    """Devuelve todas las tareas guardadas en la base de datos."""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM tareas
    """)

    filas = cursor.fetchall()
    conexion.close()

    lista = []

    for fila in filas:
        lista.append({
            "id": fila[0],
            "descripcion": fila[1],
            "responsable": fila[2],
            "estado": fila[3]
        })

    return lista

def obtener_tarea(id):
    """Devuelve una tarea guardada en la base de datos."""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM tareas
        WHERE id = ?
    """, (id))

    tarea = cursor.fetchone()
    conexion.close()

    return tarea

def modificar_tarea(id, descripcion, responsable, prioridad, estado, estado_anterior, nodo_anterior, nodo_siguiente):
    """Modifica una tarea de la tabla tareas"""
    conexion = conectar()
    cursor = conexion.cursor()

    tarea = obtener_tarea(id)
    estado_anterior = tarea[4]
    if not descripcion: descripcion = tarea[1]
    if not responsable: responsable = tarea[2]
    if not prioridad: prioridad = tarea[3]
    if not estado: 
        estado = tarea[4]
        estado_anterior = ''

    cursor.execute("""
        UPDATE tareas
        SET descripcion = ?, responsable = ?, prioridad = ?, estado = ?, estado_anterior = ?, nodo_anterior = ?, nodo_siguiente = ?
        WHERE id = ?
    """, (descripcion, estado, prioridad, estado_anterior, nodo_anterior, nodo_siguiente, id))

    conexion.commit()
    conexion.close()

def eliminar_tarea(id):
    """Elimina una tarea de la tabla tareas"""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        DELETE FROM TAREAS
        WHERE id = ?
    """, (id))

    conexion.commit()
    conexion.close()

# Al cargar este archivo, aseguramos que la tabla exista
# y que las bases anteriores tengan la columna responsable.
crear_tabla()
