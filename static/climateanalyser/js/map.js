(function($){

 $(window).ready(function(){

   switch (calculation) {
      case 'correlate':
         calculation = 'correlation';
         break;
      case 'regress':
         calculation = 'regression';
         break;
   }

   var map = L.map('map').setView([-37.81, 144.96], 2);
   var layer = L.tileLayer.wms(resultPath, {
            layers: calculation,
            format: 'image/png',   
            transparent: true,
            attribution: "Climate Analysis data"
            }).addTo(map);

   L.tileLayer('http://118.138.241.181/v2/CountryOutlines/{z}/{x}/{y}.png',{
            maxZoom: 8,
            detectRetina: true
            }).addTo(map);
 });

})(jQuery);
