/*
    LISTADO DE TAREAS
    Este archivo se encarga de:
    Mostrar las tareas.
    Buscar tareas.
    Dividir las tareas en páginas.
    Crear los botones de paginación.

    
*/


// CONFIGURACIÓN DE LA PAGINACIÓN
let tareas = [];

const tareasPorPagina = 5;

let paginaActual = 1;

// ELEMENTOS DEL HTML
const listaTareas = document.getElementById("listaTareas");
const paginacion = document.getElementById("paginacion");
const sinResultados = document.getElementById("sinResultados");

const inputBuscar = document.getElementById("buscarTarea");
const botonBuscar = document.getElementById("botonBuscar");


// Esta variable contiene las tareas que se están mostrando.
// Al principio contiene todas las tareas.
let tareasFiltradas = tareas;

// MOSTRAR TAREAS
function mostrarTareas() {
    // Limpiamos el contenido anterior.
    listaTareas.innerHTML = "";

    // Calculamos desde qué posición y hasta qué posición
    // debemos mostrar las tareas de la página actual.
    const inicio = (paginaActual - 1) * tareasPorPagina;
    const fin = inicio + tareasPorPagina;

    const tareasDeLaPagina = tareasFiltradas.slice(inicio, fin);


    // Si no encontramos tareas mostramos un mensaje.
    if (tareasDeLaPagina.length === 0) {

        sinResultados.style.display = "block";

        return;
    }

    sinResultados.style.display = "none";


    // Recorremos las tareas que corresponden a esta página.
    tareasDeLaPagina.forEach(function(tarea) {

        const elemento = document.createElement("article");

        elemento.classList.add("tarea");


        // Convertimos el estado a una clase CSS.
        const claseEstado = obtenerClaseEstado(tarea.estado);


        elemento.innerHTML = `
            <div class="tarea-info">
                <h2>${tarea.titulo}</h2>
                <p><strong>ID:</strong> ${tarea.id} &nbsp;|&nbsp; <strong>Prioridad:</strong> ${tarea.prioridad} &nbsp;|&nbsp; <strong>Responsable:</strong> ${tarea.responsable || "Sin asignar"}</p>
            </div>

            <span class="estado ${claseEstado}">
                ${tarea.estado}
            </span>
        `;


        listaTareas.appendChild(elemento);
    });
}

// OBTENER CLASE DEL ESTADO
function obtenerClaseEstado(estado) {
    if (!estado) return "pendiente";
    const est = estado.toString().toLowerCase();
    if (est === "pendiente") return "pendiente";
    if (est === "en proceso" || est === "en progreso") return "en-proceso";
    if (est === "completada") return "completada";
    return "pendiente";
}

// CREAR PAGINACIÓN
function crearPaginacion() {

    paginacion.innerHTML = "";

    const cantidadPaginas = Math.ceil(
        tareasFiltradas.length / tareasPorPagina
    );


    // Si hay una sola página no hace falta mostrar botones.
    if (cantidadPaginas <= 1) {
        return;
    }


    // Creamos un botón por cada página.
    for (let numero = 1; numero <= cantidadPaginas; numero++) {

        const boton = document.createElement("button");

        boton.classList.add("boton-pagina");

        boton.textContent = numero;


        // Marcamos la página actual.
        if (numero === paginaActual) {
            boton.classList.add("activa");
        }


        // Cuando hacemos clic cambiamos de página.
        boton.addEventListener("click", function() {

            paginaActual = numero;

            mostrarTareas();
            crearPaginacion();
        });


        paginacion.appendChild(boton);
    }
}

// BUSCAR TAREAS
function buscarTareas() {

    const texto = inputBuscar.value
        .trim()
        .toLowerCase();


    // Si el buscador está vacío mostramos todas las tareas.
    if (texto === "") {

        tareasFiltradas = tareas;

    } else {

        // filter() devuelve solamente las tareas que coinciden
        // con el texto escrito por el usuario.
        tareasFiltradas = tareas.filter(function(tarea) {
            const titulo = (tarea.titulo || "").toLowerCase();
            const id = (tarea.id || "").toLowerCase();
            const estado = (tarea.estado || "").toLowerCase();
            const responsable = (tarea.responsable || "").toLowerCase();
            return titulo.includes(texto) || id.includes(texto) ||
                   estado.includes(texto) || responsable.includes(texto);
        });
    }


    // Volvemos a la primera página después de buscar.
    paginaActual = 1;

    mostrarTareas();
    crearPaginacion();
}

