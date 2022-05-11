function toggle_(id) {
  console.log(id.includes("light"));
  var svg = document.getElementById(id);
  var change;
  console.log(svg.style.fill);
  if (id.includes("light"))
    change = svg.style.fill == "yellow" ? "silver" : "yellow";
  else change = svg.style.fill == "red" ? "green" : "red";
  return console.log((svg.style.fill = change)); 
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
  return console.log((svg.style.fill = change)); 
}
