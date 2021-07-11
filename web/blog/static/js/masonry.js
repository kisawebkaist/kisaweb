$('.grid').masonry({
	itemSelector: '.grid-item',
/*	columnWidth: 0, */ // removing in order to center stuff
	horizontalOrder: true, // Orders the posts from left to right
	fitWidth: true, // In order to center all of the items, rather than aligning them leftward
	// other options can be added here for further customizations, refer: https://masonry.desandro.com/options.html
  });