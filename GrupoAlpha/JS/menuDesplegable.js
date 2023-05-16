$(document).ready(function () {
    //jquery for toggle sub menus
    $('.sub-boton').click(function () {
        $(this).next('.sub-menu').slideToggle();
        $(this).find('.dropdown').toggleClass('rotate');
    });

    //jquery for expand and collapse the sidebar
    $('.menu-boton').click(function () {
        $('.barra-lateral').addClass('active');
        $('menu-boton').css("visibility", "hidden");
    });

    $('.cerrar-boton').click(function () {
        $('.barra-lateral').removeClass('active');
        $('menu-boton').css("visibility", "visible");
    });
});