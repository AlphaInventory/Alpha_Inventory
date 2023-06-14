let modal = document.getElementById('miModal');
let flex = document.getElementById('flex');
let abrir = document.getElementById('abrir');
let cerrar = document.getElementById('close');

abrir.addEventListener('click', function(){
    modal.style.display = 'block';
});

cerrar.addEventListener('click', function(){
    modal.style.display = 'none';
});

window.addEventListener('click', function(e){
    console.log(e.target);
    if(e.target == flex){
        modal.style.display = 'none';
    }
});

let modall = document.getElementById('miModal-');
let flexx = document.getElementById('flex-');
let abrirr = document.getElementById('abrir-');
let cerrarr = document.getElementById('close-');

abrirr.addEventListener('click', function(){
    modall.style.display = 'block';
});

cerrarr.addEventListener('click', function(){
    modall.style.display = 'none';
});

window.addEventListener('click', function(e){
    console.log(e.target);
    if(e.target == flexx){
        modall.style.display = 'none';
    }
});