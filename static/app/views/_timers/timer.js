define([
  "text!../../templates/_timers/timer.tpl.html",
  "../../models/timer"
], function (timer_template, Timer_Model) {

  return Backbone.View.extend({
    
    events: {
      "click .alarm-delete" : function() {
        this.remove();
        this.trigger("delete");
      }
    },
    
    initialize: function (data) {
      var that = this;
      _.extend(this, Backbone.Events); // Used to signal to parent view
      this.modelBinder = new  Backbone.ModelBinder();
      this.model = new Timer_Model(data);
      this.model.set("enabled","on");
      this.model.on("change", function() {
        that.trigger("change");
      });
    },
    
    
    serialise: function () {
      return this.model.serialise();
    },
    
    render: function () {
      var template = Handlebars.compile(timer_template);
      this.$el.html(template()); 
      this.$el.enhanceWithin();   // Enhance with jqm

      this.modelBinder.bind(this.model, this.el);
      
      // Update the widgets now we have bound them to the model values
      this.$el.find("input[data-type='range']").slider("refresh");    
      this.$el.find("input[type='checkbox']").checkboxradio("refresh");
      // We need to scope the "select" to not include the on/off slider.  
      // That is a html "select" but gets enhanced as a slider switch
      this.$el.find(".time select").selectmenu("refresh");
      
      return this;
    },
    
  });
});