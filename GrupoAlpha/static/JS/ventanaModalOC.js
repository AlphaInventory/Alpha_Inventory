let modalOC = document.getElementById('miModalOC');
let flexOC = document.getElementById('flexOC');
let abrirOC = document.getElementById('abrirOC');
let cerrarOC = document.getElementById('closeOC');

abrirOC.addEventListener('click', function () {
    modalOC.style.display = 'block';
});

cerrarOC.addEventListener('click', function () {
    modalOC.style.display = 'none';
});

window.addEventListener('click', function (e) {
    console.log(e.target);
    if (e.target == flexOC) {
        modalOC.style.display = 'none';
    }
});