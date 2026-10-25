// el javascript solicita el historial al servidor 
// python recibe la solicitud y consulta la pila de historial para devolverla al js
// el servidor devuelve la lista de tareas en formato JSON 
// recorre las tareas y crea los elementos html para mostrarlas en la ventana de historial


let tareas = [];
let tareasFiltradas = [];


// paginación
let paginaActual = 1;
const tareasPorPagina = 5; // Número de tareas a mostrar por página



// llama a cada class o id del html para poder manipularlos desde el js
const listaTareas = document.getElementById("listaTareas");
const paginacion = document.getElementById("paginacion");
const sinResultados = document.getElementById("sinResultados");
const inputBuscar = document.getElementById("buscarTarea");
const botonBuscar = document.getElementById("botonBuscar");

const ventanaTarea = document.getElementById("ventanaTarea");
const botonNuevaTarea = document.getElementById("botonNuevaTarea");
const botonCancelarVentana = document.getElementById("botonCancelarVentana");
const formularioTarea = document.getElementById("formularioTarea");
const inputDescripcion = document.getElementById("inputDescripcion");
const inputPrioridad = document.getElementById("inputPrioridad");
const inputComplejidad = document.getElementById("inputComplejidad");

const ventanaSolicitud = document.getElementById("ventanaSolicitud");
const formularioSolicitud = document.getElementById("formularioSolicitud");
const inputSolicitud = document.getElementById("inputSolicitud");
const inputPrioridadSolicitud = document.getElementById("inputPrioridadSolicitud");
const botonMesaAyuda = document.getElementById("botonMesaAyuda");
const menuMesaAyuda = document.getElementById("menuMesaAyuda");
const botonMenuHistorial = document.getElementById("botonMenuHistorial");
const menuHistorial = document.getElementById("menuHistorial");
const ventanaHistorial = document.getElementById("ventanaHistorial");
const listaHistorial = document.getElementById("listaHistorial");

// menu responsive
const botonMenuPrincipal = document.getElementById("botonMenuPrincipal");
const accionesCabecera = document.getElementById("accionesCabecera");

function obtenerTextoPrioridad(prioridad) {
    if (Number(prioridad) === 1) return "Alta";
    if (Number(prioridad) === 3) return "Baja";
    return "Media";
}

function obtenerClaseEstado(estado) {
    const est = (estado || "pendiente").toString().toLowerCase();
    if (est === "completada") return "completada";
    if (est === "en progreso" || est === "en proceso") return "en-proceso";
    return "pendiente";
}

function obtenerTextoEstado(estado) {
    const est = (estado || "pendiente").toString().toLowerCase();
    if (est === "en progreso" || est === "en proceso") return "En Progreso";
    if (est === "completada") return "Completada";
    return "Pendiente";
}

// solo para que muestre las tareas en la página actual python se va encargando de traer las tareas desde la base de datos
function mostrarTareas() {
    listaTareas.innerHTML = "";
    const inicio = (paginaActual - 1) * tareasPorPagina;
    const tareasDeLaPagina = tareasFiltradas.slice(inicio, inicio + tareasPorPagina);

    if (tareasDeLaPagina.length === 0) {
        sinResultados.style.display = "block";
        return;
    }
    sinResultados.style.display = "none";

    tareasDeLaPagina.forEach(tarea => {
        const elemento = document.createElement("article");
        elemento.classList.add("tarea");
        elemento.innerHTML = `
            <div class="tarea-info">
                <h2>${tarea.titulo}</h2>
                <p><strong>ID:</strong> ${tarea.id} </p>
                <p><strong>Prioridad:</strong> ${obtenerTextoPrioridad(tarea.prioridad)}</p> 
                <p><strong>Complejidad:</strong> ${tarea.complejidad}</p>
            </div>
            <div class="tarea-acciones">
                <button class="boton-ticket" data-id="${tarea.id}">Enviar a mesa de ayuda</button>
                <button class="estado estado-clickeable ${obtenerClaseEstado(tarea.estado)}"
                        data-id="${tarea.id}" aria-label="Cambiar estado de la tarea"
                        title="Hacé clic para cambiar entre Pendiente y En Progreso">${obtenerTextoEstado(tarea.estado)}</button>
                <div>
                    <button class="boton-completar" data-id="${tarea.id}">Completar</button>
                    <button class="boton-eliminar" data-id="${tarea.id}">Eliminar</button>
                </div>
            </div>
        `;
        listaTareas.appendChild(elemento);
    });

    document.querySelectorAll(".boton-ticket").forEach(boton => {
        boton.addEventListener("click", () => crearTicketDesdeTarea(boton.dataset.id, boton));
    });
    document.querySelectorAll(".estado-clickeable").forEach(boton => {
        boton.addEventListener("click", () => cambiarEstadoTarea(boton.dataset.id));
    });
    document.querySelectorAll(".boton-completar").forEach(boton => {
        boton.addEventListener("click", () => completarTarea(boton.dataset.id));
    });
    document.querySelectorAll(".boton-eliminar").forEach(boton => {
        boton.addEventListener("click", () => eliminarTarea(boton.dataset.id));
    });
}

