function seleccionarDireccion(el) {
    document.querySelectorAll('.btn-direccion').forEach(d => d.classList.remove('seleccionada'));
    el.classList.add('seleccionada');
    document.getElementById('id_direccion_seleccionada').value = el.dataset.id;
}