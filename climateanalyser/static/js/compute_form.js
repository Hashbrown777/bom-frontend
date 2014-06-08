jQuery(function($){

   //Add more file inputs to computation form
   $("#add_file").click(function(){
      event.preventDefault();

      $container = $("#data_file_container").find('p');
      $extraField = $container.find("input").clone();

      idCount = parseInt($extraField.attr('id').split('_')[2]);
      newIdCount = idCount + 1;

      $extraField.attr('id', 'file_url_' + newIdCount);
      $container.append($extraField);

   });

   
});
