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

   var wmsResource = resultPath.split('?')[0];
   var rangeURL = "/get_data_range?wms_resource="
                  + encodeURIComponent(wmsResource)
                  + "&layer=" + encodeURIComponent(calculation);

   var smallest = -50;
   var largest = 50;

   $.ajax({
     url: rangeURL
   })
   .done(function( data ) {
      if ( console && console.log ) {
         smallest = data.min;
         largest = data.max;
      }
      var map = L.map('map').setView([-37.81, 144.96], 2);
      var layer = L.tileLayer.wms(wmsResource, {
               layers: calculation,
               format: 'image/png',   
               transparent: true,
               attribution: "Climate Analyser",
               COLORSCALERANGE: smallest + "%2C" + largest
               }).addTo(map);

      L.tileLayer(tilemillServerAddress + '/v2/CountryOutlines/{z}/{x}/{y}.png',{
               maxZoom: 8,
               detectRetina: true
               }).addTo(map);
      });
   });
})(jQuery);
