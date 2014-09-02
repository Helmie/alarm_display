(function ($, L) {
    $(function () {
        $('#map').each(function() {
            var target = [52.638, 13.31374];
            
            var map = L.map('map');
            
            map.setView(target, 16);
    
            L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>'
            }).addTo(map);
    
            L.tileLayer('http://openfiremap.org/hytiles/{z}/{x}/{y}.png').addTo(map);
            L.tileLayer('http://openfiremap.org/eytiles/{z}/{x}/{y}.png').addTo(map);
    
            L.marker(target, {icon: L.AwesomeMarkers.icon({
                icon: 'fire',
                color: 'red'
            })}).addTo(map);
        });
    });
})(jQuery, L);