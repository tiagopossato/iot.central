$(document).ready(function () {
    //retrai o menu, somente em telas largas
    if (window.matchMedia('(min-width: 992px)').matches) {
        $('#menu_toggle').click();
    }
});