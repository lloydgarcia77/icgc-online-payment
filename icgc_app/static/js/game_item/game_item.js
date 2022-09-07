$(document).ready(function () {
    $("#card-game-amount .game-item").on("click", function(e){
        $(this).closest('.game-amount-container').find(".game-item").removeClass("active")
        $(this).addClass("active");
    })
    $("#card-game-payment .game-item").on("click", function(e){
        $(this).closest('.game-amount-container').find(".game-item").removeClass("active")
        $(this).addClass("active");
    })
})