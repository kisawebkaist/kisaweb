var headerName  = ["main", "member", "division", "gallery"]
var curHeader   = 0;
for(let i = 1; i < headerName.length; i++) document.getElementById(headerName[i]).style.display = "none"
document.getElementById(`btn-${headerName[curHeader]}`).style["background-color"]   = "var(--gray-dark)"
function switchHeader(id){
  var curElem = document.getElementById(headerName[curHeader])
  curElem.style.display  = "none"
  curElem = document.getElementById(`btn-${headerName[curHeader]}`)
  curElem.style["background-color"] = "var(--secondary)"
  var newElem = document.getElementById(headerName[id])
  newElem.style.display  = "flex"
  newElem = document.getElementById(`btn-${headerName[id]}`)
  newElem.style["background-color"] = "var(--dark)"
  curHeader   = id;
}