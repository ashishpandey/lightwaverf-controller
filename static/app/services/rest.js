define([], function() {
  var URL = "./api/"
  var json;
  
  var load = function(endpoint) {
      return $.getJSON(URL + endpoint);
  }
  
  var save = function(endpoint, data) {
    return $.ajax({
        url: URL + endpoint, 
        type: 'POST', 
        contentType: 'application/json', 
        data: data
      }) 
  }
  
  return {
    
    load_brightness : function() {
      return load("dimmer/1");
    },
    
    save_brightness : function(value) {
      return save("dimmer/1",  value);
    }
    
    
  }
  
})