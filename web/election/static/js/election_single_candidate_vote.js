// this script enables handling the single candidate vote page
// focuses on the yes/no vote buttons

// register a function
$(function() {
    // when the yes or no button is clicked, register the following callback function
    $('.vote-single').on('click', function() {
        // get the vote type (yes or no) from the button text
        var vote_type = $(this).val();
        // send an alert to the user to be confirmed to vote
        if (confirm(`Are you sure you want to vote ${vote_type.toUpperCase()} for this candidate?`)) {
            // make an ajax POST request to the backend to inform the backend of the vote
            $.ajax({
                type: 'POST',
                url: $(this).attr('data-url'), // the url of request is registered in the button
                data: {
                    'type': vote_type,
                    'csrfmiddlewaretoken': CSRF_TOKEN,
                }, // data consists of the vote type and the CSRF_TOKEN
                success: (response) => { // in case of a successful request
                    if (response == 'novote') { // if the vote is rejected
                        // TODO: optional, nothing needed to be done
                    }
                    else if (response == 'Success') { // if the voted is accepted
                        // TODO: optional, nothing needed to be done
                    }
                    location.reload(); // reload the page
                },
                error: () => {alert('Error');}, // in case of an error while making the request
            });
        }
    });
});
