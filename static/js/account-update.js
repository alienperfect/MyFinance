// Make sure one field is disabled if the other is set
if ( $( "#id_hourly_rate" ).val() != '' ){
    $( "#id_monthly_salary" ).prop( "disabled", true );
} else {
    // Hide by default
    $('input#id_hours_worked').val('');
    $('label[for=id_hours_worked], input#id_hours_worked').hide();
}

if ( $( "#id_monthly_salary" ).val() != '' ){
    $( "#id_hourly_rate" ).prop( "disabled", true );
}


$(document).ready(function(){
    $( "#id_hourly_rate" ).on("input", function(){
        if ( $(this).val() != '' ){
            $( "#id_monthly_salary" ).prop( "disabled", true );
            $('label[for=id_hours_worked], input#id_hours_worked').show();
        } else {
            $( "#id_monthly_salary" ).prop( "disabled", false );
            $('input#id_hours_worked').val('');
            $('label[for=id_hours_worked], input#id_hours_worked').hide();
        }
      });

    $( "#id_monthly_salary" ).on("input", function(){
        if ( $(this).val() != '' ){
            $( "#id_hourly_rate" ).prop( "disabled", true );
        } else {
            $( "#id_hourly_rate" ).prop( "disabled", false );
        }
      });
    
    // Image preview
    input_file = $('input[type=file]');
    input_file.after('<img id="id_preview" width=250>');

    input_file.change(function(){
        var file = input_file.get(0).files[0];

        if (file){
            $('#id_preview').attr('src', URL.createObjectURL(file));
        }   
    });
});
