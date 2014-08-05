(function($){

   $(document).ready(function(){

      var $form = $("form");

      /**
       * Populate the variables multi-selectbox based on the selected datafile.
       *
       * Will make an ajax call to get list of variables to use.
       */
      function populateVariables(datafileSelect){

         // ignore "-----" option
         if (!$(datafileSelect).val()){
            return;
         }

         // get multi-selectbox for variables
         var $variablesSelect = $("#" + $(datafileSelect).attr("id")
               .replace("datafile", "variables"));
         
         $variablesSelect.html("");

         // Get datafile variables
         $.ajax({
            method : "POST",
            dataType : "json",
            url : "/load_datafile_metadata",
            data : { 
               id : $(datafileSelect).val(),
               csrfmiddlewaretoken : $.cookie("csrftoken")
            }
         }).done(function(response){

            //load variables into multi-selectbox
            for (i = 0; i < response.length; i++) {
               $variablesSelect.append("<option value='" + response[i] + "'>" 
                  + response[i] + "</option>");
            }
         });
      };

      $form.find("select[id$=datafile]").change(function(){
         //Load variables each time datafile changes
         populateVariables(this);
      }).each(function(){ 
         //if we need to populate variables selectbox on page load
         populateVariables(this);
      });


   });

})(jQuery);
