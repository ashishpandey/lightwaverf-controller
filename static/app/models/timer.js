define([], function () {
  return Backbone.DeepModel.extend({
   
    initialize: function (data) {
        this.data = this.unserialise(data);
    },
    
    serialise: function () {
      var days = _.compact(_.map(this.get("days"), function (value, day) {
        return value === true ? day : undefined
      }));
      var json = this.toJSON();
      json.days = days;
      console.log(JSON.stringify(json));
      return json;
    },

    unserialise: function (json) {
      var days = {};
      _.each(json.days, function (day) {
        days[day] = true;
      });
      json.days = days;
      this.attributes = json;
    }


  });
});

