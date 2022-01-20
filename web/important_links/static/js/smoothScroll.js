$(document).ready(function(){
	// Add smooth scrolling to all links
	console.log('loaded');
	$("a").on('click', function(event) {
  	  // Make sure this.hash has a value before overriding default behavior
	  if (this.hash !== "") {
		let offset = 0;
		// Offset scroll on small screens so that category names are not covered
		if ($(document).width() < 991 || $(window).height() < 500) {
			offset = 70;
		}
		// Prevent default anchor click behavior
		event.preventDefault();
  
		// Store hash
		var hash = this.hash;
  
		// Using jQuery's animate() method to add smooth page scroll
		// The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
		$('html, body').animate({
		  scrollTop: $(hash).offset().top - offset
		}, 700, function(){
	 
			//	Enabling the following line will add the category id to the url, 
			//	but it will trigger a refresh which will undo the offset (will block the category name on mobile)
			//	window.location.hash = hash;
		});
	  } // End if
	});
});