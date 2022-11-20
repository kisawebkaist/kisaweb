// this script enables changing the video embedding ratio

$(function() {
    var oldval;

    $('.ratio-select').on('focus', function() {
        oldval = $(this).val();
    }).on('change', function() {
        $.ajax({
            type: 'POST',
            url: $(this).attr('data-embed-ratio-url'),
            data: {
                'ratio': $(this).val(),
                'csrfmiddlewaretoken': CSRF_TOKEN,
            },
            success: (response) => {
                if (response == 'Success') {
                    let oldclass = `embed-responsive-${ oldval }`;
                    let newclass = `embed-responsive-${ $(this).val() }`;
                    $('.embed-responsive').removeClass(oldclass).addClass(newclass);
                }
                else {
                    alert('Error1');
                }
            },
            error: () => {
                alert('Error0');
            },
        });
    });
});