// crea la paginación según la cantidad de tareas filtradas

function crearPaginacion() {
    paginacion.innerHTML = "";
    const cantidadPaginas = Math.ceil(tareasFiltradas.length / tareasPorPagina);
    if (cantidadPaginas <= 1) return;

    for (let numero = 1; numero <= cantidadPaginas; numero++) {
        const boton = document.createElement("button");
        boton.className = "boton-pagina" + (numero === paginaActual ? " activa" : "");
        boton.textContent = numero;
        boton.addEventListener("click", () => {
            paginaActual = numero;
            mostrarTareas();
            crearPaginacion();
        });
        paginacion.appendChild(boton);
    }
}

// busca las tareas según el texto ingresado en el input de búsqueda y actualiza la lista de tareas mostradas
function buscarTareas() {
    const texto = inputBuscar.value.trim().toLowerCase();
    tareasFiltradas = texto === "" ? tareas : tareas.filter(tarea =>
        (tarea.titulo || "").toLowerCase().includes(texto) ||
        (tarea.id || "").toLowerCase().includes(texto) ||
        (tarea.estado || "").toLowerCase().includes(texto)
    );
    paginaActual = 1;
    mostrarTareas();
    crearPaginacion();
}

// carga las tareas desde el servidor y actualiza la lista de tareas mostradas

function cargarTareasDesdeServidor() {
    fetch("http://localhost:8000/api/tareas", { cache: "no-store" })
        .then(respuesta => respuesta.json())
        .then(datos => {
            tareas = datos.map(t => ({
                id: t.id_tarea,
                titulo: t.descripcion,
                prioridad: t.prioridad || 2,
                complejidad: t.complejidad || 1,
                estado: t.estado || "Pendiente"
            }));
            tareasFiltradas = tareas;
            paginaActual = 1;
            mostrarTareas();
            crearPaginacion();
        })
        .catch(() => console.warn("Servidor Python desconectado."));
}

// Convierte la tarea elegida en un ticket pendiente de la mesa de ayuda.
function crearTicketDesdeTarea(id, boton) {
    const tarea = tareas.find(t => t.id === id);
    if (!tarea) return;

    boton.disabled = true;
    boton.textContent = "Creando ticket...";

    fetch("http://localhost:8000/api/solicitudes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            descripcion: `Tarea ${tarea.id}: ${tarea.titulo}`,
            prioridad: Number(tarea.prioridad)
        })
    })
    .then(respuesta => respuesta.json().then(datos => ({ ok: respuesta.ok, datos })))
    .then(({ ok, datos }) => {
        if (!ok) throw new Error(datos.mensaje || "No se pudo crear el ticket.");
        boton.textContent = "Ticket creado";
        boton.classList.add("ticket-creado");
        alert(`La tarea se convirtió en el ticket ${datos.id}. Podés encontrarlo en Mesa de ayuda > Solicitudes pendientes.`);
    })
    .catch(error => {
        boton.disabled = false;
        boton.textContent = "Enviar a mesa de ayuda";
        alert(error.message || "No se pudo crear el ticket.");
    });
}

// Alterna el estado con un clic y guarda el cambio en el servidor y SQLite.
function cambiarEstadoTarea(id) {
    const tarea = tareas.find(t => t.id === id);
    if (!tarea) return;

    const estadoActual = (tarea.estado || "pendiente").toLowerCase();
    const nuevoEstado = estadoActual === "en progreso" ? "pendiente" : "en progreso";

    fetch("http://localhost:8000/api/tareas/estado", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: id, estado: nuevoEstado })
    })
    .then(respuesta => respuesta.json().then(datos => ({ ok: respuesta.ok, datos })))
    .then(({ ok, datos }) => {
        if (!ok) throw new Error(datos.mensaje || "No se pudo cambiar el estado.");
        cargarTareasDesdeServidor();
    })
    .catch(error => alert(error.message || "No se pudo cambiar el estado."));
}

