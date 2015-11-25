require.config({
  paths: {
    text: "../libs/require/text" // RequireJS "text!" plugin for templates
  }
});


require(["router"], function(Router) {
  
  this.router = new Router();
});