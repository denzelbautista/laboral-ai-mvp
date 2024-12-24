document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-publicar-empleo");
    const successModal = new bootstrap.Modal(document.getElementById('successModal'));
    const errorModal = new bootstrap.Modal(document.getElementById('errorModal'));

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const empleoDatos = {
            nombre: document.getElementById("nombre_empleo").value,
            fecha_final_postulacion: document.getElementById("fecha_final_postulacion").value,
            ubicacion: document.getElementById("ubicacion").value,
            salario: document.getElementById("salario").value,
            vacantes: document.getElementById("vacantes").value,
            descripcion: document.getElementById("descripcion").value,
            funciones: document.getElementById("funciones").value,
            requisitos: document.getElementById("requisitos").value,
            beneficios: document.getElementById("beneficios").value,
            tipo_contrato: document.getElementById("tipo_contrato").value,
            modalidad_asistencia: document.getElementById("modalidad_asistencia").value,
        };

        try {
            const response = await fetch("/publicar-empleo", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(empleoDatos)
            });

            const result = await response.json();

            if (result.success) {
                successModal.show();
                form.reset();
            } else {
                document.getElementById('errorMessage').textContent = "Error al publicar el empleo: " + result.message;
                errorModal.show();
            }
        } catch (error) {
            console.error("Error al enviar los datos:", error);
            document.getElementById('errorMessage').textContent = "Hubo un error al enviar el formulario.";
            errorModal.show();
        }
    });
});
