var curSection     = 0;
const sectionNames  = ["aboutus-main", "aboutus-divisions", "aboutus-members"]

switchSection = (id) => {
  $(`#btn-${sectionNames[curSection]}`).toggleClass("active");
  $(`#btn-${sectionNames[id]}`).toggleClass("active");

  $("#aboutus-content").animate({ opacity: 0 }, "slow");
  $("#aboutus-content").promise().then(() => {
    $(`#${sectionNames[curSection]}`).toggleClass("d-none")
    $(`#${sectionNames[id]}`).toggleClass("d-none")
    curSection   = id; 
    $("#aboutus-content").animate({ opacity: 1}, "slow");
  })
};

$(document).ready(() => {
  url = new URL(window.location.href);
  if (url.searchParams.get("section") != null) {
    query_section = url.searchParams.get("section")
    if(sectionNames.includes(query_section)) {
      curSection = sectionNames.indexOf(query_section)
    }
  }
  $(`#btn-${sectionNames[curSection]}`).toggleClass("active");
  $(`#${sectionNames[curSection]}`).toggleClass("d-none")
});