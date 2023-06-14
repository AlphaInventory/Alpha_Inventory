function validarCampo_Contraseña() {
    var caja1 = document.getElementById("nom");
    var caja2 = document.getElementById("ape");
    var caja3 = document.getElementById("dir");
    var caja4 = document.getElementById("tel");
    var caja5 = document.getElementById("email");
    var caja6 = document.getElementById("password");
    var caja7 = document.getElementById("password-");

    if(caja1.value == "") {
        alert("El campo no puede estar en blanco.");
        caja1.focus();
        caja2.style.border = 0;
        caja3.style.border = 0;
        caja4.style.border = 0;
        caja5.style.border = 0;
        caja6.style.border = 0;
        caja7.style.border = 0;
        caja1.style.border = "3px solid #f00";
        return false;
    } else if(caja2.value == "") {
        alert("El campo no puede estar en blanco.");
        caja2.focus();
        caja1.style.border = 0;
        caja3.style.border = 0;
        caja4.style.border = 0;
        caja5.style.border = 0;
        caja6.style.border = 0;
        caja7.style.border = 0;
        caja2.style.border = "3px solid #f00";
        return false;
    } else if(caja3.value == "") {
        alert("El campo no puede estar en blanco.");
        caja3.focus();
        caja1.style.border = 0;
        caja2.style.border = 0;
        caja4.style.border = 0;
        caja5.style.border = 0;
        caja6.style.border = 0;
        caja7.style.border = 0;
        caja3.style.border = "3px solid #f00";
        return false;
    } else if(caja4.value == "") {
        alert("El campo no puede estar en blanco.");
        caja4.focus();
        caja1.style.border = 0;
        caja2.style.border = 0;
        caja3.style.border = 0;
        caja5.style.border = 0;
        caja6.style.border = 0;
        caja7.style.border = 0;
        caja4.style.border = "3px solid #f00";
        return false;
    } else if(caja5.value == "") {
        alert("El campo no puede estar en blanco.");
        caja5.focus();
        caja1.style.border = 0;
        caja2.style.border = 0;
        caja3.style.border = 0;
        caja4.style.border = 0;
        caja6.style.border = 0;
        caja7.style.border = 0;
        caja5.style.border = "3px solid #f00";
        return false;
    } else if(caja6.value == "") {
        alert("La contraseña no puede estar en blanco.");
        caja6.focus();
        caja1.style.border = 0;
        caja2.style.border = 0;
        caja3.style.border = 0;
        caja4.style.border = 0;
        caja5.style.border = 0;
        caja7.style.border = 0;
        caja6.style.border = "3px solid #f00";
        return false;
    } else if(caja7.value == "") {
        alert("La contraseña no puede estar en blanco.");
        caja7.focus();
        caja1.style.border = 0;
        caja2.style.border = 0;
        caja3.style.border = 0;
        caja4.style.border = 0;
        caja5.style.border = 0;
        caja6.style.border = 0;
        caja7.style.border = "3px solid #f00";
        return false;
    } else {
        caja7.style.border = 0;
    }

    let pwd=document.getElementById("password").value;
    let pwdn=document.getElementById("password-").value;

    if(pwd.length < 8) {
        alert("La contraseña debe tener 8 caracteres minimos")
    } else if(pwd === pwdn) {
        window.location="metododepago.html"
    } else {
        alert("Las contraseñas no coinciden");
    }
}