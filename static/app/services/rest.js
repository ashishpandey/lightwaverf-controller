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
    
    get_timers : function() {
      return json;
    },
    
    load_timers : function() {
      return load("schedules").done(function(data) {
        json = data;
      });
    
    },
    save_timers : function(data  ) {
      this.json = data;
      return save("schedules", JSON.stringify(data));
    },
    
    load_brightness : function(room) {
      return load("panel/" + room);
    },
    
    save_brightness : function(room, value) {
      return save("panel/" + room,  value);
    }
    
    
  }
  
})