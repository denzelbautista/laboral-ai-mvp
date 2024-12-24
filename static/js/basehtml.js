document.addEventListener("DOMContentLoaded", () => {
    const logoutButton = document.getElementById("logoutButton");

    logoutButton.addEventListener("click", async () => {
        try {
            // Realizar la solicitud al endpoint de logout
            const response = await fetch('/logout', {
                method: 'GET', // Cambiar a GET según tu ruta
            });

            if (response.ok) {
                // Logout exitoso, redirigir al login
                window.location.href = '/login';
            } else {
                // Manejar errores en caso de que el logout falle
                const errorData = await response.json();
                console.error("Error al cerrar sesión:", errorData.message || "Error desconocido");
                alert("Hubo un problema al cerrar sesión. Por favor, intenta de nuevo.");
            }
        } catch (error) {
            alert("Ocurrió un error al cerrar sesión. Verifica tu conexión y vuelve a intentarlo.");
        }
    });
});
