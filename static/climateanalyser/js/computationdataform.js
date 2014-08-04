(function($){

   $(document).ready(function(){

      var $form = $("form");

      $form.find("select:not([multiple])").change(function(){

         // ignore "-----" option
         if (!$(this).val()){
            return;
         }

         // get multi-selectbox for variables
         var $variablesSelect = $("#" + $(this).attr("id").replace("datafile",
               "variables"));
         
         $variablesSelect.html("");

         // Get datafile variables
         $.ajax({
            method : "POST",
            dataType : "json",
            url : "/load_datafile_metadata",
            data : { 
               id : $(this).val(),
               csrfmiddlewaretoken : $.cookie("csrftoken")
            }
         }).done(function(response){

            //load variables into multi-selectbox
            for (i = 0; i < response.length; i++) {
               $variablesSelect.append("<option value='" + response[i] + "'>" 
                  + response[i] + "</option>");
            }
         });

      });

   });

})(jQuery);
