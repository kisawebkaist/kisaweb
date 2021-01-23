/*
  This javascript file is the manual implementation of 
  basic properties of the dropdown menu used in the blog
  app category navbar. 
*/

///////////////////////////////////////////////////////////////////

/* 
  This function toggles the currently clicked dropdown menu 
  and in case the dropdown menu is toggled into the unshown state
  the sub-menus are also toggled into the unshown state.
*/
toggle_show = (item) => {
  sibling_dropdown = $(item).next('.dropdown-menu')[0];
  if(sibling_dropdown.classList.contains("show")) {
    sibling_dropdown.classList.remove("show")
    descendant_dropdown = $(sibling_dropdown).find('.dropdown-menu');
    for(let i = 0; i < descendant_dropdown.length; i++) {
      descendant_dropdown[i].classList.remove("show");
    }
  }
  else {
    sibling_dropdown.classList.add("show")
  }
};


/*
  This function catches the clicks performed on the document.
  Accordingly, if the click is performed outside of a dropdown menu,
  the corresponding dropdown menu becomes toggled into the unshown state.
*/
$(document).click(function() {
  document.querySelectorAll('.btn-group').forEach(item => {
    if(!item.classList.contains("unchange")) {
      $(item).children('.dropdown-menu')[0].classList.remove("show");
    }
    else {
      item.classList.remove("unchange");
    }
    console.log("Hi");
  });
});

/*
  This is a function that is called whenever all of the 
  DOM elements of the page are ready to be used.
  It is the jQuery short-hand for:
    $(document).ready(function() { ... });
*/
$(function() {
  /*
    This function adds a 'click' EventListener to each dropdown toggler 
    button.
  */
  document.querySelectorAll('.my-toggler').forEach(item => {
    item.addEventListener('click', () => {
      toggle_show(item);
    });
  });

  /*
    This function adds a 'click' EventListener to each dropdown containers.
    Whenever some part of a dropdown container is clicked, "unchange"
    is added to the classList of the corresponding container. This is used
    for determining whether the click is on the dropdown container.
  */
  document.querySelectorAll('.btn-group').forEach(item => {
    item.addEventListener('click', () => {
      if(!item.classList.contains("unchange")) {
        item.classList.add("unchange")
      }
    });
  });
});