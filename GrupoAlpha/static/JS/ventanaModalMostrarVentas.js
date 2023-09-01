// MODAL CLIENTES (MOSTRAR)
let modalC = document.getElementById('miModalC');
let flexC = document.getElementById('flexC');
let abrirC = document.getElementById('abrirC');
let cerrarC = document.getElementById('closeC');

abrirC.addEventListener('click', function () {
    modalC.style.display = 'block';
});

cerrarC.addEventListener('click', function () {
    modalC.style.display = 'none';
});

window.addEventListener('click', function (e) {
    console.log(e.target);
    if (e.target == flexC) {
        modalC.style.display = 'block';
    }
});

// MODAL ENCARGADOS DE VENTAS (MOSTRAR)
let modalENVM = document.getElementById('miModalENVM');
let flexENVM = document.getElementById('flexENVM');
let abrirENVM = document.getElementById('abrirENVM');
let cerrarENVM = document.getElementById('closeENVM');

abrirENVM.addEventListener('click', function () {
    modalENVM.style.display = 'block';
});

cerrarENVM.addEventListener('click', function () {
    modalENVM.style.display = 'none';
});

window.addEventListener('click', function (e) {
    console.log(e.target);
    if (e.target == flexENVM) {
        modalENVM.style.display = 'block';
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