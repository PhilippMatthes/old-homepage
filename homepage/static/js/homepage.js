

$(document).ready(function() {

    $(".card").each(function(index) {

        var shine = document.createElement("div");
        shine.className = "shine";
        shine.style.display = "block";
        $(this).append(shine);

        $(this).mousemove(function(event) {
            var rect = $(this).get(0).getBoundingClientRect();
            var x = Math.abs(rect.x - event.clientX) / rect.width * 100;
            var y = Math.abs(rect.y - event.clientY) / rect.height * 100;
            x = -(x-50)/10;
            y = -(y-50)/10;
            $(this).css({
                "transform": "rotateY(" + x + "deg) rotateX(" + y + "deg)",
            });
            shine.style.backgroundImage = `radial-gradient(circle at ${100-x}% ${100-y}%, rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0))`;
        });

        $(this).mouseleave(function() {
            $(this).css({
                "transform": "none",
            });
        });
    });

});
