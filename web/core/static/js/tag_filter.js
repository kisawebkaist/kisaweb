// Toggle active status of clicked tag
$('button.tag').click(function() {
    $(this).toggleClass('active');
});

// Unselect all tags when reset button is pressed
$('button#tag-reset').click(function() {
    $('.tag.active').removeClass('active');
});

// Grab the selected tags when search button is pressed and make GET request
$('button#tag-search').click(function() {
    let tags = document.querySelectorAll(".tag.active");
    if (tags.length >= 1) {
        $("#results-area").empty();
        let tagValues = [];
        for (let i = 0; i < tags.length; i++) tagValues.push(tags[i].value);

        $.get( "", { "tags[]": tagValues } ); // routes to http://domain.com/app
        // If you want to route the GET request to some other url, edit the first parameter above
        // For example: $.get( "search", { "tags[]": tagValues } ); will route the request to http://domain.com/app/search
    }
});
