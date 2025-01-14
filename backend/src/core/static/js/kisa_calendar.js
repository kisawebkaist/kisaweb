$('.calendar-button-load').click(() => {
    let src = 'https://calendar.google.com/calendar/embed?height=500&wkst=1&bgcolor=%23ffffff&ctz=Asia%2FSeoul&src=cnMxOGo0MThxZG1mc2w5cGY4NmI3cTk4OWtAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&color=%23F6BF26';
    if ($(window).width() < 600) {
      src = 'https://calendar.google.com/calendar/embed?height=500&mode=AGENDA&wkst=1&bgcolor=%23ffffff&ctz=Asia%2FSeoul&src=cnMxOGo0MThxZG1mc2w5cGY4NmI3cTk4OWtAZ3JvdXAuY2FsZW5kYXIuZ29vZ2xlLmNvbQ&color=%23F6BF26'
    };
    $('<iframe>', {
      src: src,
      id:  'kisa-google-calendar',
      frameborder: 0,
      width: "100%",
      height: "500",
      scrolling: 'no'
      }).appendTo('#kisa-google-calendar-container');
      $('.calendar-button-load').remove();
    //   $('.calendar-button-toggle').toggle();
  });
// $('.calendar-button-toggle').click(() => {
// 	$("#kisa-google-calendar").toggle( );
// })