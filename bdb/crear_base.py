import sqlite3

def cargar_base(): 
    """
    Carga y ejecuta el archivo de script SQL (base_de_datos.sql) para inicializar
    la base de datos SQLite, creando las tablas y estructuras relacionales necesarias.
    """
    conexion = sqlite3.connect("tareas.db")

    with open("base_de_datos.sql", "r", encoding="utf-8") as archivo:
        sql = archivo.read()

    conexion.executescript(sql)

    conexion.close()