function confirmacionM() {
    var conf =  confirm("Estas seguro de que quieres guardar esta marca?");

    if(conf == true) {
        return true;
    } else {
        return false;
    }
}

function confirmacionEV() {
    var confEV = confirm("Estas seguro que quieres guardar este encargardo de ventas");

    if(confEV == true) {
        return true;
    } else {
        return false;
    }
}

function confirmacionEC() {
    var confEC = confirm("Estas seguro que quieres guardar este encargardo de compras");

    if(confEC == true) {
        return true;
    } else {
        return false;
    }
}
