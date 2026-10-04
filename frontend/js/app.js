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
const inputResponsable = document.getElementById("inputResponsable");
const inputPrioridad = document.getElementById("inputPrioridad");
const inputComplejidad = document.getElementById("inputComplejidad");

const ventanaSolicitud = document.getElementById("ventanaSolicitud");
const formularioSolicitud = document.getElementById("formularioSolicitud");
const inputSolicitud = document.getElementById("inputSolicitud");
const inputPrioridadSolicitud = document.getElementById("inputPrioridadSolicitud");
const botonMesaAyuda = document.getElementById("botonMesaAyuda");
const menuMesaAyuda = document.getElementById("menuMesaAyuda");

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
                <p><strong>ID:</strong> ${tarea.id} | <strong>Prioridad:</strong> ${obtenerTextoPrioridad(tarea.prioridad)} | <strong>Complejidad:</strong> ${tarea.complejidad} | <strong>Responsable:</strong> ${tarea.responsable || "Sin asignar"}</p>
            </div>
            <div class="tarea-acciones">
                <span class="estado ${obtenerClaseEstado(tarea.estado)}">${tarea.estado}</span>
                <button class="boton-completar" data-id="${tarea.id}">Completar</button>
                <button class="boton-eliminar" data-id="${tarea.id}">Eliminar</button>
            </div>
        `;
        listaTareas.appendChild(elemento);
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
        (tarea.estado || "").toLowerCase().includes(texto) ||
        (tarea.responsable || "").toLowerCase().includes(texto)
    );
    paginaActual = 1;
    mostrarTareas();
    crearPaginacion();
}

// carga las tareas desde el servidor y actualiza la lista de tareas mostradas

function cargarTareasDesdeServidor() {
    fetch("http://localhost:8000/api/tareas")
        .then(respuesta => respuesta.json())
        .then(datos => {
            tareas = datos.map(t => ({
                id: t.id_tarea,
                titulo: t.descripcion,
                responsable: t.responsable || "",
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
            responsable: inputResponsable.value.trim(),
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

// envía una solicitud al servidor para deshacer la última acción y recarga la lista de tareas
document.getElementById("botonDeshacer").addEventListener("click", () => {
    fetch("http://localhost:8000/api/tareas/deshacer", { method: "POST" })
        .then(r => r.json().then(datos => ({ ok: r.ok, datos })))
        .then(({ ok, datos }) => {
            if (!ok) throw new Error(datos.mensaje);
            cargarTareasDesdeServidor();
        })
        .catch(error => alert(error.message));
});

botonMesaAyuda.addEventListener("click", evento => {
    evento.stopPropagation();
    menuMesaAyuda.classList.toggle("mostrar");
});

document.addEventListener("click", evento => {
    if (!evento.target.closest(".desplegable-ayuda")) {
        menuMesaAyuda.classList.remove("mostrar");
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
// envía una solicitud al servidor para atender la solicitud más antigua y recarga la lista de solicitudes
document.getElementById("botonAtenderSolicitud").addEventListener("click", () => {
    menuMesaAyuda.classList.remove("mostrar");
    fetch("http://localhost:8000/api/solicitudes/atender", { method: "POST" })
        .then(r => r.json().then(datos => ({ ok: r.ok, datos })))
        .then(({ ok, datos }) => {
            if (!ok) throw new Error(datos.mensaje);
            alert("Solicitud atendida: " + datos.descripcion);
            cargarSolicitudes();
        })
        .catch(error => alert(error.message));
});
// carga las solicitudes desde el servidor y actualiza la lista de solicitudes mostradas =)
function cargarSolicitudes() {
    fetch("http://localhost:8000/api/solicitudes")
        .then(r => r.json())
        .then(solicitudes => {
            const contenedor = document.getElementById("listaSolicitudes");
            contenedor.innerHTML = solicitudes.length ? solicitudes.map(s =>
                `<div class="item-extra"><strong>Solicitud ${s.id_solicitud}</strong> - ${s.descripcion} <span>${s.estado}</span></div>`
            ).join("") : "<p>No hay solicitudes pendientes.</p>";
        });
}
// carga la complejidad de las tareas desde el servidor y actualiza la lista de complejidad mostradas
document.getElementById("botonComplejidad").addEventListener("click", () => {
    fetch("http://localhost:8000/api/complejidad")
        .then(r => r.json())
        .then(lista => {
            const contenedor = document.getElementById("listaComplejidad");
            contenedor.innerHTML = lista.length ? lista.map(t =>
                `<div class="item-extra"><strong>${t.id_tarea}</strong> - ${t.descripcion} <span>Complejidad: ${t.complejidad}</span></div>`
            ).join("") : "<p>No hay tareas para mostrar.</p>";
        });
});

botonBuscar.addEventListener("click", buscarTareas);
inputBuscar.addEventListener("keydown", evento => {
    if (evento.key === "Enter") buscarTareas();
});

document.addEventListener("keydown", evento => {
    if (evento.key === "Escape") {
        ventanaTarea.style.display = "none";
        ventanaSolicitud.style.display = "none";
        menuMesaAyuda.classList.remove("mostrar");
    }
});
// carga las tareas y solicitudes desde el servidor al iniciar la aplicación
cargarTareasDesdeServidor();
cargarSolicitudes();
