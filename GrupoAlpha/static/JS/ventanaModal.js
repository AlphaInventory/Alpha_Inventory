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

let modalll = document.getElementById('miModal--');
let flexxx = document.getElementById('flex--');
let abrirrr = document.getElementById('abrir--');
let cerrarrr = document.getElementById('close--');

abrirrr.addEventListener('click', function () {
    modalll.style.display = 'block';
});

cerrarrr.addEventListener('click', function () {
    modalll.style.display = 'none';
});

window.addEventListener('click', function (e) {
    console.log(e.target);
    if (e.target == flexxx) {
        modalll.style.display = 'none';
    }
});

let modallll = document.getElementById('miModal---');
let flexxxx = document.getElementById('flex---');
let abrirrrr = document.getElementById('abrir---');
let cerrarrrr = document.getElementById('close---');

abrirrrr.addEventListener('click', function () {
    modallll.style.display = 'block';
});

cerrarrrr.addEventListener('click', function () {
    modallll.style.display = 'none';
});

window.addEventListener('click', function (e) {
    console.log(e.target);
    if (e.target == flexxxx) {
        modallll.style.display = 'none';
    }
});

let modalllll = document.getElementById('miModal----');
let flexxxxx = document.getElementById('flex----');
let abrirrrrr = document.getElementById('abrir----');
let cerrarrrrr = document.getElementById('close----');

abrirrrrr.addEventListener('click', function () {
    modalllll.style.display = 'block';
});

cerrarrrrr.addEventListener('click', function () {
    modalllll.style.display = 'none';
});

window.addEventListener('click', function (e) {
    console.log(e.target);
    if (e.target == flexxxxx) {
        modalllll.style.display = 'none';
    }
});

let modallllll = document.getElementById('miModal-----');
let flexxxxxx = document.getElementById('flex-----');
let abrirrrrrr = document.getElementById('abrir-----');
let cerrarrrrrr = document.getElementById('close-----');

abrirrrrrr.addEventListener('click', function () {
    modallllll.style.display = 'block';
});

cerrarrrrrr.addEventListener('click', function () {
    modallllll.style.display = 'none';
});

window.addEventListener('click', function (e) {
    console.log(e.target);
    if (e.target == flexxxxxx) {
        modallllll.style.display = 'none';
    }
});