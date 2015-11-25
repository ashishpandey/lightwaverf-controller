var Alarm = function (data) {
  var $alarm = $($.Mustache.render('alarm', {num: data.num}));

  if (typeof data.brightness !== "undefined") {
    $alarm.find("[name='brightness']").attr("value", data.brightness); 
  }
    // for some reason val(x) doesn't work here !
  if (typeof data.enabled !== "undefined")  {
    $alarm.find("[name='enabled']").val(data.enabled);
  }
  if (typeof data.hour !== "undefined")  { 
    $alarm.find("[name='hour']").val(data.hour);
  }
  if (typeof data.min !== "undefined")  {
    $alarm.find("[name='min']").val(data.min);
  }

  if (typeof data.days !== "undefined") {
    data.days.forEach(function (day) {
      $alarm.find("[name='days'][value='" + day + "']").prop("checked", "checked");
    });
  }


  $alarm.find(".alarm-delete").click(function () {
    $alarm.trigger("delete");
  });
  $alarm.serialise = function () {
    var $this = $(this);
    var output = {};
    output.enabled = $this.find("select[name='enabled']").val();
    output.brightness = $this.find("input[name='brightness']").val();
    output.hour = $this.find("select[name='hour']").val();
    output.min = $this.find("select[name='min']").val();
    output.days = $this.find("input:checkbox[name='days']:checked").map(function () {
      return $(this).val();
    }).get();
    return output;
  }

  

  return $alarm;
}

$(document).onPage("show", "#alarms", function () {
  var endpoint = "api/schedules";
  alarms = [];
  serialisedData = [];

  var $el = $('#alarms');
  var $alarmsList = $el.find("#alarms-list");
  var $globalEnabled = $el.find("#global-enabled");
  $globalEnabled.off("change");
  $globalEnabled.change(function () {
    postUpdate();
  });


  $.get(endpoint).done(function (config) {
    config.schedules.forEach(function (data, index) {
      data.num = index;
      var $alarm = Alarm(data);
      bindEventHandlers($alarm);
      $alarmsList.append($alarm);
      $alarm.trigger("create");
      alarms.push($alarm);
    });

    $globalEnabled.val(config.globalEnabled);
    $globalEnabled.slider("refresh");

  });


  var bindEventHandlers = function ($alarm) {
    $alarm.find(".form-item").change(function () {
      postUpdate();
    });

    $alarm.find(".slider-item").on("slidestop", function () {
      postUpdate();
    });
    
    $alarm.on("delete", function (alarm) {
      alarms.forEach(function ($item, index) {
        if ($item[0] === alarm.target) { // we need $item[0] because $item is the jQ wrapper.  I think jQ does something odd with the $alarm.trigger() where the event target is the DOM element or something
          console.log("deleting..." + $item);
          alarms.splice(index, 1);
          $item.remove(); 	// remove from DOM
        }
      })
      postUpdate();
    });
  }

  var postUpdate = function () {
    serialisedData = [];
    alarms.forEach(function ($item, index) {
      serialisedData.push($item.serialise());
    });
    $.ajax({
      url: endpoint,
      type: "POST",
      contentType: 'application/json',
      data: JSON.stringify({globalEnabled: $globalEnabled.val(), schedules: serialisedData})
    });
  }



  $("#add-alarm").click(function () {
    var $alarm = Alarm({num: alarms.length});
    $alarmsList.append($alarm);
    $alarm.trigger("create");
    bindEventHandlers($alarm);
    alarms.push($alarm);
  });




});