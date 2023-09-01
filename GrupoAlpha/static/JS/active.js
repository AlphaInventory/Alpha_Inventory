var registros = document.getElementById('registros');
var procesos = document.getElementById('procesos');
var movimientos = document.getElementById('movimientos');
var listados = document.getElementById('listados');
var respaldos = document.getElementById('respaldos');
var configuraciones = document.getElementById('configuraciones');

document.getElementById('registros').addEventListener("click", function() {
    if (procesos.classList.contains("activado")) {
        procesos.classList.remove("activado")
    }

    else if (movimientos.classList.contains("activado")) {
        movimientos.classList.remove("activado")
    }

    else if (listados.classList.contains("activado")) {
        listados.classList.remove("activado")
    }

    else if (respaldos.classList.contains("activado")) {
        respaldos.classList.remove("activado")
    }

    else if (configuraciones.classList.contains("activado")) {
        configuraciones.classList.remove("activado")
    }

    if (!registros.classList.contains("activado")) {
        registros.classList.toggle("activado")
    }
});

document.getElementById('procesos').addEventListener("click", function () {

    if (registros.classList.contains("activado")) {
        registros.classList.remove("activado")
    }

    else if (movimientos.classList.contains("activado")) {
        movimientos.classList.remove("activado")
    }

    else if (listados.classList.contains("activado")) {
        listados.classList.remove("activado")
    }

    else if (respaldos.classList.contains("activado")) {
        respaldos.classList.remove("activado")
    }

    else if (configuraciones.classList.contains("activado")) {
        configuraciones.classList.remove("activado")
    }

    if (!procesos.classList.contains("activado")) {
        procesos.classList.toggle("activado")
    }
});

document.getElementById('movimientos').addEventListener("click", function () {

    if (registros.classList.contains("activado")) {
        registros.classList.remove("activado")
    }

    else if (procesos.classList.contains("activado")) {
        procesos.classList.remove("activado")
    }

    else if (listados.classList.contains("activado")) {
        listados.classList.remove("activado")
    }

    else if (respaldos.classList.contains("activado")) {
        respaldos.classList.remove("activado")
    }

    else if (configuraciones.classList.contains("activado")) {
        configuraciones.classList.remove("activado")
    }

    if (!movimientos.classList.contains("activado")) {
        movimientos.classList.toggle("activado")
    }
});

document.getElementById('listados').addEventListener("click", function () {

    if (registros.classList.contains("activado")) {
        registros.classList.remove("activado")
    }

    else if (procesos.classList.contains("activado")) {
        procesos.classList.remove("activado")
    }

    else if (movimientos.classList.contains("activado")) {
        movimientos.classList.remove("activado")
    }

    else if (respaldos.classList.contains("activado")) {
        respaldos.classList.remove("activado")
    }

    else if (configuraciones.classList.contains("activado")) {
        configuraciones.classList.remove("activado")
    }

    if (!listados.classList.contains("activado")) {
        listados.classList.toggle("activado")
    }
});

document.getElementById('respaldos').addEventListener("click", function () {

    if (registros.classList.contains("activado")) {
        registros.classList.remove("activado")
    }

    else if (procesos.classList.contains("activado")) {
        procesos.classList.remove("activado")
    }

    else if (movimientos.classList.contains("activado")) {
        movimientos.classList.remove("activado")
    }

    else if (listados.classList.contains("activado")) {
        listados.classList.remove("activado")
    }

    else if (configuraciones.classList.contains("activado")) {
        configuraciones.classList.remove("activado")
    }

    if (!respaldos.classList.contains("activado")) {
        respaldos.classList.toggle("activado")
    }
});

document.getElementById('configuraciones').addEventListener("click", function () {

    if (registros.classList.contains("activado")) {
        registros.classList.remove("activado")
    }

    else if (procesos.classList.contains("activado")) {
        procesos.classList.remove("activado")
    }

    else if (movimientos.classList.contains("activado")) {
        movimientos.classList.remove("activado")
    }

    else if (listados.classList.contains("activado")) {
        listados.classList.remove("activado")
    }

    else if (respaldos.classList.contains("activado")) {
        respaldos.classList.remove("activado")
    }

    if (!configuraciones.classList.contains("activado")) {
        configuraciones.classList.toggle("activado")
    }
});