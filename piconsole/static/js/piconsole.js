function piconsole_loadpage(app) {
  $('#piconsole-main').load(apps[app][1], function (response, status, xhr) {
    if (status == 'error') {
      var msg = 'Sorry, but there was an error: ' + xhr.status + ' ' + xhr.statusText;
      var p = $('<p class="bg-danger"></p>').text(msg);
      $('#piconsole-main').html(p);
    }
  });
}

(function($) {
  $(window).hashchange(function(){
    var hash = location.hash.substr(1);
    for (var app in apps) {
      if (apps[app][0] == hash) {
        piconsole_loadpage(app);
      }
    }
  });
  if (location.hash) {
    $(window).hashchange();
  } else {
    location.hash = apps[0][0];
    $(window).hashchange();
  }
})(jQuery);