$(function() {
    $('.vote-single').on('click', function() {
        var vote_type = $(this).val();
        if (confirm(`Are you sure you want to vote ${vote_type.toUpperCase()} for this candidate?`)) {
            $.ajax({
                type: 'POST',
                url: $(this).attr('data-url'),
                data: {
                    'type': vote_type,
                    'csrfmiddlewaretoken': CSRF_TOKEN,
                },
                success: (response) => {location.reload()},
                error: () => {alert('Error');},
            });
        }
    });
});
