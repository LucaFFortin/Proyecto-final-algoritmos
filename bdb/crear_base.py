import sqlite3

def cargar_base(): # basicamente es un script que ejecuta el archivo base_de_datos.sql para crear la base de datos y sus tablas
    conexion = sqlite3.connect("tareas.db")

    with open("base_de_datos.sql", "r", encoding="utf-8") as archivo:
        sql = archivo.read()

    conexion.executescript(sql)

    conexion.close()