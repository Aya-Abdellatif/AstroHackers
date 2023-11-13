var moon = document.getElementById('moon');
var earth = document.getElementById('earth');
var sun = document.getElementById('sun');
var black_bg = document.getElementById('black_bg');
var moon_black_bg = document.getElementById('moon_black_bg');
var text = document.getElementById('txt');


black_bg.style.transition = "opacity 0.8s";
moon_black_bg.style.transition = "opacity 0.8s";
text.style.transition = "opacity 0.8s";

document.addEventListener('mousemove', function(event) {
    var mouseX = event.clientX;
    var mouseY = event.clientY;
    


    var point = get_intersection_point(mouseX, mouseY);

    moon.style.left = point[0] + 'px';
    moon.style.top = point[1] + 'px';
    moon_black_bg.style.left = point[0] + 'px';
    moon_black_bg.style.top = point[1] + 'px';

    if (Math.abs(point[1] - (window.innerHeight * 0.5 - 60)) <= 100 && point[0] > window.innerWidth * 0.5 - 50){
        black_bg.style.opacity = 0.8;
        text.innerHTML = "Solar Eclipse";
        text.style.opacity = 1;
    }else{
        black_bg.style.opacity = 0.0;
    }

    if (Math.abs(point[1] - (window.innerHeight * 0.5 - 60)) <= 100 && point[0] < window.innerWidth * 0.5 - 150){
        moon_black_bg.style.opacity = 0.8;
        text.innerHTML = "Lunar Eclipse";
        text.style.opacity = 1;
    }else{
        moon_black_bg.style.opacity = 0.0;
    }

    if (!(Math.abs(point[1] - (window.innerHeight * 0.5 - 60)) <= 100 && point[0] > window.innerWidth * 0.2) && !(Math.abs(point[1] - (window.innerHeight * 0.5 - 60)) <= 100 && point[0] < window.innerWidth * 0.2)){
        text.style.opacity = 0;
    }
});


function get_intersection_point(x, y){
    var CentreEarthX = window.innerWidth * 0.5 - 150;
    var CentreEarthY = window.innerHeight * 0.5 - 30;

    var dx = x - CentreEarthX;
    var dy = y - CentreEarthY;

    var k_squared = (125 * 125) / (dx * dx + dy * dy);
    var k = Math.sqrt(k_squared);

    return [CentreEarthX + k * dx, CentreEarthY + k * dy];
}
