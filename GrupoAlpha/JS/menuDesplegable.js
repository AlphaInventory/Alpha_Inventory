let listElements = document.querySelectorAll('.lista_boton--click');

listElements.forEach(listElement => {
    listElement.addEventListener('click', ()=>{
        
        listElement.classList.toggle('lista_arrow');

        let height = 0;
        let menu = listElement.nextElementSibling;
        if(menu.clientHeight == "0"){
            height=menu.scrollHeight;
        }

        menu.style.height = `${height}px`;

    })

    const menu = document.getElementsByClassName('contenedor_menu');

    for (i=0; i<menu.length; i++) {
        menu[i].addEventListener('click', function () {
        this.classList.toggle('lista_show')
        })
    }
    
});