$(document).ready(function(){
    $('#id_category').select2();

    var add_button = '<img id="addlink" data-toggle="modal" data-target="#exampleModalCenter" src="http://127.0.0.1:8000/static/img/icon-addlink.svg">';
    var label = $('label[for="id_category"]').closest("label");
    var input = $("#name-input");
    var submit = $("#name-submit");

    $(label).append(add_button);

    submit.on("click", function(){
        var result = true;
        $("select > option").each(function() {
            if (this.text == input.val()){
                result = false;
                return false;
            }
        });

        if (result !== false){
            $.ajax({
                method: "POST",
                url: 'http://127.0.0.1:8000/accounting/endpoint/',
                data: {"name": input.val(), "pk": $('meta[name="pk"]').attr('content')},
                headers: {
                    'X-CSRFTOKEN': $('meta[name="csrf-token"]').attr('content')
                }
                }).done(function(resp){
                    console.log(resp);
                    $('#exampleModalCenter').modal('hide');

                    var option = option = $('<option/>');
                    var lastValue = parseInt( $('select[id="id_category"] option:last-child').val());
                    console.log(lastValue)
                    option.attr({ 'value': lastValue+1, 'selected': '' }).text(input.val());
                    $('select[id="id_category"]').append(option);

                    input.removeClass('is-invalid');
                    input.val('');
                });
        } else {
            input.addClass('is-invalid');
            $('.modal-body').append('<small id="passwordHelp" class="text-danger">Category with this name already exists.</small>');
        };
    });
});
