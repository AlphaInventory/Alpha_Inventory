// MODAL SUPLIDORES (MOSTRAR)
let modalS = document.getElementById('miModalS');
let flexS = document.getElementById('flexS');
let abrirS = document.getElementById('abrirS');
let cerrarS = document.getElementById('closeS');

abrirS.addEventListener('click', function () {
    modalS.style.display = 'block';
});

cerrarS.addEventListener('click', function () {
    modalS.style.display = 'none';
});

window.addEventListener('click', function (e) {
    console.log(e.target);
    if (e.target == flexS) {
        modalS.style.display = 'block';
    }
});

// MODAL ENCARGADOS DE COMPRAS (MOSTRAR)
let modalENCM = document.getElementById('miModalENCM');
let flexENCM = document.getElementById('flexENCM');
let abrirENCM = document.getElementById('abrirENCM');
let cerrarENCM = document.getElementById('closeENCM');

abrirENCM.addEventListener('click', function () {
    modalENCM.style.display = 'block';
});

cerrarENCM.addEventListener('click', function () {
    modalENCM.style.display = 'none';
});

window.addEventListener('click', function (e) {
    console.log(e.target);
    if (e.target == flexENCM) {
        modalENCM.style.display = 'block';
    }
});

// MODAL ARTICULOS (MOSTRAR)
let modalA = document.getElementById('miModalA');
let flexA = document.getElementById('flexA');
let abrirA = document.getElementById('abrirA');
let cerrarA = document.getElementById('closeA');

abrirA.addEventListener('click', function () {
    modalA.style.display = 'block';
});

cerrarA.addEventListener('click', function () {
    modalA.style.display = 'none';
});

window.addEventListener('click', function (e) {
    console.log(e.target);
    if (e.target == flexA) {
        modalA.style.display = 'block';
    }
});