// envía una solicitud al servidor para completar una tarea y recarga la lista de tareas
function completarTarea(id) {
    fetch("http://localhost:8000/api/tareas/completar", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id })
    })
    .then(r => r.json())
    .then(datos => {
        if (!datos.mensaje) throw new Error();
        cargarTareasDesdeServidor();
    })
    .catch(() => alert("No se pudo completar la tarea."));
}

// envía una solicitud al servidor para eliminar una tarea y recarga la lista de tareas
function eliminarTarea(id) {
    if (!confirm("¿Eliminar esta tarea?")) return;
    fetch(`http://localhost:8000/api/tareas?id=${encodeURIComponent(id)}`, { method: "DELETE" })
        .then(r => r.json())
        .then(() => cargarTareasDesdeServidor())
        .catch(() => alert("No se pudo eliminar la tarea."));
}

botonNuevaTarea.addEventListener("click", () => {
    ventanaTarea.style.display = "flex";
    inputDescripcion.focus();
});

botonCancelarVentana.addEventListener("click", () => {
    formularioTarea.reset();
    ventanaTarea.style.display = "none";
});

ventanaTarea.addEventListener("click", evento => {
    if (evento.target === ventanaTarea) ventanaTarea.style.display = "none";
});

// envía una solicitud al servidor para crear una nueva tarea y recarga la lista de tareas
formularioTarea.addEventListener("submit", evento => {
    evento.preventDefault();
    fetch("http://localhost:8000/api/tareas", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            descripcion: inputDescripcion.value.trim(),
            prioridad: Number(inputPrioridad.value),
            complejidad: Number(inputComplejidad.value)
        })
    })
    .then(r => r.json().then(datos => ({ ok: r.ok, datos })))
    .then(({ ok, datos }) => {
        if (!ok) throw new Error(datos.mensaje);
        formularioTarea.reset();
        ventanaTarea.style.display = "none";
        cargarTareasDesdeServidor();
    })
    .catch(error => alert(error.message || "No se pudo guardar la tarea."));
});

// Abre el menú de tres rayitas y muestra el historial guardado en la pila.
botonMenuHistorial.addEventListener("click", evento => {
    evento.stopPropagation();
    menuHistorial.classList.toggle("mostrar");

    menuMesaAyuda.classList.remove("mostrar");
    botonMenuHistorial.setAttribute("aria-expanded", menuHistorial.classList.contains("mostrar"));
});

document.getElementById("botonAbrirHistorial").addEventListener("click", () => {
    menuHistorial.classList.remove("mostrar");
    ventanaHistorial.style.display = "flex";
    cargarHistorial();
});

document.getElementById("botonCerrarHistorial").addEventListener("click", () => {
    ventanaHistorial.style.display = "none";
});

ventanaHistorial.addEventListener("click", evento => {
    if (evento.target === ventanaHistorial) ventanaHistorial.style.display = "none";
});

function cargarHistorial() { // carga el historial de tareas completadas desde el servidor y actualiza la lista de historial mostradas
    fetch("http://localhost:8000/api/tareas/historial", { cache: "no-store" })
        .then(respuesta => respuesta.json())
        .then(historial => {
            listaHistorial.innerHTML = "";
            if (historial.length === 0) {
                listaHistorial.innerHTML = '<p class="historial-vacio">Todavía no hay tareas completadas.</p>';
                return;
            }
            historial.forEach(tarea => {
                const elemento = document.createElement("article");
                elemento.className = "item-historial";
                elemento.innerHTML = `
                    <div><strong>${tarea.descripcion}</strong>
                    <p>ID: ${tarea.id_tarea} · Prioridad: ${obtenerTextoPrioridad(tarea.prioridad)} · Complejidad: ${tarea.complejidad}</p></div>
                    <span class="estado completada">Completada</span>`;
                listaHistorial.appendChild(elemento);
            });
        })
        .catch(() => { listaHistorial.innerHTML = '<p class="historial-vacio">No se pudo cargar el historial. Revisá que el servidor esté iniciado.</p>'; });
}

