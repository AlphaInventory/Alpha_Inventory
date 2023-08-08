$(document).ready(function () {
    $('.sub-boton').click(function () {
        $(this).next('.sub-menu').slideToggle();
        $(this).find('.dropdown').toggleClass('rotate');
    });

    $('.menu-boton').click(function () {
        $('.barra-lateral').addClass('active');
        $('menu-boton').css("visibility", "hidden");
    });

    $('.cerrar-boton').click(function () {
        $('.barra-lateral').removeClass('active');
        $('menu-boton').css("visibility", "visible");
    });
});