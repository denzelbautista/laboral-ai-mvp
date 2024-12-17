document.getElementById('register').addEventListener('submit', async (event) => {
    event.preventDefault();

    const empresaData = {
        nombre: document.getElementById('nombre').value,
        razon_social: document.getElementById('razon_social').value,
        RUC: document.getElementById('RUC').value,
        correo: document.getElementById('correo').value,
        numero_contacto: document.getElementById('numero_contacto').value,
        contrasena: document.getElementById('contrasena').value
    };

    try {
        const response = await fetch('/api/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(empresaData)
        });

        const result = await response.json();

        if (response.ok && result.success) {
            window.location.href = '/dashboard'; // Redireccionar al dashboard
        } else {
            alert(result.message || 'Error en el registro.');
        }
    } catch (error) {
        console.error('Error al enviar los datos:', error);
    }
});