// envía una solicitud al servidor para deshacer la última tarea completada y recarga las listas
document.getElementById("botonDeshacer").addEventListener("click", () => {
    menuHistorial.classList.remove("mostrar");
    fetch("http://localhost:8000/api/tareas/deshacer", { method: "POST" })
        .then(r => r.json().then(datos => ({ ok: r.ok, datos })))
        .then(({ ok, datos }) => {
            if (!ok) throw new Error(datos.mensaje);
            cargarTareasDesdeServidor();
            cargarHistorial();
        })
        .catch(error => alert(error.message));
});

botonMesaAyuda.addEventListener("click", evento => {
    evento.stopPropagation();
    menuMesaAyuda.classList.toggle("mostrar");

    menuHistorial.classList.remove("mostrar");
});

document.addEventListener("click", evento => {
    if (!evento.target.closest(".desplegable-ayuda")) {
        menuMesaAyuda.classList.remove("mostrar");
    }
    if (!evento.target.closest(".desplegable-historial")) {
        menuHistorial.classList.remove("mostrar");
        botonMenuHistorial.setAttribute("aria-expanded", "false");
    }
});

document.getElementById("botonNuevaSolicitud").addEventListener("click", () => {
    menuMesaAyuda.classList.remove("mostrar");
    ventanaSolicitud.style.display = "flex";
    inputSolicitud.focus();
});

document.getElementById("botonCancelarSolicitud").addEventListener("click", () => {
    formularioSolicitud.reset();
    ventanaSolicitud.style.display = "none";
});

ventanaSolicitud.addEventListener("click", evento => {
    if (evento.target === ventanaSolicitud) ventanaSolicitud.style.display = "none";
});
// envía una solicitud al servidor para crear una nueva solicitud y recarga la lista de solicitudes
formularioSolicitud.addEventListener("submit", evento => {
    evento.preventDefault();
    fetch("http://localhost:8000/api/solicitudes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            descripcion: inputSolicitud.value.trim(),
            prioridad: Number(inputPrioridadSolicitud.value)
        })
    })
    .then(r => r.json().then(datos => ({ ok: r.ok, datos })))
    .then(({ ok, datos }) => {
        if (!ok) throw new Error(datos.mensaje);
        formularioSolicitud.reset();
        ventanaSolicitud.style.display = "none";
        cargarSolicitudes();
    })
    .catch(error => alert(error.message || "No se pudo registrar la solicitud."));
});
// Variables para paginar las solicitudes: mostramos 6 por página.
const ventanaSolicitudes = document.getElementById("ventanaSolicitudes");
const listaSolicitudes = document.getElementById("listaSolicitudes");
const mensajeSolicitudes = document.getElementById("mensajeSolicitudes");
const solicitudesPorPagina = 6;
let paginaSolicitudesActual = 1;
let solicitudesMostradas = [];
let tipoSolicitudes = "pendientes";

// Cambia de página sin volver a consultar el servidor.
document.getElementById("paginaAnterior").addEventListener("click", () => {
    if (paginaSolicitudesActual > 1) {
        paginaSolicitudesActual--;
        mostrarPaginaSolicitudes();
    }
});

document.getElementById("paginaSiguiente").addEventListener("click", () => {
    const totalPaginas = Math.ceil(solicitudesMostradas.length / solicitudesPorPagina);
    if (paginaSolicitudesActual < totalPaginas) {
        paginaSolicitudesActual++;
        mostrarPaginaSolicitudes();
    }
});

document.getElementById("botonVerSolicitudes").addEventListener("click", () => {
    menuMesaAyuda.classList.remove("mostrar");
    ventanaSolicitudes.style.display = "flex";
    mensajeSolicitudes.textContent = "";
    document.querySelector("#ventanaSolicitudes h2").textContent = "Solicitudes de mesa de ayuda";
    document.querySelector("#ventanaSolicitudes .cabecera-historial p").textContent = "Se atienden en orden de llegada (primero en entrar, primero en salir).";
    document.getElementById("botonAtenderSolicitud").style.display = "";
    tipoSolicitudes = "pendientes";
    cargarSolicitudes();
});

