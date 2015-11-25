$(document).onPage("show", "#index", function () {

  var endpoint = "api/panel/bedroom";
  var alarmEndpoint = "api/schedules";

  $.get(alarmEndpoint, function (data) {
    var enabledSchedules = 0;
    data.schedules.forEach(function (schedule) {
      if (schedule.enabled == "on")
        enabledSchedules++;
    });

    if (enabledSchedules > 0 && data.globalEnabled == "on") {
      $("#alarm-btn").addClass("warning");
    } else {
      $("#alarm-btn").removeClass("warning");
    }
  });

  function refreshSlider() {
    $.get(endpoint).done(function (data) {
      data = data.trim();
      console.log(data);
      $("#slider").val(data);
      $("#slider").slider("refresh");

      $("button").each(function (index, button) {
        if ($(button).val() == data) {
          $(button).addClass("ui-btn-active");
        } else {
          $(button).removeClass("ui-btn-active");
        }
      });
    });
  }


  refreshSlider();
  $("#slider").off("slidestop");	// This runs every pageshow (not create), so make sure not to bind multiple times
  $("#slider").on("slidestop", function (event, ui) {
    console.log($(this).val());
    $.post(endpoint, {val: $(this).val()});
    refreshSlider();
  });
  $("button").off("click"); // This runs every pageshow (not create), so make sure not to bind multiple times
  $("button").click(function () {
    $.post(endpoint, {val: $(this).val()}).done(refreshSlider);
  });

});