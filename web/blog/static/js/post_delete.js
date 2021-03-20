/*
    This file is created to send a POST request through javascript 
    ajax request to the corresponding url to delete a post. 
*/

$('#post_delete').on('click', function() {
    if (confirm(`Do you want to delete this post?`)) {
        $.ajax({
            type: 'POST',
            url: $(this).attr('data-post-delete-url'),
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
