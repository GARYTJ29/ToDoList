$("#date-time-picker").calendar();
$("#datetime").click(function () {
  $("#date-time-picker").toggle();
});
$("#repeats").click(function () {
  $("#select-days").toggle();
});
$("#hasPriority").click(function () {
  $("#select-priority").toggle();
});
$(".tag .ui.dropdown").dropdown({
  allowAdditions: true,
});
$("select.dropdown").dropdown("set selected");
