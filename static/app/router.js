define(["text!templates/error.tpl.html"], function(error_template) {

  return Backbone.Router.extend({
    initialize: function() {
      try {
         Backbone.history.start();    // Tells Backbone to start watching for hashchange events
      } catch (error) {
        this.handle_error(error);
      }
    },

    change_page: function(View, action, params) {
//      try {

        // Remove any global error messages - otherwise they stay in the body and are visible during transistions
        $("#global-error").remove();

        // Remove any "pageinit" events a previous view may have registered.
        $(document).off("pageinit");
        // Call remove() on the old view so it can clean up and remove any event bindings
        if (typeof (this.view) !== "undefined" && typeof (this.view.remove) === "function") {
          this.view.remove(); // Clean up the old view
        };

        var view = new View(params);  // The new page (view) we are moving to
        this.view = view; // Save it for future reference, so we can call remove() on it when pages change.

        view.$el.attr('data-role', 'page');

        // Call the specified action on the view - this needs to do something useful, like render itself
        // into it's $el property.
        view[action](params);

        // And add it to the global DOM
        $('body').append(view.$el);

        // Then manually fire jQM to change pages.
        // The old page is automataically removed from the DOM by the "pagehide" binding we set when the app was
        // initialized
        $.mobile.pageContainer.pagecontainer("change", view.$el, {changeHash: false, transition: $.mobile.defaultPageTransition});

//      } catch (error) {
//        this.handle_error(error);
//      }
    },
    // Backbone.js Routes
    routes: {
      "": "main_action",
      ":controller": "main_action",
      ":controller/:action": "main_action",
      ":controller/:action/*params": "main_action"
    },

    /**
     * Front controller method to handle view changes.
     * @param {String} view_name Name of the Backbone.View controller to change to.
     * @param {String} action Method on the controller to call
     * @param {Array} params Parameters to pass to the action
     * @returns {undefined}
     */
    main_action: function(view_name, action, params) {
      try {
        var that = this;


        // This follows the classic MVC pattern that maps a URL to: /controller/action/param1/param2
        // So it loads the file "controller", executes the "action" method, and passes it an array of params.
        // There is some URL rewriting, see below.

        // Controller ("View")
        if (typeof (view_name) === "undefined" || view_name === null)
          view_name = "index";
        // TODO(2) - default controller

        // Replace any hypens in the viewName with underscores so they map to the filesystem
        view_name = view_name.replace("-", "_");

        // Action
        if (typeof (action) === "undefined" || action === null) {
          this.action = "render";
        } else {
          // Convert any hypens to underscores, and append "_action" to the end, so they map to methods
          this.action = action.replace("-", "_") + "_action";

          // or camelCase instead....
          // this.action = action.replace(/-([a-z])/g, function (g) { return g[1].toUpperCase() }) + "Action";
        }

        // Params
        if (typeof (params) === "undefined" || params === null) {
          this.params = undefined;  //Reset this.params from any previous calls
        } else {
          this.params = params.split("/");
        }

        // Finally we load the view, and display it.
        require(["views/" + view_name], function(View) {
          that.change_page(View, that.action, that.params);
        });
//        , function() {
//          that.handle_error(new Error("Missing required file: " + view_name));
//        });
      } catch (error) {
        this.handle_error(error);
      }

    },
    handle_error: function(error) {
      // Show the error page with a message, stacktrace and option to clear all the local data.
      var template = Handlebars.compile(error_template);
      error.settings = JSON.stringify($.localStorage.get("settings"));
      error.surveys = JSON.stringify($.localStorage.get("surveys"));
      $('body').html(template(error));
      $("#clear-all-data").click(function() {
        if (confirm("DELETE ALL COMET DATA ON THIS DEVICE?")) {
          $.localStorage.removeAll();
          location.reload(true);
        }
      });
    }

  });

});