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
    if (tags.length > 0) {
        $("#results-area").empty();
        let tagValues = [];
        for (let i = 0; i < tags.length; i++) 
            tagValues.push(tags[i].value);
        updateGetRequestParams("tags[]", tagValues);
    }
    else {
        updateGetRequestParams("tags[]", null);
    }
    window.location.assign(url.href);
});

updateGetRequestParams = (key, value) => {
    if(value == null) {
        url.searchParams.delete(key);
    }
    else {
        url.searchParams.set(key, value);
    }
};

$(document).ready(() => {
    url = new URL(window.location.href);    
});