document.getElementById("botonVerSolicitudesAtendidas").addEventListener("click", () => {
    menuMesaAyuda.classList.remove("mostrar");
    ventanaSolicitudes.style.display = "flex";
    mensajeSolicitudes.textContent = "";
    document.querySelector("#ventanaSolicitudes h2").textContent = "Solicitudes atendidas";
    document.querySelector("#ventanaSolicitudes .cabecera-historial p").textContent = "Historial de solicitudes que ya fueron atendidas.";
    document.getElementById("botonAtenderSolicitud").style.display = "none";
    tipoSolicitudes = "atendidas";
    cargarSolicitudesAtendidas();
});

document.getElementById("botonCerrarSolicitudes").addEventListener("click", () => {
    ventanaSolicitudes.style.display = "none";
});

ventanaSolicitudes.addEventListener("click", evento => {
    if (evento.target === ventanaSolicitudes) ventanaSolicitudes.style.display = "none";
});

// Atiende y retira de la cola únicamente la solicitud que está al frente.
document.getElementById("botonAtenderSolicitud").addEventListener("click", () => {
    fetch("http://localhost:8000/api/solicitudes/atender", { method: "POST" })
        .then(r => r.json().then(datos => ({ ok: r.ok, datos })))
        .then(({ ok, datos }) => {
            if (!ok) throw new Error(datos.mensaje || "No se pudo atender la solicitud.");
            mensajeSolicitudes.textContent = `Solicitud ${datos.id_solicitud} atendida: ${datos.descripcion}`;
            cargarSolicitudes();
        })
        .catch(error => {
            mensajeSolicitudes.textContent = error.message;
            cargarSolicitudes();
        });
});

// Consulta las solicitudes pendientes y prepara el paginado.
function cargarSolicitudes() {
    fetch("http://localhost:8000/api/solicitudes", { cache: "no-store" })
        .then(respuesta => {
            if (!respuesta.ok) throw new Error("No se pudieron cargar las solicitudes.");
            return respuesta.json();
        })
        .then(solicitudes => {
            solicitudesMostradas = solicitudes;
            tipoSolicitudes = "pendientes";
            paginaSolicitudesActual = 1;
            mostrarPaginaSolicitudes();
        })
        .catch(error => mostrarErrorSolicitudes(error.message));
}

// Consulta las solicitudes atendidas y prepara el mismo paginado.
function cargarSolicitudesAtendidas() {
    fetch("http://localhost:8000/api/solicitudes/atendidas", { cache: "no-store" })
        .then(respuesta => {
            if (!respuesta.ok) throw new Error("No se pudieron cargar las solicitudes atendidas.");
            return respuesta.json();
        })
        .then(solicitudes => {
            solicitudesMostradas = solicitudes;
            tipoSolicitudes = "atendidas";
            paginaSolicitudesActual = 1;
            mostrarPaginaSolicitudes();
        })
        .catch(error => mostrarErrorSolicitudes(error.message));
}

// Muestra solamente las seis solicitudes que corresponden a la página actual.
function mostrarPaginaSolicitudes() {
    listaSolicitudes.innerHTML = "";

    if (solicitudesMostradas.length === 0) {
        const texto = tipoSolicitudes === "atendidas"
            ? "Todavía no hay solicitudes atendidas."
            : "No hay solicitudes pendientes.";
        listaSolicitudes.innerHTML = `<p class="historial-vacio">${texto}</p>`;
        document.getElementById("paginadoSolicitudes").style.display = "none";
        return;
    }

    const inicio = (paginaSolicitudesActual - 1) * solicitudesPorPagina;
    const fin = inicio + solicitudesPorPagina;
    const solicitudesPagina = solicitudesMostradas.slice(inicio, fin);

    solicitudesPagina.forEach((solicitud, indice) => {
        const elemento = document.createElement("article");
        elemento.className = "item-historial";
        const info = document.createElement("div");
        const titulo = document.createElement("strong");

        if (tipoSolicitudes === "pendientes") {
            titulo.textContent = `${inicio + indice === 0 ? "Siguiente en atender · " : ""}Solicitud ${solicitud.id_solicitud}`;
        } else {
            titulo.textContent = `Solicitud ${solicitud.id_solicitud}`;
        }

        const detalle = document.createElement("p");
        detalle.textContent = `${solicitud.descripcion} · Prioridad: ${obtenerTextoPrioridad(solicitud.prioridad)}`;
        info.append(titulo, detalle);

        const estado = document.createElement("span");
        estado.className = tipoSolicitudes === "atendidas" ? "estado atendida" : "estado pendiente";
        estado.textContent = solicitud.estado || (tipoSolicitudes === "atendidas" ? "Atendida" : "Pendiente");

        elemento.append(info, estado);
        listaSolicitudes.appendChild(elemento);
    });

    const totalPaginas = Math.ceil(solicitudesMostradas.length / solicitudesPorPagina);
    const paginado = document.getElementById("paginadoSolicitudes");
    paginado.style.display = totalPaginas > 1 ? "flex" : "none";
    document.getElementById("numeroPagina").textContent = `Página ${paginaSolicitudesActual} de ${totalPaginas}`;
    document.getElementById("paginaAnterior").disabled = paginaSolicitudesActual === 1;
    document.getElementById("paginaSiguiente").disabled = paginaSolicitudesActual === totalPaginas;
}

