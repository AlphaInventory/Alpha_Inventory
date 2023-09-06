// MODAL CREADOR MARCAS
let modalM = document.getElementById('miModalM');
let flexM = document.getElementById('flexM');
let abrirM = document.getElementById('abrirM');
let cerrarM = document.getElementById('closeM');

abrirM.addEventListener('click', function(){
    modalM.style.display = 'block';
});

cerrarM.addEventListener('click', function(){
    modalM.style.display = 'none';
});

window.addEventListener('click', function(e){
    console.log(e.target);
    if(e.target == flexM){
        modalM.style.display = 'block';
    }
});

// MODAL CREADOR ENCARGADO DE VENTAS
let modalENV = document.getElementById('miModalENV');
let flexENV = document.getElementById('flexENV');
let abrirENV = document.getElementById('abrirENV');
let cerrarENV = document.getElementById('closeENV');

abrirENV.addEventListener('click', function(){
    modalENV.style.display = 'block';
});

cerrarENV.addEventListener('click', function(){
    modalENV.style.display = 'none';
});

window.addEventListener('click', function(e){
    console.log(e.target);
    if(e.target == flexENV){
        modalENV.style.display = 'block';
    }
});

// MODAL CREADOR ENCARGADO DE COMPRAS
let modalENC = document.getElementById('miModalENC');
let flexENC = document.getElementById('flexENC');
let abrirENC = document.getElementById('abrirENC');
let cerrarENC = document.getElementById('closeENC');

abrirENC.addEventListener('click', function () {
    modalENC.style.display = 'block';
});

cerrarENC.addEventListener('click', function () {
    modalENC.style.display = 'none';
});

window.addEventListener('click', function (e) {
    console.log(e.target);
    if (e.target == flexENC) {
        modalENC.style.display = 'block';
    }
});

// MODAL MARCAS (MOSTRAR)
let modalMM = document.getElementById('miModalMM');
let flexMM = document.getElementById('flexMM');
let abrirMM = document.getElementById('abrirMM');
let cerrarMM = document.getElementById('closeMM');

abrirMM.addEventListener('click', function(){
    modalMM.style.display = 'block';
});

cerrarMM.addEventListener('click', function(){
    modalMM.style.display = 'none';
});

window.addEventListener('click', function(e){
    console.log(e.target);
    if(e.target == flexMM){
        modalMM.style.display = 'block';
    }
});