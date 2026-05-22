function filtrarCategoria(btn, categoria) {
    document.querySelectorAll('.categoria-btn').forEach(b => b.classList.remove('activo'));
    btn.classList.add('activo');
    document.querySelectorAll('.producto').forEach(prod => {
        prod.style.display = (categoria === 'todos' || prod.dataset.categoria === categoria) ? '' : 'none';
    });
}

function AgregaralCarrito(btn, id, nombre, precio) {
    btn.textContent = '✓ Añadido';
    btn.disabled = true;
    btn.style.background = '#1b5e20';
    setTimeout(() => {
        btn.textContent = 'Añadir al carrito';
        btn.style.background = '';
        btn.disabled = false;
    }, 1500);

    const carritoIcon = document.getElementById('carrito-icon');
    const btnRect = btn.getBoundingClientRect();
    const carritoRect = carritoIcon.getBoundingClientRect();
    const burbuja = document.createElement('div');
    burbuja.className = 'burbuja-fly';
    burbuja.textContent = '🛒';
    burbuja.style.left = (btnRect.left + btnRect.width / 2) + 'px';
    burbuja.style.top = (btnRect.top + window.scrollY) + 'px';
    burbuja.style.setProperty('--dx', (carritoRect.left - btnRect.left) + 'px');
    burbuja.style.setProperty('--dy', (carritoRect.top - btnRect.top - window.scrollY) + 'px');
    document.body.appendChild(burbuja);
    burbuja.offsetWidth;
    burbuja.classList.add('volando');
    burbuja.addEventListener('animationend', () => {
        burbuja.remove();
        carritoIcon.classList.add('shake');
        setTimeout(() => carritoIcon.classList.remove('shake'), 500);
    });

    fetch('/carrito/agregar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, nombre, precio })
    })
    .then(r => r.json())
    .then(data => {
        const badge = document.getElementById('carrito-badge');
        badge.textContent = data.total_items;
        badge.style.display = data.total_items > 0 ? 'flex' : 'none';
    });
}

function abrirModal(id, nombre, precio, imagen, unidad, categoria) {
    document.getElementById('edit-nombre').value = nombre;
    document.getElementById('edit-precio').value = precio;
    document.getElementById('edit-imagen').value = imagen;
    document.getElementById('edit-unidad').value = unidad;
    document.getElementById('edit-categoria').value = categoria;
    document.getElementById('formEditar').action = '/admin/producto/editar/' + id;
    document.getElementById('modalEditar').classList.add('abierto');
}

function cerrarModal() {
    document.getElementById('modalEditar').classList.remove('abierto');
}

document.getElementById('modalEditar')?.addEventListener('click', function(e) {
    if (e.target === this) cerrarModal();
});
