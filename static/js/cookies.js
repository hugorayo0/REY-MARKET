if (!localStorage.getItem('cookies')) {
    // Mostrar si no ha aceptado las cookies
    document.getElementById('recuadro-cookies').style.display = 'flex';
}

document.getElementById('boton-aceptar').addEventListener('click', function() {
    // Guardar en el LocalStorage que ha aceptado las cookies
    localStorage.setItem('cookies', 'aceptadas');
    document.getElementById('recuadro-cookies').style.display = 'none';
});

document.getElementById('boton-rechazar').addEventListener('click', function() {
    // Guardar en el LocalStorage que ha rechazado
    localStorage.setItem('cookies', 'rechazadas');
    // Ocultar si ha aceptado las cookies
    document.getElementById('recuadro-cookies').style.display = 'none';
});