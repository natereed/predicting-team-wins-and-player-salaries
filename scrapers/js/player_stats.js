function retrievePage(url, statsType) {

  var scrapeCareerStats = function(page) {
    return page.evaluate(function() {
      var stats = [];
      var headers = $("#careerStats table thead tr th");
      var rows = $("#careerStats table tbody tr");

      headers = headers.map(function() {return $.trim(this.textContent);}).get();

      for (var i=0; i<rows.length; i++) {
        var cells = rows[i].getElementsByTagName("td");
        var d = {};
        for (var j=0; j<cells.length; j++) {
          d[headers[j]] = $.trim(cells[j].textContent);
        }
        stats.push(d);
      }
      return stats;
    });
  };

  var scrapeCareerAdvancedStats1 = function(page) {
    return page.evaluate(function() {
      var stats = [];
      var headers = $("#careerAdvancedStats1 table thead tr th");
      var rows = $("#careerAdvancedStats1 table tbody tr");

      if (!headers || !rows) {
        return stats;
      }

      headers = headers.map(function() {return $.trim(this.textContent);}).get();

      for (var i=0; i<rows.length; i++) {
        var cells = rows[i].getElementsByTagName("td");
        var d = {};
        for (var j=0; j<cells.length; j++) {
          d[headers[j]] = $.trim(cells[j].textContent);
        }
        stats.push(d);
      }
      return stats;
    });
  };

  var scrapeCareerAdvancedStats2 = function(page) {
    return page.evaluate(function() {
      var stats = [];
      var headers = $("#careerAdvancedStats2 table thead tr th");
      var rows = $("#careerAdvancedStats2 table tbody tr");

      if (!headers || !rows) {
        return stats;
      }

      headers = headers.map(function() {return $.trim(this.textContent);}).get();

      for (var i=0; i<rows.length; i++) {
        var cells = rows[i].getElementsByTagName("td");
        var d = {};
        for (var j=0; j<cells.length; j++) {
          d[headers[j]] = $.trim(cells[j].textContent);
        }
        stats.push(d);
      }
      return stats;
    });
  };

  var redirectURL = null;
  var page = require('webpage').create();
  page.settings.loadImages = false;

  page.viewportSize = { width: 1024, height: 2400 };
  //the clipRect is the portion of the page you are taking a screenshot of
  page.clipRect = { top: 0, left: 0, width: 1024, height: 2400 };

  page.onError = function (msg, trace) {
    console.log(msg);
    trace.forEach(function(item) {
      console.log('  ', item.file, ':', item.line);
    });
  };

  page.onResourceReceived = function(resource) {
    if (url == resource.url && resource.redirectURL) {
      console.log("Redirect detected...");
      redirectURL = resource.redirectURL;
    }
  };

  // Uncomment this to be able to see console.log messages from page:
  page.onConsoleMessage = function(msg) {
    console.log(msg);
  }

  var handleHappyPath = function(page, statsType) {
    console.log("handleHappyPath");
    console.log("stats type : " + statsType);

    var waitFor = function(testFx, onReady, timeOutMillis) {
        var maxtimeOutMillis = timeOutMillis ? timeOutMillis : 6000, //< Default Max Timout is 3s
          start = new Date().getTime(),
          condition = false,
          interval = setInterval(function() {
              if ( (new Date().getTime() - start < maxtimeOutMillis) && !condition ) {
                  // If not time-out yet and condition not yet fulfilled
                  //console.log("condition? " + condition)
                  condition = (typeof(testFx) === "string" ? eval(testFx) : testFx()); //< defensive code
              } else {
                  if(!condition) {
                      // If condition still not fulfilled (timeout but condition is 'false')
                      page.render("stats-debug.png");
                      console.log("'waitFor()' timeout");
                      phantom.exit(1);
                  } else {
                      // Condition fulfilled (timeout and/or condition is 'true')
                      //console.log("'waitFor()' finished in " + (new Date().getTime() - start) + "ms.");
                      typeof(onReady) === "string" ? eval(onReady) : onReady(); //< Do what it's supposed to do once the condition is fulfilled
                      clearInterval(interval); //< Stop this interval
                  }
              }
          }, 250); //< repeat check every 250ms
      };

    waitFor(function() {
        return page.evaluate(function(statsType) {
                 var statsNav = $("#stat_type_nav button#stats_nav_type_" + statsType);
                 var mlbButton = $("button#level_mlb");

                 if (statsNav && statsNav.length > 0 && mlbButton && mlbButton.length > 0) {
                   return true;
                 }
               }, statsType);
              }, function() {
                   page.evaluate(function(statsType) {
                     var statsNav = $("#stat_type_nav button#stats_nav_type_" + statsType);
                     statsNav[0].click();
                     var mlbButton = $("button#level_mlb")[0];
                     mlbButton.click();
                   }, statsType);
               });

    // Scrape career stats and exit
    waitFor(function() {
        var condition = page.evaluate(function(statsType) {
          if ($(".status-message").css('display') != "none") {
              return false;
          }
          var titleStats = $(".title-stats");
          if (!titleStats || titleStats.length < 1 || !titleStats[0].textContent) {
            return false;
          }

          // Check the table
          rows = $("#careerStats table tbody tr")
          return titleStats[0].textContent.search(new RegExp(statsType + " stats", "i")) != -1 && rows && rows.length > 0;
        }, statsType);
        return condition;
        }, function() {
             setTimeout(function() {
               stats = {};
               var careerStats = scrapeCareerStats(page);
               stats['career'] = careerStats;

               if (statsType == 'pitching' || statsType == 'batting') {
                 var advancedCareerStats1 = scrapeCareerAdvancedStats1(page);
                 stats['advancedCareerStats1'] = advancedCareerStats1;
               }

               if (statsType == 'pitching') {
                 var advancedCareerStats2 = scrapeCareerAdvancedStats2(page);
                 stats['advancedCareerStats2'] = advancedCareerStats2;
               }

               console.log(JSON.stringify(stats));
               phantom.exit();
             }, 1000);
           });

  };
  // End nested function declarations

  // Open specified url, handle based on status
  page.open(url, function(status) {
    if (redirectURL) {
      retrievePage(redirectURL, statsType);
    }
    else if (status !== "success") {
      console.log("Unable to access network");
      phantom.exit();
    }
    else {
      console.log("statsType: " + statsType);
      handleHappyPath(page, statsType);
    }
  });

};

var system = require('system');
var args = system.args;

if (args.length < 3) {
  console.log('No args specified. Please specify url and type of sortable stats to scrape (pitching, batting, fielding).');
  phantom.exit();
}

var url = args[1];
var statsType = args[2];
console.log("url : " + url);
console.log("statsType: " + statsType);
retrievePage(url, statsType);
