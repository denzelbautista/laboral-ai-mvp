document.getElementById('loginForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const correo = document.getElementById('correo').value;
    const contrasena = document.getElementById('contrasena').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ correo, contrasena })
        });

        const result = await response.json();

        if (response.ok && result.success) {
            window.location.href = '/dashboard'; // Redireccionar
        } else {
            alert(result.message || 'Error al iniciar sesión.');
        }
    } catch (error) {
        console.error('Error al iniciar sesión:', error);
        alert('Hubo un problema al iniciar sesión. Intenta de nuevo.');
    }
});
