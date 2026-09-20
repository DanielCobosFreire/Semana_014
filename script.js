// script.js
// CSi - CoFre Sistemas Informáticos
// Semana 7: contenido dinámico renderizado desde arreglos/objetos,
// estructura pensada para una futura migración a plantillas de Flask.
// Semana 8: se conserva toda la lógica anterior (validaciones y renderizado
// dinámico) y se incorporan dos componentes Bootstrap controlados desde JS:
//   - Spinner: simula un proceso de registro antes de insertar la solicitud.
//   - Modal: reemplaza la eliminación directa por una confirmación explícita.
//
// Cada función de "render" de este archivo simula lo que en Flask sería
// un {% for %} recorriendo datos que en el futuro vendrán de una base
// de datos, en lugar de un arreglo estático en JavaScript.

document.addEventListener('DOMContentLoaded', function () {

  /* =====================================================================
     BLOQUE 1: SERVICIOS (dato -> array de objetos)
     Equivalente futuro en Flask: servicios = Servicio.query.all()
     ===================================================================== */

  const servicios = [
    {
      icono: '💻',
      titulo: 'Desarrollo Web',
      descripcion: 'Sitios web modernos, responsivos y optimizados.'
    },
    {
      icono: '🧭',
      titulo: 'Consultoría IT',
      descripcion: 'Asesoramiento tecnológico para empresas.'
    },
    {
      icono: '🛠️',
      titulo: 'Soporte Técnico',
      descripcion: 'Mantenimiento y administración de infraestructura TI.'
    }
  ];

  const contenedorServicios = document.getElementById('contenedorServicios');

  // Renderiza las tarjetas de servicio a partir del arreglo "servicios".
  // Estructura repetitiva (forEach) + condicional de estado vacío.
  function renderServicios() {
    contenedorServicios.innerHTML = '';

    if (servicios.length === 0) {
      contenedorServicios.innerHTML =
        '<p class="text-center text-light">No hay servicios disponibles por el momento.</p>';
      return;
    }

    servicios.forEach(function (servicio) {
      const columna = document.createElement('div');
      columna.className = 'col-md-4 mb-4';

      columna.innerHTML = `
        <div class="card h-100 shadow">
          <div class="card-body text-dark text-center">
            <div class="icono-servicio">${servicio.icono}</div>
            <h5 class="card-title">${servicio.titulo}</h5>
            <p class="card-text">${servicio.descripcion}</p>
          </div>
        </div>
      `;

      contenedorServicios.appendChild(columna);
    });
  }

  renderServicios();


  /* =====================================================================
     BLOQUE 2: SOLICITUDES (dato -> array de objetos, con registro desde
     formulario)
     Equivalente futuro en Flask: solicitudes = Solicitud.query.all()
     ===================================================================== */

  // Referencias a elementos del DOM
  const formSolicitud = document.getElementById('formSolicitud');
  const nombreCliente = document.getElementById('nombreCliente');
  const categoriaServicio = document.getElementById('categoriaServicio');
  const descripcionServicio = document.getElementById('descripcionServicio');
  const mensajeValidacion = document.getElementById('mensajeValidacion');
  const listaSolicitudes = document.getElementById('listaSolicitudes');
  const contadorSolicitudes = document.getElementById('contadorSolicitudes');

  // Semana 8: referencias al botón/spinner de registro y al modal de confirmación
  const btnRegistrar = document.getElementById('btnRegistrar');
  const spinnerRegistrar = document.getElementById('spinnerRegistrar');
  const textoBtnRegistrar = document.getElementById('textoBtnRegistrar');

  const elementoModalEliminar = document.getElementById('modalConfirmarEliminar');
  const modalConfirmarEliminar = new bootstrap.Modal(elementoModalEliminar);
  const modalNombreSolicitud = document.getElementById('modalNombreSolicitud');
  const modalCategoriaSolicitud = document.getElementById('modalCategoriaSolicitud');
  const modalDescripcionSolicitud = document.getElementById('modalDescripcionSolicitud');
  const btnConfirmarEliminar = document.getElementById('btnConfirmarEliminar');

  // Arreglo de objetos: representa los datos de las solicitudes registradas.
  // Cada solicitud es un objeto con id, nombre, categoría y descripción.
  let solicitudes = [];
  let siguienteId = 1;

  // Guarda temporalmente el id de la solicitud que el modal está por eliminar
  let idPendienteEliminar = null;

  // Función para mostrar mensajes de validación al usuario (Semana 6, sin cambios)
  function mostrarMensaje(texto, tipo) {
    mensajeValidacion.textContent = texto;
    mensajeValidacion.classList.remove('d-none', 'alert-danger', 'alert-success');
    mensajeValidacion.classList.add(tipo === 'error' ? 'alert-danger' : 'alert-success');

    // El mensaje desaparece automáticamente después de unos segundos
    setTimeout(function () {
      mensajeValidacion.classList.add('d-none');
    }, 3000);
  }

  // Actualiza el contador de registros en pantalla a partir del arreglo
  function actualizarContador() {
    contadorSolicitudes.textContent = solicitudes.length;
  }

  // Renderiza la lista completa de solicitudes a partir del arreglo "solicitudes".
  // Estructura repetitiva (forEach) + condicional de estado (lista vacía / con datos).
  function renderSolicitudes() {
    listaSolicitudes.innerHTML = '';
    actualizarContador();

    // Condición según el estado de los datos
    if (solicitudes.length === 0) {
      const vacio = document.createElement('li');
      vacio.className = 'list-group-item text-center text-muted';
      vacio.textContent = 'Aún no hay solicitudes registradas.';
      listaSolicitudes.appendChild(vacio);
      return;
    }

    // Estructura repetitiva: recorre el arreglo y genera un <li> por cada solicitud
    solicitudes.forEach(function (solicitud) {

      const item = document.createElement('li');
      item.className = 'list-group-item d-flex justify-content-between align-items-start flex-wrap';

      const contenido = document.createElement('div');
      contenido.className = 'me-auto';

      const tituloNombre = document.createElement('strong');
      tituloNombre.textContent = solicitud.nombre;

      const badgeCategoria = document.createElement('span');
      badgeCategoria.className = 'badge bg-secondary ms-2';
      badgeCategoria.textContent = solicitud.categoria;

      const textoDescripcion = document.createElement('p');
      textoDescripcion.className = 'mb-0 text-muted';
      textoDescripcion.textContent = solicitud.descripcion;

      contenido.appendChild(tituloNombre);
      contenido.appendChild(badgeCategoria);
      contenido.appendChild(textoDescripcion);

      // Botón para eliminar la solicitud
      const botonEliminar = document.createElement('button');
      botonEliminar.className = 'btn btn-outline-danger btn-sm';
      botonEliminar.textContent = 'Eliminar';

      // Semana 8: en lugar de eliminar directo, se abre el modal Bootstrap
      // de confirmación con los datos de la solicitud seleccionada.
      botonEliminar.addEventListener('click', function () {
        idPendienteEliminar = solicitud.id;
        modalNombreSolicitud.textContent = solicitud.nombre;
        modalCategoriaSolicitud.textContent = solicitud.categoria;
        modalDescripcionSolicitud.textContent = solicitud.descripcion;
        modalConfirmarEliminar.show();
      });

      item.appendChild(contenido);
      item.appendChild(botonEliminar);
      listaSolicitudes.appendChild(item);
    });
  }

  // Semana 8: al confirmar en el modal, se elimina la solicitud pendiente,
  // se cierra el modal y se muestra el mensaje de éxito.
  btnConfirmarEliminar.addEventListener('click', function () {
    if (idPendienteEliminar === null) return;

    solicitudes = solicitudes.filter(function (s) {
      return s.id !== idPendienteEliminar;
    });

    renderSolicitudes();
    modalConfirmarEliminar.hide();
    mostrarMensaje('Solicitud eliminada correctamente.', 'success');
    idPendienteEliminar = null;
  });

  // Agrega una nueva solicitud al arreglo de datos y vuelve a renderizar la lista
  function crearSolicitud(nombre, categoria, descripcion) {
    solicitudes.push({
      id: siguienteId++,
      nombre: nombre,
      categoria: categoria,
      descripcion: descripcion
    });

    renderSolicitudes();
  }

  // Captura del evento submit del formulario (validaciones de la Semana 6, sin cambios)
  formSolicitud.addEventListener('submit', function (evento) {

    // Evita que la página se recargue
    evento.preventDefault();

    const nombre = nombreCliente.value.trim();
    const categoria = categoriaServicio.value;
    const descripcion = descripcionServicio.value.trim();

    // Validación de campos vacíos
    if (nombre === '' || categoria === '' || descripcion === '') {
      mostrarMensaje('Por favor complete todos los campos antes de registrar la solicitud.', 'error');
      return;
    }

    // Semana 8: se simula un proceso de registro (ej. envío a un futuro backend
    // Flask) mostrando un spinner Bootstrap y deshabilitando el botón mientras dura.
    btnRegistrar.disabled = true;
    spinnerRegistrar.classList.remove('d-none');
    textoBtnRegistrar.textContent = 'Registrando...';

    setTimeout(function () {
      // Una vez "terminado" el proceso simulado, se registra en el arreglo
      crearSolicitud(nombre, categoria, descripcion);
      mostrarMensaje('Solicitud registrada exitosamente.', 'success');

      // Limpiar el formulario para un nuevo registro
      formSolicitud.reset();
      nombreCliente.focus();

      // Restaurar el botón a su estado normal
      btnRegistrar.disabled = false;
      spinnerRegistrar.classList.add('d-none');
      textoBtnRegistrar.textContent = 'Registrar Solicitud';
    }, 900);
  });

  // Render inicial: muestra el mensaje de estado vacío al cargar la página
  renderSolicitudes();

});
