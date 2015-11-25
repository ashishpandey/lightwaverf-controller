/**
 * Backbone.View that manages the display of the home page
 */
define([
  "text!../templates/index.tpl.html",
  "services/rest"
], function(home_template, rest_service) {

  return Backbone.View.extend({
    brightness: null,
    
    events: {
      "click #light-buttons button" : function(evt) {
        this.brightness = $(evt.target).val();
        this.save();
      },
      
      "change #light-slider": function(evt){
        var val = $(evt.target).val();
        // jqm appears to fire 00s of change events each time the slider moves!
        if (val !== this.brightness) {
          this.brightness = $(evt.target).val();
          this.save();
        }
      }
    
    },
    
    
    initialize: function() {
      var that = this;
      rest_service.load_timers().done(function(data) {
        var count = _.filter(data.timers, {enabled: "on"}).length;
        if (count > 0 && data.global_enabled === "on") {
          that.$el.find("#timer-btn").addClass("warning");
        }
      });
      rest_service.load_brightness("bedroom").done(function(data) {
        that.brightness = data;
        that.refresh_ui();
      });
    },
   
    refresh_ui: function () {
      var that = this;
      var $slider = this.$el.find("#light-slider");
      this.undelegateEvents();  //prevent another change event firing on the 
                                // slider, which causes an infinite loop
      $slider.val(this.brightness);
      $slider.slider("refresh");
      this.delegateEvents();

      this.$el.find("#light-buttons button").each(function (index, button) {
        var $button = $(button);
        if ($button.val() == that.brightness) {
          $button.addClass("ui-btn-active");
        } else {
          $button.removeClass("ui-btn-active");
        }
      });
    },
   
   save: function() {
     var that = this;
     rest_service.save_brightness("bedroom", this.brightness).done(function() {
       that.refresh_ui();
     });
   },
   
    render: function() {
      var template = Handlebars.compile(home_template);
      this.$el.html(template());
      return this;
    },

    remove: function() {
      
    }
    

  });
});