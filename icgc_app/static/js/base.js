$(document).ready(function () { 

    setTimeout(function () {
        var preloader = $(".preloader");

        if (preloader) {
            preloader.css('height', 0);
            setTimeout(function () {
                preloader.children().hide();
            }, 200);
        }
    }, 500);

   
})