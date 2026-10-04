from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import os

# Agregamos las carpetas al camino de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bdb")))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import conexion
import tareas

# Funcion para manejar las peticiones de GET, POST y configurar CORS
class ManejadorTareas(BaseHTTPRequestHandler):

    # 1. Cuando la web pide ver las tareas (GET)
    def do_GET(self):
        if self.path == "/api/tareas":
            # Recorremos tu TDA Lista Enlazada real
            datos = tareas.obtener_todas_las_tareas(tareas.lista_tareas)

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            # Enviamos tus tareas del TDA a la web
            self.wfile.write(json.dumps(datos).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()

    # 2. Cuando la web envía una nueva tarea (POST)
    def do_POST(self):
        if self.path == "/api/tareas":
            longitud = int(self.headers["Content-Length"])
            cuerpo = self.rfile.read(longitud)
            datos = json.loads(cuerpo.decode("utf-8"))

            descripcion = datos.get("descripcion", "").strip()
            responsable = datos.get("responsable", "").strip()
            prioridad = int(datos.get("prioridad", 2))

            if descripcion == "" or responsable == "":
                self.send_response(400)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(
                    json.dumps({
                        "mensaje": "La descripción y el responsable son obligatorios."
                    }).encode("utf-8")
                )
                return

            id_tarea = f"tarea{tareas.lista_tareas.tamanio + 1}"

            # Mantenemos la lógica existente:
            # la tarea entra a la lista enlazada ordenada por prioridad.
            tareas.agregar_tarea(
                tareas.lista_tareas,
                id_tarea,
                descripcion,
                prioridad,
                "pendiente",
                responsable
            )

            # También la guardamos en la base de datos.

            conexion.guardar_tarea(
                descripcion,
                responsable,
                "pendiente"
            )

            self.send_response(201)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()

            self.wfile.write(
                json.dumps({
                    "mensaje": "Tarea agregada con éxito"
                }).encode("utf-8")
            )

        else:
            self.send_response(404)
            self.end_headers()

    # 3. Permisos de seguridad para el navegador
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

if __name__ == "__main__":
    puerto = 8000
    servidor = HTTPServer(("localhost", puerto), ManejadorTareas)

    print(f"Servidor iniciado en http://localhost:{puerto}")
    print("Presiona Ctrl + C en la terminal para detenerlo.")

    servidor.serve_forever()
