// Script used in event_form.html

$('#id_no_registration').on('click', function() {
    $regis_start = $('#id_registration_start_datetime');
    $regis_end = $('#id_registration_end_datetime');
    if ($(this).prop('checked')) {
        $regis_start.val('');
        $regis_start.prop('disabled', true);
        $regis_end.val('');
        $regis_end.prop('disabled', true);
    }
    else {
        $regis_start.prop('disabled', false);
        $regis_end.prop('disabled', false);
    }
});

$('#event_delete').on('click', function() {
    title = $(this).attr('data-title')
    if (confirm(`Do you want to delete the event ${title}`)) {
        $.ajax({
            type: 'POST',
            url: $(this).attr('data-event-delete-url'),
            data:{
                'csrfmiddlewaretoken': CSRF_TOKEN,
            },
            success: (e) => {
                window.location.href = e
            },
            error: () => {
                alert('Error')
            },
        });
    }
});
