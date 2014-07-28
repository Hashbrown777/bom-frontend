(function($){

 $(window).ready(function(){

   var map = L.map('map').setView([-37.81, 144.96], 2);

   var layer = L.tileLayer.wms(resultPath, {
            layers: 'correlation',
            format: 'image/png',   
            transparent: true,
            attribution: "Sample weather data"
            }).addTo(map);

   L.tileLayer('http://118.138.241.181/v2/CountryOutlines/{z}/{x}/{y}.png',{
            maxZoom: 8,
            detectRetina: true
            }).addTo(map);
 });

})(jQuery);
