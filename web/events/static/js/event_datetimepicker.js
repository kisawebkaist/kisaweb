// Script used in event_form.html
$('.datetimepicker').datetimepicker({
    format: 'YYYY-MM-DD HH:mm:ss',
});

$('#id_event_start_datetime').on('dp.change', function(e) {
    // Event end datetime >= Event start datetime
    $('#id_event_end_datetime').data('DateTimePicker').minDate(e.date);
    // Registration start datetime <= Event start datetime
    $('#id_registration_start_datetime').data('DateTimePicker').maxDate(e.date);
});

$('#id_event_end_datetime').on('dp.change', function(e) {
    // Registration end datetime <= Event end datetime
    $('#id_registration_end_datetime').data('DateTimePicker').maxDate(e.date);
});

$('#id_registration_start_datetime').on('dp.change', function(e) {
    // Registration end datetime >= Registration start datetime
    $('#id_registration_end_datetime').data('DateTimePicker').minDate(e.date);
});
