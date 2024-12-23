document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-publicar-empleo");

    form.addEventListener("submit", async function (event) {
        event.preventDefault(); // Evita el comportamiento predeterminado del formulario

        // Obtener los datos del formulario
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
            // Enviar datos al servidor Flask
            const response = await fetch("/publicar-empleo", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(empleoDatos)
            });

            const result = await response.json();

            if (result.success) {
                alert("Empleo publicado con éxito.");
                form.reset();
            } else {
                alert("Error al publicar el empleo: " + result.message);
            }
        } catch (error) {
            console.error("Error al enviar los datos:", error);
            alert("Hubo un error al enviar el formulario.");
        }
    });
});
