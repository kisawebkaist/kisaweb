var headerName  = ["main", "member", "division"]
var curHeader   = 0;

for(let i = 1; i < headerName.length; i++) {
  document.getElementById(headerName[i]).style.display = "none"
}

function switchHeader(id){
  
  document.getElementById(`btn-${headerName[curHeader]}`).classList.toggle("active")
  document.getElementById(`btn-${headerName[id]}`).classList.toggle("active")

  var curElem = document.getElementById(headerName[curHeader])
  var newElem = document.getElementById(headerName[id])

  $(".aboutus-content").animate({ opacity: 0 }, "slow");
  $(".aboutus-content").promise().then(() => {
    curElem.style.display = "none";
    newElem.style.display = "flex";
    curHeader   = id; 
    $(".aboutus-content").animate({ opacity: 1}, "slow");
  })

}