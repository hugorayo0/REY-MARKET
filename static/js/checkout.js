function rellenarDireccion(calle, portal, piso, puerta, localidad, provincia, cp) {
    document.getElementById('calle_entrega').value = calle;
    document.getElementById('portal_entrega').value = portal;
    document.getElementById('piso_entrega').value = piso;
    document.getElementById('puerta_entrega').value = puerta;
    document.getElementById('localidad_entrega').value = localidad;
    document.getElementById('provincia_entrega').value = provincia;
    document.getElementById('cp_entrega').value = cp;
}