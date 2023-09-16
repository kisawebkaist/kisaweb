$(document).ready(function()
    {
    var players = []
    var stopVideo = function ( element ) {
		var iframeSrc = element.src;
		element.src = iframeSrc;
    };
    var allMovieIframes = document.getElementById("carousel-video").getElementsByTagName('iframe');
    for (currentIFrame of allMovieIframes)
    {
        players.push(currentIFrame);
    }
    $('#carousel-video').on('slide.bs.carousel', function(event) {
        stopVideo(players[event.from])
    })
});
