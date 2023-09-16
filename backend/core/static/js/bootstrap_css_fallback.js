
var test = document.createElement("div")
test.className = "hidden d-none"

document.head.appendChild(test)
var cssLoaded = window.getComputedStyle(test).display === "none"
document.head.removeChild(test)

if (!cssLoaded) {
    var link = document.createElement("link");

    link.type = `text/css`;
    link.rel = `stylesheet`;
    link.href = `static/bootstrap/css/bootstrap.min.css`;

    document.head.appendChild(link);
}
