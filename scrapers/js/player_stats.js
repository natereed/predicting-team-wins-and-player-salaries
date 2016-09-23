function retrievePage(url) {

  var scrapePitching = function(page) {
    //page.render("pitching-stats-debug.png");
    console.log("Scraping pitching...");
    //        console.log(page);

    return page.evaluate(function() {
            var stats = [];

            var headers = $("#careerStats table thead tr th");
            var rows = $("#careerStats table tbody tr");

            headers = headers.map(function() {return $.trim(this.textContent);}).get();

            for (var i=0; i<rows.length; i++) {
              console.log(i);
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

  var scrapeAdvancedPitching1 = function(page) {
    return page.evaluate(function() {
      var stats = [];
      var headers = $("#careerAdvancedStats1 table thead tr th");
      var rows = $("#careerAdvancedStats1 table tbody tr");

      if (!headers || !rows) {
        return stats;
      }

      headers = headers.map(function() {return $.trim(this.textContent);}).get();

      for (var i=0; i<rows.length; i++) {
        console.log(i);
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

  var scrapeAdvancedPitching2 = function(page) {
    return page.evaluate(function() {
      var stats = [];
      var headers = $("#careerAdvancedStats2 table thead tr th");
      var rows = $("#careerAdvancedStats2 table tbody tr");

      if (!headers || !rows) {
        return stats;
      }

      headers = headers.map(function() {return $.trim(this.textContent);}).get();

      for (var i=0; i<rows.length; i++) {
        console.log(i);
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

  console.log("Retrieving page...");
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

  var handleHappyPath = function(page) {
    var waitFor = function(testFx, onReady, timeOutMillis) {
        console.log("Waiting for...");
        var maxtimeOutMillis = timeOutMillis ? timeOutMillis : 6000, //< Default Max Timout is 3s
          start = new Date().getTime(),
          condition = false,
          interval = setInterval(function() {
              if ( (new Date().getTime() - start < maxtimeOutMillis) && !condition ) {
                  // If not time-out yet and condition not yet fulfilled
                  console.log("condition? " + condition)
                  condition = (typeof(testFx) === "string" ? eval(testFx) : testFx()); //< defensive code
              } else {
                  if(!condition) {
                      // If condition still not fulfilled (timeout but condition is 'false')
                      //page.render("stats.png");
                      console.log("'waitFor()' timeout");
                      phantom.exit(1);
                  } else {
                      // Condition fulfilled (timeout and/or condition is 'true')
                      console.log("'waitFor()' finished in " + (new Date().getTime() - start) + "ms.");
                      typeof(onReady) === "string" ? eval(onReady) : onReady(); //< Do what it's supposed to do once the condition is fulfilled
                      clearInterval(interval); //< Stop this interval
                  }
              }
          }, 250); //< repeat check every 250ms
      };

    console.log("Clicking...");

    // Scrape pitching
    // Click on "Pitching" once it appears
    waitFor(function() {
        return page.evaluate(function() {
                 if ($("#stat_type_nav button#stats_nav_type_pitching")) {
                   return true;
                 }
               });
              }, function() {
                   var clicked = page.evaluate(function() {
                     var pitchingNav = $("#stat_type_nav button#stats_nav_type_pitching");
                     if (pitchingNav && pitchingNav.length > 0) {
                       //console.log("Clicking Pitching nav button");
                       pitchingNav[0].click();
                       return true;
                     }
                     else {
                       return false;
                     }
                   });
                   if (!clicked) {
                     console.log("Pitching NAV not found!!! Aborting...")
                     phantom.exit();
                   }
               });

    // Scrape pitching and exit
    waitFor(function() {
        var condition = page.evaluate(function() {
          console.log("Checking for title");
          var titleStats = $(".title-stats");
          if (!titleStats || titleStats.length < 1 || !titleStats[0].textContent) {
            return false;
          }
          console.log("Checking for table...");
          // Check the table
          rows = $("#careerStats table tbody tr")
          return titleStats[0].textContent.search(/Pitching Stats/) != -1 && rows && rows.length > 0;
        });
        console.log("Ready? " + condition);
        return condition;
        }, function() {
             console.log("onReady function");
             setTimeout(function() {
               console.log("Found page elements - ready to scrape...");
               var pitchingStats = scrapePitching(page);
               var advancedPitchingStats1 = scrapeAdvancedPitching1(page);
               var advancedPitchingStats2 = scrapeAdvancedPitching2(page);
               stats = {};
               stats['pitching'] = pitchingStats;
               stats['advancedPitching1'] = advancedPitchingStats1;
               stats['advancedPitching2'] = advancedPitchingStats2;
               console.log(JSON.stringify(stats));
               console.log("Done");
               phantom.exit();
             }, 1000);
           });

/**
    console.log("Waiting a few seconds...");
    // Old approach: just scrape the page without waiting. Probably want to wait until the stats appear:
    setTimeout(function() {
      console.log("Executing");
      var stats = scrapePitching(page);
      console.log(JSON.stringify(stats))
      phantom.exit();
    }, 5000);
**/

  };
  // End nested function declarations

  // Open specified url, handle based on status
  page.open(url, function(status) {
    console.log(status);
    if (redirectURL) {
      console.log("Redirecting...");
      retrievePage(redirectURL);
    }
    else if (status !== "success") {
      console.log("Unable to access network");
      phantom.exit();
    }
    else {
      handleHappyPath(page);
    }
  });

};

var system = require('system');
var args = system.args;

if (args.length === 1) {
  console.log('No args specified. Please specify url of sortable stats.');
  phantom.exit();
}

var url = args[1];
retrievePage(url);
