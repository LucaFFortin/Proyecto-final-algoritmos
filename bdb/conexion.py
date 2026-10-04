import sqlite3
import os

RUTA_DB = os.path.join(os.path.dirname(__file__), "tareas.db")


def conectar():
    return sqlite3.connect(RUTA_DB)


def inicializar_bd():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            responsable TEXT NOT NULL DEFAULT '',
            prioridad INTEGER NOT NULL DEFAULT 2,
            complejidad INTEGER NOT NULL DEFAULT 1,
            estado TEXT NOT NULL DEFAULT 'pendiente'
        )
    """)

    cursor.execute("PRAGMA table_info(tareas)")
    columnas = [fila[1] for fila in cursor.fetchall()]
    if "prioridad" not in columnas:
        cursor.execute("ALTER TABLE tareas ADD COLUMN prioridad INTEGER NOT NULL DEFAULT 2")
    if "complejidad" not in columnas:
        cursor.execute("ALTER TABLE tareas ADD COLUMN complejidad INTEGER NOT NULL DEFAULT 1")
    if "responsable" not in columnas:
        cursor.execute("ALTER TABLE tareas ADD COLUMN responsable TEXT NOT NULL DEFAULT ''")
    if "estado" not in columnas:
        cursor.execute("ALTER TABLE tareas ADD COLUMN estado TEXT NOT NULL DEFAULT 'pendiente'")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS solicitudes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            prioridad INTEGER NOT NULL DEFAULT 2,
            estado TEXT NOT NULL DEFAULT 'Pendiente'
        )
    """)

    conexion.commit()
    conexion.close()


def guardar_tarea(descripcion, responsable="", prioridad=2, complejidad=1, estado="pendiente"):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO tareas (descripcion, responsable, prioridad, complejidad, estado) VALUES (?, ?, ?, ?, ?)",
        (descripcion, responsable, prioridad, complejidad, estado)
    )
    id_bd = cursor.lastrowid
    conexion.commit()
    conexion.close()
    return id_bd


def obtener_tareas():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, descripcion, responsable, prioridad, complejidad, estado FROM tareas ORDER BY id")
    datos = cursor.fetchall()
    conexion.close()
    return datos


def actualizar_estado_tarea(id_bd, estado):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("UPDATE tareas SET estado = ? WHERE id = ?", (estado, id_bd))
    conexion.commit()
    conexion.close()


def eliminar_tarea(id_bd):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM tareas WHERE id = ?", (id_bd,))
    conexion.commit()
    conexion.close()


def guardar_solicitud(descripcion, prioridad=2, estado="Pendiente"):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO solicitudes (descripcion, prioridad, estado) VALUES (?, ?, ?)",
        (descripcion, prioridad, estado)
    )
    id_solicitud = cursor.lastrowid
    conexion.commit()
    conexion.close()
    return id_solicitud


def obtener_solicitudes():
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, descripcion, prioridad, estado FROM solicitudes ORDER BY id")
    datos = cursor.fetchall()
    conexion.close()
    return datos


def actualizar_estado_solicitud(id_solicitud, estado):
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("UPDATE solicitudes SET estado = ? WHERE id = ?", (estado, id_solicitud))
    conexion.commit()
    conexion.close()


inicializar_bd()
