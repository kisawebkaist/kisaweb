$('.grid').masonry({
	itemSelector: '.grid-item',
	columnWidth: 58, // Reducing will decrease the gap between the cards and vice-versa. Will also change the number of cards per row if the change is big.
	horizontalOrder: true // Orders the posts from left to right
	// other options can be added here for further customizations, refer: https://masonry.desandro.com/options.html
  });