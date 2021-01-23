/*
  This javascript file is used while previewing the properties of 
  the added image at the time of creating/updating a post.
*/

/////////////////////////////////////////////////////

/*
  This function is used for reading the URL of the temporarily 
  uploaded image through the image upload box.
*/
function readURL(input, $preview) {
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function(e) {
      $preview.attr('src', e.target.result);
    };
    reader.readAsDataURL(input.files[0]);
  }
}


/*
  This is a function that is called whenever all of the 
  DOM elements of the page are ready to be used.
  It is the jQuery short-hand for:
    $(document).ready(function() { ... });
*/
$(function() {

  $image_preview = $('#image_preview');
  
  /*
    This function is called whenever a 'click' is performed on
    the HTML element with id 'reset-id-reset' which resets the 
    post creating/updating form. If the corresponding post form 
    is a post create form, this function resets the img source to ''.
    If the post form is a post update form, this function assigns the
    retrieves the old image source.
  */
  $('#reset-id-reset').on("click", () => {
    currently = $("span[class='text-break']");
    if(currently.length > 0) {
      normal_img_link = $(currently[0].getElementsByTagName('a')[0]).attr('href');
      $image_preview.attr('src', normal_img_link);
    }
    else {
      $image_preview.attr('src', '');
    }
    $("label[for='image']")[1].textContent = '---';
  });

  /*
    This function adds a 'change' EventListener on the element with 
    id 'image' which is an image upload box. As a result of this 
    EventListener, the URL of the temporarily uploaded image 
    is retrieved.
  */
  $('#image').on("change", function() {
    readURL(this, $image_preview);
  });

});