// CONTROL DE LA VENTANA PARA NUEVA TAREA
const ventanaTarea = document.getElementById("ventanaTarea");
const botonNuevaTarea = document.getElementById("botonNuevaTarea");
const botonCancelarVentana = document.getElementById("botonCancelarVentana");
const formularioTarea = document.getElementById("formularioTarea");
const inputDescripcion = document.getElementById("inputDescripcion");
const inputResponsable = document.getElementById("inputResponsable");
const inputPrioridad = document.getElementById("inputPrioridad");
const botonVerHistorial = document.getElementById("botonHistorial");

// Abrir la ventana cuando hacen clic en "Nueva Tarea".
botonNuevaTarea.addEventListener("click", function() {
    ventanaTarea.style.display = "flex";
    inputDescripcion.focus();
});

botonVerHistorial.addEventListener("click", function() {
});

// Cerrar la ventana cuando hacen clic en "Cancelar".
botonCancelarVentana.addEventListener("click", function() {
    formularioTarea.reset();
    ventanaTarea.style.display = "none";
});

// Cerrar la ventana si hacen clic en la parte oscura de afuera.
ventanaTarea.addEventListener("click", function(evento) {
    if (evento.target === ventanaTarea) {
        formularioTarea.reset();
        ventanaTarea.style.display = "none";
    }
});

// También permite cerrar la ventana con Escape.
document.addEventListener("keydown", function(evento) {
    if (evento.key === "Escape" && ventanaTarea.style.display === "flex") {
        formularioTarea.reset();
        ventanaTarea.style.display = "none";
    }
});


// COMUNICACIÓN CON PYTHON (FETCH)

// Función para pedirle las tareas a Python (GET).
function cargarTareasDesdeServidor() {
    fetch("http://localhost:8000/api/tareas")
        .then(respuesta => {
            if (!respuesta.ok) {
                throw new Error("No se pudieron cargar las tareas.");
            }
            return respuesta.json();
        })
        .then(datosDesdePython => {
            console.log("Tareas recibidas de Python:", datosDesdePython);

            // Adaptamos el formato de Python para tu función mostrarTareas.
            tareas = datosDesdePython.map(t => ({
                id: t.id_tarea,
                titulo: t.descripcion,
                responsable: t.responsable || "",
                prioridad: t.prioridad || 2,
                estado: t.estado || "Pendiente"
            }));

            tareasFiltradas = tareas;
            paginaActual = 1;
            mostrarTareas();
            crearPaginacion();
        })
        .catch(error => {
            console.warn("Servidor Python desconectado:", error);
        });
}

// Evento al enviar el formulario (POST).
formularioTarea.addEventListener("submit", function(evento) {
    evento.preventDefault();

    const descripcion = inputDescripcion.value.trim();
    const responsable = inputResponsable.value.trim();
    const prioridad = inputPrioridad.value.trim();

    if (descripcion === "" || responsable === "" || prioridad === "") {
        return;
    }

    // Enviamos la tarea a Python.
    fetch("http://localhost:8000/api/tareas", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            descripcion: descripcion,
            responsable: responsable,
            prioridad: prioridad
        })
    })
    .then(respuesta => {
        if (!respuesta.ok) {
            return respuesta.json().then(datos => {
                throw new Error(datos.mensaje || "No se pudo guardar la tarea.");
            });
        }

        return respuesta.json();
    })
    .then(datos => {
        console.log("Respuesta de Python:", datos.mensaje);

        // Limpiamos los campos y cerramos la ventana.
        formularioTarea.reset();
        ventanaTarea.style.display = "none";

        // Volvemos a traer la lista actualizada desde Python.
        cargarTareasDesdeServidor();
    })
    .catch(error => {
        console.error("Error al guardar en Python:", error);
        alert("No se pudo guardar la tarea. Verificá que el servidor Python esté iniciado.");
    });
});

// INICIO DE LA APLICACIÓN

// Buscar al presionar el botón o presionar Enter
botonBuscar.addEventListener("click", buscarTareas);
inputBuscar.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        buscarTareas();
    }
});
// Al cargar la página, traemos las tareas directamente de Python
cargarTareasDesdeServidor();
