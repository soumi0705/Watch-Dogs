function toggle_(id) {
  var svg = document.getElementById(id);
  var change;
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
  console.log(id);
  console.log(typeof id);
  console.log(bool);
  console.log(typeof bool);

  var svg = document.getElementById(id);
  if (bool == "true") var change = id.includes("light") ? "yellow" : "green";
  else var change = id.includes("light") ? "silver" : "red";
  return console.log((svg.style.fill = change));
}
