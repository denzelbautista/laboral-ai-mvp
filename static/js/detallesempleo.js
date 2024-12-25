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
                                <p><strong>Descripción:</strong> ${empleo.descripcion}</p>
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
