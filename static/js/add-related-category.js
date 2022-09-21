$(document).ready(function(){
    // Initialize select2
    $('#id_category').select2();

    // Render add new button
    var add_button = '<img id="addlink" data-toggle="modal" data-target="#id_category_modal" style="padding-left: 0.15em; padding-bottom: 0.125em; width: 1.15em" src="http://127.0.0.1:8000/static/img/icon-addlink.svg">';
    var label = $('label[for="id_category"]').closest("label");
    $(label).append(add_button);

    var category_input = $("#id_category_name_input");
    var category_submit = $("#id_category_name_submit");

    category_submit.on("click", function(){
        var result = true;
        $("select > option").each(function(){
            if (this.text == category_input.val()){
                result = false;
                return false;
            }
        });

        var csrf_token = $('meta[name="csrf-token"]').attr('content');
        var url = document.URL;

        if (result !== false){
            $.ajax({
                method: "POST",
                url: url,
                data: {"name": category_input.val()},
                headers: {'X-CSRFTOKEN': csrf_token}
                }).done(function(response){
                    $('#id_category_modal').modal('hide');
                    console.log(response['id'])

                    // Append option to select
                    var newOption = new Option(category_input.val(), response['id'], true, true);
                    $('#id_category').append(newOption).trigger('change');

                    category_input.removeClass('is-invalid');
                    category_input.val('');
                });
        } else {
            category_input.addClass('is-invalid');
            invalid_msg = '<small id="id_category_invalid" class="text-danger">Category with this name already exists.</small>';
            
            if ($('#id_category_invalid').length){
                $('id_category_invalid').html(invalid_msg);
            } else {
                $('.modal-body').append(invalid_msg);
            };
        };
    });
});
