from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import os
from urllib.parse import urlparse, parse_qs

# Este módulo levanta un servidor HTTP estándar en Python (sin frameworks externos)
# para exponer la API consumida por el Frontend, comunicando las peticiones 
# con los Tipos de Datos Abstractos (TDA) y la base de datos relacional (SQLite).

# Configuración de rutas relativas para la importación interna de módulos de la cátedra
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "bdb")))
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import conexion
import tareas
from tda_colas import arribo, atencion, cola_vacia





def responder(handler, codigo, datos): 
    """
    Envía una respuesta HTTP estructurada en formato JSON al cliente, configurando
    los encabezados necesarios para evitar caché y habilitar políticas CORS (*).

    Parámetros:
    - handler: Instancia de BaseHTTPRequestHandler encargada de la conexión.
    - codigo: Código de estado HTTP (ej. 200, 201, 400, 404).
    - datos: Diccionario o lista de Python que se serializará como JSON.
    """

    handler.send_response(codigo)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.end_headers()
    handler.wfile.write(json.dumps(datos, ensure_ascii=False).encode("utf-8"))


class ManejadorTareas(BaseHTTPRequestHandler):
    """
    Clase manejadora de peticiones HTTP nativas de Python.
    Implementa los métodos do_GET, do_POST, do_DELETE y do_OPTIONS para dar 
    soporte completo a la API REST del sistema de administración.
    """

    def do_GET(self):
        """Maneja todas las solicitudes de lectura (GET) de la API."""
        ruta = urlparse(self.path)

        if ruta.path == "/api/tareas": # para obtener tareas 
            responder(self, 200, tareas.obtener_todas_las_tareas(tareas.lista_tareas))

        elif ruta.path == "/api/tareas/historial": # para obtener historial de tareas completadas PILA
            responder(self, 200, tareas.obtener_historial(tareas.pila_historial))

        elif ruta.path == "/api/solicitudes": # para obtener solicitudes cola
            responder(self, 200, tareas.obtener_solicitudes(tareas.cola_soporte))

        elif ruta.path == "/api/complejidad": # para la complejidad filtro ARBOL
            responder(self, 200, tareas.obtener_complejidad())

        else:
            responder(self, 404, {"mensaje": "Ruta no encontrada."})

    def do_POST(self):
        """Maneja todas las solicitudes de creación o modificación por acción (POST)."""
        ruta = urlparse(self.path)
        longitud = int(self.headers.get("Content-Length", 0))
        cuerpo = self.rfile.read(longitud) if longitud else b"{}"
        datos = json.loads(cuerpo.decode("utf-8"))

        if ruta.path == "/api/tareas":
            descripcion = datos.get("descripcion", "").strip()
            prioridad = int(datos.get("prioridad", 2))
            complejidad = int(datos.get("complejidad", 1))

            if descripcion == "":
                responder(self, 400, {"mensaje": "La descripción es obligatoria."})
                return

            id_bd = conexion.guardar_tarea(descripcion, prioridad, complejidad, "pendiente")
            id_tarea = f"tarea{id_bd}"

            tareas.agregar_tarea(
                tareas.lista_tareas,
                id_tarea,
                descripcion,
                prioridad,
                "pendiente",
                complejidad
            )

            responder(self, 201, {"mensaje": "Tarea agregada con éxito", "id": id_tarea})

        elif ruta.path == "/api/tareas/estado":
            # Cambia entre Pendiente y En Progreso y guarda el cambio en SQLite.
            id_tarea = datos.get("id")
            nuevo_estado = str(datos.get("estado", "")).strip().lower()

            if nuevo_estado not in ("pendiente", "en progreso"):
                responder(self, 400, {"mensaje": "Estado no válido."})
                return

            tarea = tareas.actualizar_estado_tarea(
                tareas.lista_tareas, id_tarea, nuevo_estado
            )

            if tarea is None:
                responder(self, 404, {"mensaje": "No se encontró la tarea."})
                return

            id_bd = int(str(id_tarea).replace("tarea", ""))
            conexion.actualizar_estado_tarea(id_bd, nuevo_estado)
            responder(self, 200, {"mensaje": "Estado actualizado.", "estado": nuevo_estado})

        elif ruta.path == "/api/tareas/editar":
            id_tarea = datos.get("id")
            if not isinstance(id_tarea, str) or not id_tarea.startswith("tarea") or not id_tarea[5:].isdigit():
                responder(self, 400, {"mensaje": "El ID de la tarea no es válido."})
                return

            descripcion = datos.get("descripcion", "")
            if not isinstance(descripcion, str) or descripcion.strip() == "":
                responder(self, 400, {"mensaje": "La descripción es obligatoria."})
                return
            descripcion = descripcion.strip()

            prioridad_dato = datos.get("prioridad")
            complejidad_dato = datos.get("complejidad")
            try:
                prioridad = int(prioridad_dato)
                complejidad = int(complejidad_dato)
            except (TypeError, ValueError):
                responder(self, 400, {"mensaje": "La prioridad y la complejidad deben ser números enteros."})
                return

            if (
                isinstance(prioridad_dato, bool)
                or isinstance(complejidad_dato, bool)
                or (isinstance(prioridad_dato, float) and not prioridad_dato.is_integer())
                or (isinstance(complejidad_dato, float) and not complejidad_dato.is_integer())
            ):
                responder(self, 400, {"mensaje": "La prioridad y la complejidad deben ser números enteros."})
                return

            if prioridad not in (1, 2, 3):
                responder(self, 400, {"mensaje": "La prioridad debe ser 1, 2 o 3."})
                return
            if complejidad < 1 or complejidad > 10:
                responder(self, 400, {"mensaje": "La complejidad debe estar entre 1 y 10."})
                return

            estado = str(datos.get("estado", "")).strip().lower()
            if estado not in ("pendiente", "en progreso"):
                responder(self, 400, {"mensaje": "El estado debe ser Pendiente o En Progreso."})
                return

            tarea = next(
                (item for item in tareas.obtener_todas_las_tareas(tareas.lista_tareas)
                 if item["id_tarea"] == id_tarea),
                None
            )
            if tarea is None:
                responder(self, 404, {"mensaje": "No se encontró la tarea activa."})
                return

            id_bd = int(id_tarea[5:])
            if not conexion.actualizar_tarea(id_bd, descripcion, prioridad, complejidad, estado):
                responder(self, 404, {"mensaje": "No se encontró la tarea en la base de datos."})
                return

            tarea_actualizada = tareas.editar_tarea(
                tareas.lista_tareas, id_tarea, descripcion, prioridad, complejidad, estado
            )
            responder(self, 200, {"mensaje": "Tarea actualizada.", "tarea": tarea_actualizada})

        elif ruta.path == "/api/tareas/completar": # para completar la tarea lista 
            id_tarea = datos.get("id")
            tarea = tareas.completar_tarea(tareas.lista_tareas, tareas.pila_historial, id_tarea)
            if tarea is None:
                responder(self, 404, {"mensaje": "No se encontró la tarea."})
                return

            id_bd = int(str(id_tarea).replace("tarea", ""))
            conexion.actualizar_estado_tarea(id_bd, "completada")
            responder(self, 200, {"mensaje": "Tarea completada."})

        elif ruta.path == "/api/tareas/deshacer": # deshacer especifica tarea PILA
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
            solicitud = {"id_solicitud": f"tarea{id_bd}", "descripcion": descripcion, "prioridad": prioridad, "estado": "Pendiente"}
            tareas.agregar_solicitud(tareas.cola_soporte, id_bd, descripcion, prioridad, "Pendiente")
            responder(self, 201, {"mensaje": "Solicitud registrada.", "id": id_bd})

        elif ruta.path == "/api/solicitudes/atender":
            if tareas.cola_vacia(tareas.cola_soporte):
                responder(self, 404, {"mensaje": "No hay solicitudes pendientes."})
                return

            solicitud = tareas.atender_solicitud(tareas.cola_soporte)
            conexion.actualizar_estado_solicitud(solicitud["id_solicitud"], "Atendida")
            # solicitud["estado"] = "Atendida"
            print(solicitud, "solicitud en el servidor")

            solicitud["complejidad"] = 1
            id_bd = conexion.guardar_tarea(solicitud["descripcion"], solicitud["prioridad"] or "baja", solicitud["complejidad"], solicitud["estado"])

            # solicitud["id_tarea"] = str(solicitud.pop("id_solicitud"))
            tareas.agregar_tarea(tareas.lista_tareas, f"tarea{id_bd}", solicitud["descripcion"], solicitud["prioridad"] or "baja", solicitud["estado"], solicitud["complejidad"])

            responder(self, 200, solicitud)

        else:
            responder(self, 404, {"mensaje": "Ruta no encontrada."})

    def do_DELETE(self):
        """Maneja las peticiones de eliminación de tareas por identificador."""

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
        """Configura los permisos de cabecera CORS para aceptar solicitudes asíncronas del Frontend."""

        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def cargar_tareas_de_base():
    """
    Inicializa la base de datos SQLite si no existe
    y carga en memoria las estructuras de TDA con los registros persistidos.
    """

    if not os.path.exists(conexion.RUTA_DB):
        ruta_sql = os.path.join(os.path.dirname(__file__), "..", "bdb", "base_de_datos.sql")
        with open(ruta_sql, "r", encoding="utf-8") as archivo:
            sql = archivo.read()
        with conexion.conectar() as bd:
            bd.executescript(sql)

    # La lista enlazada se carga con las tareas guardadas en SQLite.
    tareas.lista_tareas.inicio = None
    tareas.lista_tareas.tamanio = 0
    for fila in conexion.obtener_tareas():
        id_bd, descripcion, prioridad, complejidad, estado = fila[:5]
        dato = {
            "id_tarea": f"tarea{id_bd}",
            "descripcion": descripcion,
            "prioridad": prioridad,
            "complejidad": complejidad,
            "estado": estado
        }
        if str(estado).lower() == "completada":
            dato["estado_previo"] = "pendiente"
            tareas.apilar(tareas.pila_historial, dato)
        else:
            tareas.agregar_tarea(
                tareas.lista_tareas, f"tarea{id_bd}", descripcion,
                prioridad, estado, complejidad
            )


def cargar_solicitudes_de_base():
    """Reconstruye el TDA Cola cargando las solicitudes pendientes desde SQLite en orden FIFO."""
    tareas.cola_soporte.frente = None
    tareas.cola_soporte.final = None
    tareas.cola_soporte.tamanio = 0
    for id_solicitud, descripcion, prioridad, estado in conexion.obtener_solicitudes_pendientes():
        tareas.agregar_solicitud(
            tareas.cola_soporte, id_solicitud, descripcion, prioridad, estado
        )


if __name__ == "__main__":
    # Inicialización de estructuras desde la persistencia antes de arrancar el servidor
    cargar_tareas_de_base()
    # faltaba este para cargar las solicitudes en la base de datos a la memoria de la aplicacion.
    cargar_solicitudes_de_base()

    puerto = 8000
    servidor = HTTPServer(("localhost", puerto), ManejadorTareas)
    print(f"Servidor iniciado en http://localhost:{puerto}")
    print("Presiona Ctrl + C en la terminal para detenerlo.")
    servidor.serve_forever()
