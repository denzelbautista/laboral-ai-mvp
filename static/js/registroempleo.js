document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-publicar-empleo");

    form.addEventListener("submit", async function (event) {
        event.preventDefault(); // Evita el comportamiento predeterminado del formulario

        // Obtener los datos del formulario
        const empleoDatos = {
            nombre_empleo: document.getElementById("nombre_empleo").value,
            fecha_final: document.getElementById("fecha_final").value,
            ubicacion: document.getElementById("ubicacion").value,
            salario_min: document.getElementById("salario_min").value,
            vacantes: document.getElementById("vacantes").value,
            descripcion: document.getElementById("descripcion").value
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
