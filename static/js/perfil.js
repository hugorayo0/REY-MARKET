function togglePerfil() {
    document.getElementById('perfilMenu').classList.toggle('abierto');
}

document.addEventListener('click', function(e) {
    const wrapper = document.querySelector('.perfil-wrapper');
    if (wrapper && !wrapper.contains(e.target)) {
        document.getElementById('perfilMenu').classList.remove('abierto');
    }
});