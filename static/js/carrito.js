// ── Seleccionar dirección ──────────────────────────────
function seleccionarDireccion(btn) {
    document.querySelectorAll('.btn-direccion').forEach(b => b.classList.remove('seleccionada'));
    btn.classList.add('seleccionada');
    document.getElementById('id_direccion_seleccionada').value = btn.dataset.id;
}

window.addEventListener('DOMContentLoaded', () => {
    const dirs = document.querySelectorAll('.btn-direccion');
    if (dirs.length === 1) seleccionarDireccion(dirs[0]);
});

// ── Modal Editar ───────────────────────────────────────
function abrirEditar(event, btn) {
    event.stopPropagation();
    document.getElementById('edit-nombre').value    = btn.dataset.nombre;
    document.getElementById('edit-id').value        = btn.dataset.id;
    document.getElementById('edit-calle').value     = btn.dataset.calle;
    document.getElementById('edit-portal').value    = btn.dataset.portal;
    document.getElementById('edit-piso').value      = btn.dataset.piso;
    document.getElementById('edit-puerta').value    = btn.dataset.puerta;
    document.getElementById('edit-localidad').value = btn.dataset.localidad;
    document.getElementById('edit-provincia').value = btn.dataset.provincia;
    document.getElementById('edit-cp').value        = btn.dataset.cp;
    document.getElementById('modalEditar').classList.add('abierto');
}

function cerrarEditar() {
    document.getElementById('modalEditar').classList.remove('abierto');
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('modalEditar').addEventListener('click', function(e) {
        if (e.target === this) cerrarEditar();
    });

    document.getElementById('confirmEliminar').addEventListener('click', function(e) {
        if (e.target === this) cerrarConfirm();
    });
});

// ── Modal Eliminar ─────────────────────────────────────
let idAEliminar = null;

function abrirEliminar(event, id) {
    event.stopPropagation();
    idAEliminar = id;
    document.getElementById('confirmEliminar').classList.add('activo');
}

function cerrarConfirm() {
    document.getElementById('confirmEliminar').classList.remove('activo');
    idAEliminar = null;
}

function confirmarEliminar() {
    if (!idAEliminar) return;
    window.location.href = '/direccion/eliminar/' + idAEliminar;
}