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
                    <style>
                        .general-description-job {
                            transition: transform 0.2s;
                            border: none;
                            margin-bottom: 2rem;
                        }

                        .general-description-job:hover {
                            transform: translateY(-5px);
                        }

                        .card {
                            border-radius: 15px;
                            border: 1px solid rgba(0,0,0,0.08);
                        }

                        .card-body {
                            padding: 2rem;
                        }
                        
                        .btn-postular {
                            border-radius: 30px;
                            padding: 1rem 2rem;
                            font-weight: 600;
                            text-transform: uppercase;
                            letter-spacing: 1px;
                            margin-top: 1rem;
                            transition: all 0.3s;
                        }

                        .btn-postular:hover {
                            transform: translateY(-2px);
                            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                        }

                        .section-title {
                            color: #2c3e50;
                            margin-bottom: 1.5rem;
                            padding-bottom: 0.5rem;
                            border-bottom: 2px solid #e9ecef;
                        }
                        .section-title2 {
                            margin-bottom: 1.5rem;
                            padding-bottom: 0.5rem;
                        }
                        .toast {
                            border-radius: 10px;
                        }

                                      
                    </style>
                    <div class="col-lg-8">
                        <div class="general-description-job card shadow-sm">
                            <div class="card-body position-relative">
                                <div style="display: flex; gap: 15px; flex-direction: row">
                                    <h4 class="section-title">Descripción del Puesto</h4>
                                    <button id="btn-copiar-${empleo.id}"
                                    class="btn btn-secondary btn-sm section-title2"
                                    data-job-name="${empleo.nombre}"
                                    title="Copiar nombre del empleo"
                                    onclick="copiarAlPortapapeles('${empleo.nombre}')">
                                        <i class="fas fa-copy"></i> Copiar nombre
                                    </button>
                                </div>
                                
                                
                                
                                <p class="lead mb-4">${empleo.descripcion}</p>
                                
                                <div class="info-section mb-4">
                                    <div class="row">
                                        <div class="col-md-6">
                                            <p class="mb-3"><strong>Tipo de Contrato:</strong><br>
                                            ${empleo.tipo_contrato.replace(/_/g, ' ').split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ')}</p>
                                        </div>
                                        <div class="col-md-6">
                                            <p class="mb-3"><strong>Modalidad:</strong><br>
                                            ${empleo.modalidad_asistencia.replace(/_/g, ' ').split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ')}</p>
                                        </div>
                                    </div>
                                </div>

                                <h4 class="section-title">Requisitos</h4>
                                <div class="mb-4">
                                    ${empleo.requisitos || "No especificados"}
                                </div>

                                <h4 class="section-title">Beneficios</h4>
                                <div class="mb-4">
                                    ${empleo.beneficios || "No especificados"}
                                </div>

                                <h4 class="section-title">Funciones</h4>
                                <div class="mb-4">
                                    ${empleo.funciones || "No especificadas"}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-lg-4">
                        <div class="general-description-job card shadow-sm">
                            <div class="card-body">
                                <p id="empresa-nombre"><strong>Empresa:</strong> Cargando...</p>
                                <p><i class="fas fa-map-marker-alt text-danger me-2"></i><strong>Ubicación:</strong> ${empleo.ubicacion || "No especificada"}</p>
                                <p><i class="fas fa-money-bill-wave text-success me-2"></i><strong>Salario:</strong> ${empleo.salario || "No especificado"}</p>
                                <p><i class="fas fa-users text-success me-2"></i><strong>Vacantes:</strong> ${empleo.vacantes || "No especificadas"}</p>
                                <p><i class="fas fa-calendar-alt text-warning me-2"></i><strong>Fecha de publicación:</strong> ${empleo.fecha_creacion || "No disponible"}</p>
                                <p><i class="fas fa-hourglass-end text-warning me-2"></i><strong>Fecha límite:</strong> ${empleo.fecha_final_postulacion || "No disponible"}</p>
                                <a href="https://forms.gle/7xBM9NnXNtJfxNTC6" target="_blank" class="btn btn-primary w-100 btn-postular">
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

                // Hacer otra solicitud para obtener el nombre de la empresa
                fetch(`/empleo/empresa/${empleo.empresa_id}`)
                    .then(response => response.json())
                    .then(empresaData => {
                        if (empresaData.success) {
                            // Actualizar el nombre de la empresa
                            const empresaNombreElement = document.getElementById('empresa-nombre');
                            empresaNombreElement.innerHTML = `<strong>Empresa:</strong> ${empresaData.empresa}`;
                        } else {
                            console.error('Error al cargar el nombre de la empresa:', empresaData.message);
                            document.getElementById('empresa-nombre').textContent = "Empresa no encontrada";
                        }
                    })
                    .catch(error => {
                        console.error('Error al cargar el nombre de la empresa:', error);
                        document.getElementById('empresa-nombre').textContent = "Error al cargar la empresa";
                    });
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
