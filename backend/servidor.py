from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import os
from urllib.parse import urlparse, parse_qs

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bdb")))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import conexion
import tareas
from tda_colas import arribo, atencion, cola_vacia


cola_soporte = tareas.cola_soporte


def responder(handler, codigo, datos):
    handler.send_response(codigo)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    handler.wfile.write(json.dumps(datos, ensure_ascii=False).encode("utf-8"))


class ManejadorTareas(BaseHTTPRequestHandler):

    def do_GET(self):
        ruta = urlparse(self.path)

        if ruta.path == "/api/tareas":
            responder(self, 200, tareas.obtener_todas_las_tareas(tareas.lista_tareas))

        elif ruta.path == "/api/solicitudes":
            responder(self, 200, tareas.obtener_solicitudes(cola_soporte))

        elif ruta.path == "/api/complejidad":
            responder(self, 200, tareas.obtener_complejidad())

        else:
            responder(self, 404, {"mensaje": "Ruta no encontrada."})

    def do_POST(self):
        ruta = urlparse(self.path)
        longitud = int(self.headers.get("Content-Length", 0))
        cuerpo = self.rfile.read(longitud) if longitud else b"{}"
        datos = json.loads(cuerpo.decode("utf-8"))

        if ruta.path == "/api/tareas":
            descripcion = datos.get("descripcion", "").strip()
            responsable = datos.get("responsable", "").strip()
            prioridad = int(datos.get("prioridad", 2))
            complejidad = int(datos.get("complejidad", 1))

            if descripcion == "" or responsable == "":
                responder(self, 400, {"mensaje": "La descripción y el responsable son obligatorios."})
                return

            id_bd = conexion.guardar_tarea(descripcion, responsable, prioridad, complejidad, "pendiente")
            id_tarea = f"tarea{id_bd}"

            tareas.agregar_tarea(
                tareas.lista_tareas,
                id_tarea,
                descripcion,
                prioridad,
                "pendiente",
                responsable,
                complejidad
            )

            responder(self, 201, {"mensaje": "Tarea agregada con éxito", "id": id_tarea})

        elif ruta.path == "/api/tareas/completar":
            id_tarea = datos.get("id")
            tarea = tareas.completar_tarea(tareas.lista_tareas, tareas.pila_historial, id_tarea)
            if tarea is None:
                responder(self, 404, {"mensaje": "No se encontró la tarea."})
                return

            id_bd = int(str(id_tarea).replace("tarea", ""))
            conexion.actualizar_estado_tarea(id_bd, "completada")
            responder(self, 200, {"mensaje": "Tarea completada."})

        elif ruta.path == "/api/tareas/deshacer":
            tarea = tareas.deshacer_ultima_completada(tareas.lista_tareas, tareas.pila_historial)
            if tarea is None:
                responder(self, 404, {"mensaje": "No hay tareas completadas para deshacer."})
                return

            id_bd = int(str(tarea["id_tarea"]).replace("tarea", ""))
            conexion.actualizar_estado_tarea(id_bd, tarea["estado"])
            responder(self, 200, {"mensaje": "Última tarea completada restaurada."})

        elif ruta.path == "/api/solicitudes":
            descripcion = datos.get("descripcion", "").strip()
            prioridad = int(datos.get("prioridad", 2))
            if descripcion == "":
                responder(self, 400, {"mensaje": "La descripción es obligatoria."})
                return

            id_bd = conexion.guardar_solicitud(descripcion, prioridad, "Pendiente")
            solicitud = {"id_solicitud": id_bd, "descripcion": descripcion, "prioridad": prioridad, "estado": "Pendiente"}
            arribo(cola_soporte, solicitud)
            responder(self, 201, {"mensaje": "Solicitud registrada.", "id": id_bd})

        elif ruta.path == "/api/solicitudes/atender":
            if cola_vacia(cola_soporte):
                responder(self, 404, {"mensaje": "No hay solicitudes pendientes."})
                return

            solicitud = atencion(cola_soporte)
            conexion.actualizar_estado_solicitud(solicitud["id_solicitud"], "Atendida")
            solicitud["estado"] = "Atendida"
            responder(self, 200, solicitud)

        else:
            responder(self, 404, {"mensaje": "Ruta no encontrada."})

    def do_DELETE(self):
        ruta = urlparse(self.path)
        parametros = parse_qs(ruta.query)

        if ruta.path != "/api/tareas" or "id" not in parametros:
            responder(self, 400, {"mensaje": "Debe indicar el ID de la tarea."})
            return

        id_tarea = parametros["id"][0]
        tarea = tareas.eliminar_id(tareas.lista_tareas, id_tarea)
        if tarea is None:
            responder(self, 404, {"mensaje": "No se encontró la tarea."})
            return

        id_bd = int(str(id_tarea).replace("tarea", ""))
        conexion.eliminar_tarea(id_bd)
        responder(self, 200, {"mensaje": "Tarea eliminada."})

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


if __name__ == "__main__":
    puerto = 8000
    servidor = HTTPServer(("localhost", puerto), ManejadorTareas)
    print(f"Servidor iniciado en http://localhost:{puerto}")
    print("Presiona Ctrl + C en la terminal para detenerlo.")
    servidor.serve_forever()
