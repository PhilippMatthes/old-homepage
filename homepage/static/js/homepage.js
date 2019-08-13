

$(document).ready(function() {

    window.applyShine = function(element) {
        var shine = document.createElement("div");
        shine.className = "shine";
        shine.style.display = "block";
        element.append(shine);

        element.mousemove(function(event) {
            var rect = $(this).get(0).getBoundingClientRect();
            var x = Math.abs(rect.x - event.clientX) / rect.width * 100;
            var y = Math.abs(rect.y - event.clientY) / rect.height * 100;
            xR = -(x-50)/5;
            yR = -(y-50)/5;
            $(this).css({
                "transform": "rotateY(" + xR + "deg) rotateX(" + yR + "deg)",
            });
            shine.style.backgroundImage = `radial-gradient(circle at ${100 - x}% ${y}%, rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0))`;
        });

        element.mouseleave(function() {
           $(this).css({
                "transform": "none",
            });
        });
    };

    $(".card").each(function(index) {
        window.applyShine($(this));
    });

});
