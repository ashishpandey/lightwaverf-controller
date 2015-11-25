define([
  "text!../templates/timers.tpl.html", 
  "./_timers/timer",
  "../services/rest"
], function(timers_template, Timer_View, rest_service) {

  return Backbone.View.extend({
    timers: null,
    
    
    events: {
      "click #add-timer" : function() {
        this.add_timer();
      },
      "slidestop #global-enabled" : "save"
     
    },

    initialize : function() {
      this.timers = [];
    },
  
    add_timer: function(data) {
      var that = this;
      var timer = new Timer_View(data);

      // Listen to the timer view for it trigger it should be removed
      // from the list, caused if someone presses the delete button
      timer.on("delete", function() {
        // Remove the timer from the list
        that.timers.forEach(function(entry, index) {
          if (entry === this ) {
            that.timers.splice(index, 1);
          }
        }, this)
        that.save();
      });

      timer.on("change", this.save, this);

      timer.render();
      this.$el.find("#timers-list").append(timer.$el);
      this.timers.push(timer);
    },
   
   save: function() {
    var data = {
      timers: [],
      global_enabled: this.$el.find("#global-enabled").val()
    }

      _.each(this.timers, function(timer) {
        data.timers.push(timer.serialise());
      })
      rest_service.save_timers(data);
   },
   
    render: function() {
      var that = this;
      var template = Handlebars.compile(timers_template);
      this.$el.html(template());
      var json = rest_service.get_timers();
      this.$el.find("#global-enabled").val(json.global_enabled);
      _.each(json.timers, function(timer){
         that.add_timer(timer);
      });

     
      return this;
    }

  });
});