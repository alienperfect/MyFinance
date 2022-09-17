$(document).ready(function(){
    // Prevents from typing non numeric values
    $('input[numval]').on("input", function(){
        $(this).val($(this).val().replace(/[^\d.]/g, ''));
    });
});
