// MODAL ELIMINAR CUENTA
let modalEC = document.getElementById('miModalEC');
let flexEC = document.getElementById('flexEC');
let abrirEC = document.getElementById('abrirEC');
let cerrarEC = document.getElementById('closeEC');

abrirEC.addEventListener('click', function () {
    modalEC.style.display = 'block';
});

cerrarEC.addEventListener('click', function () {
    modalEC.style.display = 'none';
});

window.addEventListener('click', function (e) {
    console.log(e.target);
    if (e.target == flexEC) {
        modalEC.style.display = 'block';
    }
});