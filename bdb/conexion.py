import sqlite3
import os

# Esto asegura que tareas.db se cree siempre al lado de este archivo conexion.py
RUTA_BD = os.path.join(os.path.dirname(__file__), "tareas.db")


def conectar():
    """Crea y devuelve la conexión con la base de datos."""
    return sqlite3.connect(RUTA_BD)


def crear_tabla():
    """Crea la tabla si no existe y agrega responsable a instalaciones anteriores."""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT,
            responsable TEXT,
            estado TEXT
        )
    """)
        
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas_completadas (
            id TEXT PRIMARY KEY,
            descripcion TEXT,
            responsable TEXT,
            estado TEXT
            estado_pasado TEXT,
            nodo_anterior TEXT,
            nodo_siguiente TEXT,
        )
    """)

    # Si la base ya existía con la estructura anterior, agregamos
    # solamente la columna nueva sin borrar las tareas existentes.
    cursor.execute("PRAGMA table_info(tareas)")
    columnas = [fila[1] for fila in cursor.fetchall()]

    if "responsable" not in columnas:
        cursor.execute(
            "ALTER TABLE tareas ADD COLUMN responsable TEXT DEFAULT ''"
        )

    conexion.commit()
    conexion.close()


def guardar_tarea(descripcion, responsable="", estado="Pendiente"):
    """Inserta una tarea nueva en la base de datos."""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO tareas (descripcion, responsable, estado)
        VALUES (?, ?, ?)
    """, (descripcion, responsable, estado))

    conexion.commit()
    conexion.close()

def obtener_tareas():
    """Devuelve todas las tareas guardadas en la base de datos."""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id, descripcion, responsable, estado
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
        SELECT id, descripcion, responsable, estado
        FROM tareas
        WHERE id = ?
    """, (id))

    tarea = cursor.fetchone()
    conexion.close()

    return tarea

def obtener_tarea_completada(id):
    """Devuelve una tarea completada guardada en la base de datos."""
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM tareas_completadas
        WHERE id = ?
    """, (id))

    tarea = cursor.fetchone()
    conexion.close()

    return tarea

def completar_tarea(id, estado_anterior, nodo_anterior, nodo_siguiente):
    """Guarda una tarea en la tabla tareas_completadas."""
    conexion = conectar()
    cursor = conexion.cursor()

    tarea = obtener_tarea(id)

    cursor.execute("""
        INSERT INTO tareas_completadas (id, descripcion, responsable, estado, estado_anterior, nodo_anterior, nodo_siguiente)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, tarea[0], tarea[1], tarea[2], tarea[3], estado_anterior, nodo_anterior, nodo_siguiente)

    # TODO:
    # habria que eliminar de la tabla tareas la tarea completada
    # o, fucionar las tablas y en tareas agregar los campos faltantes

    conexion.commit()
    conexion.close()

def deshacer_tarea_completada(id, estado_anterior, nodo_anterior, nodo_siguiente):
    """Deshace la ultima tarea guardada."""
    conexion = conectar()
    cursor = conexion.cursor()

    tarea = obtener_tarea_completada(id)

    cursor.execute("""
        INSERT INTO tareas_completadas (id, descripcion, responsable, estado, estado_anterior, nodo_anterior, nodo_siguiente)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, tarea[0], tarea[1], tarea[2], tarea[3], estado_anterior, nodo_anterior, nodo_siguiente)

    conexion.commit()
    conexion.close()

# Al cargar este archivo, aseguramos que la tabla exista
# y que las bases anteriores tengan la columna responsable.
crear_tabla()