function mostrarErrorSolicitudes(texto) {
    listaSolicitudes.innerHTML = "";
    const mensaje = document.createElement("p");
    mensaje.className = "historial-vacio";
    mensaje.textContent = texto;
    listaSolicitudes.appendChild(mensaje);
    document.getElementById("paginadoSolicitudes").style.display = "none";
}

// Pide al servidor las tareas ordenadas por el árbol de complejidad.
const ventanaComplejidad = document.getElementById("ventanaComplejidad");

document.getElementById("botonComplejidad").addEventListener("click", () => {
    fetch("http://localhost:8000/api/complejidad")
        .then(r => r.json())
        .then(datos => {
            const contenedor = document.getElementById("listaComplejidad");
            const resumen = document.getElementById("resumenComplejidad");

            if (datos.tareas.length === 0) {
                resumen.innerHTML = "";
                contenedor.innerHTML = "<p>No hay tareas para mostrar.</p>";
            } else {
                resumen.innerHTML = `
                    <p><strong>Menor complejidad:</strong> ${datos.menor.descripcion} (${datos.menor.complejidad})</p>
                    <p><strong>Mayor complejidad:</strong> ${datos.mayor.descripcion} (${datos.mayor.complejidad})</p>`;
                contenedor.innerHTML = datos.tareas.map(t =>
                    `<div class="item-historial"><div><strong>${t.id_tarea}</strong> - ${t.descripcion}<p>Complejidad: ${t.complejidad}</p></div></div>`
                ).join("");
            }
            ventanaComplejidad.style.display = "flex";
        })
        .catch(error => alert("No se pudieron cargar las tareas por complejidad."));
});

document.getElementById("botonCerrarComplejidad").addEventListener("click", () => {
    ventanaComplejidad.style.display = "none";
});

ventanaComplejidad.addEventListener("click", evento => {
    if (evento.target === ventanaComplejidad) ventanaComplejidad.style.display = "none";
});

botonBuscar.addEventListener("click", buscarTareas);
inputBuscar.addEventListener("keydown", evento => {
    if (evento.key === "Enter") buscarTareas();
});

document.addEventListener("keydown", evento => {
    if (evento.key === "Escape") {
        ventanaTarea.style.display = "none";
        ventanaSolicitud.style.display = "none";
        ventanaHistorial.style.display = "none";
        ventanaComplejidad.style.display = "none";
        ventanaSolicitudes.style.display = "none";
        menuMesaAyuda.classList.remove("mostrar");
        menuHistorial.classList.remove("mostrar");
    }
});

// menu responsive
botonMenuPrincipal.addEventListener("click", evento => {
    evento.stopPropagation();
    accionesCabecera.classList.toggle("mostrar-menu");
    botonMenuPrincipal.setAttribute("aria-expanded", accionesCabecera.classList.contains("mostrar-menu"));
});

// Cerrar el menú principal si se hace clic fuera de él
document.addEventListener("click", evento => {
    if (!evento.target.closest(".encabezado")) {
        accionesCabecera.classList.remove("mostrar-menu");
        botonMenuPrincipal.setAttribute("aria-expanded", "false");
    }
});

// Incluir el cierre del menú principal al presionar la tecla Escape
document.addEventListener("keydown", evento => {
    if (evento.key === "Escape") {
        accionesCabecera.classList.remove("mostrar-menu");
        botonMenuPrincipal.setAttribute("aria-expanded", "false");
    }
});

// carga las tareas y solicitudes desde el servidor al iniciar la aplicación
cargarTareasDesdeServidor();
cargarSolicitudes();
