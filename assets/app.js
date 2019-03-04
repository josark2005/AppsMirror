window.onload = function() {
  resize();
}
window.onresize = function() {
  resize();
}
function resize() {
  let height_offset = -40
  let win_height = document.body.offsetHeight;
  let header_height = document.getElementById('header').offsetHeight;
  let footer_height = document.getElementById('footer').offsetHeight;
  console.log(win_height - header_height - footer_height + "px")
  document.getElementById('container').style.minHeight = win_height - header_height - footer_height + height_offset + "px";
}
