function toggle_(id) {
  var svg = document.getElementById(id);
  var change;
  if (id.includes("light"))
    change = svg.style.fill == "yellow" ? "silver" : "yellow";
  else change = svg.style.fill == "red" ? "green" : "red";
  return; 
}
jQuery(function ($) {
  $("#camera_bed")
    .click(function () {
      return false;
    })
    .dblclick(function () {
      window.location = "http://localhost:5001/";
      return false;
    });
});
function control(id, bool) {
  

  var svg = document.getElementById(id);
  if (bool == "true") var change = id.includes("light") ? "yellow" : "green";
  else var change = id.includes("light") ? "silver" : "red";
  return; 
}
