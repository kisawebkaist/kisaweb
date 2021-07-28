var headerName  = ["main", "member", "division", "gallery"]
var curHeader   = 0;
for(let i = 1; i < headerName.length; i++) document.getElementById(headerName[i]).style.display = "none"

function switchHeader(id){
  document.getElementById(headerName[curHeader]).style.display  = "none"
  document.getElementById(headerName[id]).style.display         = "flex"
  curHeader   = id;
}