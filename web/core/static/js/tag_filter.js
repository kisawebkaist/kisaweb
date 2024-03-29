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
        let tagValues = [];
        for (let i = 0; i < tags.length; i++)
            tagValues.push(tags[i].value);
        updateGetRequestParams("tags", tagValues);
    }
    else {
        updateGetRequestParams("tags", null);
    }
    window.location.assign(url.href);
});

// Toggle visiblity of tag selection area and active tags when Filter button is pressed
$('#tag-filter-button').click(function() {
    $(this).toggleClass('btn-outline-dark');
    $(this).toggleClass('btn-dark');
    $('#tag-filter-area').toggle('fast');
    $('#active-tags').toggle( 'fast');
});

updateGetRequestParams = (key, value) => {
    if(value == null) {
        url.searchParams.delete(key);
    }
    else {
        url.searchParams.set(key, value);
    }
};

// Set all tags in url parameter as active
$(document).ready(() => {
    url = new URL(window.location.href);
    let tagParams = url.searchParams.get("tags");
    if (tagParams != null) {
        let selectedTags = tagParams.split(",");
        for (let i = 0; i < selectedTags.length; i++) {
            let sanitizedTag = DOMPurify.sanitize(selectedTags[i]);
            $(`.tag[value="${sanitizedTag}"]`).addClass("active");
            $('#active-tags').append(`
                <button class = "tag btn btn-outline-dark btn-sm rounded-pill border-0 my-1" disabled><b>#</b>${sanitizedTag}</button>
            `);
            // $(`.tag[value="${selectedTags[i]}"]`).addClass("active");
            // $('#active-tags').append(`
            //     <button class = "tag btn btn-outline-dark btn-sm rounded-pill border-0 my-1" disabled><b>#</b>${selectedTags[i]}</button>
            // `);
        }
    }
});
