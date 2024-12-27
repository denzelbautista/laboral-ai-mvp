document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const empleoId = urlParams.get('id');

    const jobDetailsContainer = document.getElementById('job-details');
    const jobTitle = document.getElementById('job-title');

    // Fetch empleo details from API
    fetch(`/empleos/${empleoId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const empleo = data.empleo;

                // Actualizar el título del empleo
                jobTitle.textContent = empleo.nombre;

                // Crear contenido dinámico para los detalles del empleo
                jobDetailsContainer.innerHTML = `
                    <div class="col-lg-8">
                        <div class="general-description-job card shadow-sm">
                            <div class="card-body">
                                <button id="btn-copiar-{{ loop.index }}"
                                    class="btn btn-secondary btn-sm"
                                    data-job-name="${ empleo.nombre }"
                                        title="Copiar nombre del empleo"
                                    onclick="copiarAlPortapapeles('${ empleo.nombre }')">
                                    <i class="fas fa-copy"></i> Copiar nombre del empleo
                                </button>
                                <p><strong>Descripción:</strong> ${empleo.descripcion}</p>
                                <p><strong>Tipo de Contrato:</strong> ${empleo.tipo_contrato.replace(/_/g, ' ').split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ')}</p>
                                <p><strong>Modalidad:</strong> ${empleo.modalidad_asistencia.replace(/_/g, ' ').split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ')}</p>
                                <h5>Requisitos:</h5>
                                <p>${empleo.requisitos || "No especificados"}</p> <!-- Manejar como texto -->
                                <h5>Beneficios:</h5>
                                <p>${empleo.beneficios || "No especificados"}</p> <!-- Manejar como texto -->
                                <h5>Funciones:</h5>
                                <p>${empleo.funciones || "No especificadas"}</p> <!-- Manejar como texto -->
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-4">
                        <div class="general-description-job card shadow-sm">
                            <div class="card-body">
                                <p><i class="fas fa-map-marker-alt text-danger me-2"></i><strong>Ubicación:</strong> ${empleo.ubicacion || "No especificada"}</p>
                                <p><i class="fas fa-money-bill-wave text-success me-2"></i><strong>Salario:</strong> ${empleo.salario || "No especificado"}</p>
                                <p><i class="fas fa-users text-success me-2"></i><strong>Vacantes:</strong> ${empleo.vacantes || "No especificadas"}</p>
                                <p><i class="fas fa-calendar-alt text-warning me-2"></i><strong>Fecha de publicación:</strong> ${empleo.fecha_creacion || "No disponible"}</p>
                                <p><i class="fas fa-hourglass-end text-warning me-2"></i><strong>Fecha límite:</strong> ${empleo.fecha_final_postulacion || "No disponible"}</p>
                                <a href="https://forms.gle/7xBM9NnXNtJfxNTC6" target="_blank" class="btn btn-primary w-100">
                                    <i class="fas fa-paper-plane me-2"></i>Postular ahora
                                </a>
                            </div>
                        </div>
                    </div>
                    
                    <!-- exito -->
                    <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 11">
                        <div id="successToast" class="toast align-items-center text-white bg-success border-0" role="alert"
                             aria-live="assertive" aria-atomic="true">
                            <div class="d-flex">
                                <div class="toast-body" id="toastMessage">
                                    Operación exitosa
                                </div>
                                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"
                                        aria-label="Close"></button>
                            </div>
                        </div>
                    </div>

                    <!-- error -->
                    <div class="position-fixed bottom-0 end-0 p-3" style="z-index: 11">
                        <div id="errorToast" class="toast align-items-center text-white bg-danger border-0" role="alert"
                             aria-live="assertive" aria-atomic="true">
                            <div class="d-flex">
                                <div class="toast-body" id="errorToastMessage">
                                    Error en la operación
                                </div>
                                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"
                                        aria-label="Close"></button>
                            </div>
                        </div>
                    </div>
                `;
            } else {
                jobTitle.textContent = "Error al cargar el empleo";
                jobDetailsContainer.innerHTML = `<p>Error al cargar los detalles del empleo.</p>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            jobTitle.textContent = "Error al cargar el empleo";
            jobDetailsContainer.innerHTML = `<p>Error al cargar los detalles del empleo.</p>`;
        });
});
function copiarAlPortapapeles(texto) {
    const url = texto;
    console.log("klok")
    const tempInput = document.createElement('input');
    tempInput.style.position = 'absolute';
    tempInput.style.left = '-9999px';
    tempInput.value = url;
    document.body.appendChild(tempInput);

    try {
        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(url).then(() => {
                mostrarNotificacion(true);
            }).catch(() => {
                copiarConSeleccion();
            });
        } else {
            copiarConSeleccion();
        }
    } catch (err) {
        console.error('Error al copiar:', err);
        mostrarNotificacion(false);
    }

    function copiarConSeleccion() {
        tempInput.select();
        tempInput.setSelectionRange(0, 99999);

        try {
            document.execCommand('copy');
            mostrarNotificacion(true);
        } catch (err) {
            console.error('Error al copiar:', err);
            mostrarNotificacion(false);
        }
    }

    document.body.removeChild(tempInput);
}

function mostrarNotificacion(exito) {
    if (exito) {
        const toast = new bootstrap.Toast(document.getElementById('successToast'));
        document.getElementById('toastMessage').textContent = 'Nombre del empleo copiado al portapapeles';
        toast.show();
    } else {
        const toast = new bootstrap.Toast(document.getElementById('errorToast'));
        document.getElementById('errorToastMessage').textContent = 'Error al copiar el nombre del empleo';
        toast.show();
    }
}