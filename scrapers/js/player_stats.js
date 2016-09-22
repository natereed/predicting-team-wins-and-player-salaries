function retrievePage(url) {

  function scrapePage() {
    console.log("Scraping page...");
    console.log(page);

    var stats = page.evaluate(function() {
      // Declare helpers
      var scrapeTable = function(headers, rows) {
        console.log("Scraping table...");
        var stats = [];
        var header_names = [];
        for (var i=0; i<headers.length; i++) {
          header_names.push($.trim(headers[i].textContent));
        }

        for (var i=0; i<rows.length; i++) {
          var cells = rows[i].getElementsByTagName("td");
          stat = {}
          for (var j=0; j<cells.length; j++) {
            stat[header_names[j]] = $.trim(cells[j].textContent);
            console.log(header_names[j] + ": " + cells[j].textContent);
          }
          stats.push(stat);
        }
        console.log("Got stats...");
        return stats;
      };

      var scrapePitching = function() {
        //console.log("Scraping pitching...");
        var headers = $("#careerStats table thead tr th");
        var rows = $("#careerStats table tbody tr");
        var stats = {};
        stats['pitching'] = scrapeTable(headers, rows);

        var headers = $("#careerAdvancedStats1 table thead tr th");
        var rows = $("#careerAdvancedStats1 table tbody tr");
        stats['advanced_pitching1'] = scrapeTable(headers, rows);
        console.log(stats);
        console.log("Done");

        var headers = $("#careerAdvancedStats2 table thead tr th");
        var rows = $("#careerAdvancedStats2 table tbody tr");
        stats['advanced_pitching2'] = scrapeTable(headers, rows);
        console.log(stats);
        console.log("Done");
        return stats;
      };

      // End helper declarations
      //console.log("About to scrape, yo!");
      var pitchingNav = $("#stats_nav_type_pitching");
      if (pitchingNav && pitchingNav.length > 0) {
        //console.log("Clicking Pitching nav button");
        pitchingNav[0].click();
      } else {
        //console.log("Pitching NAV not found!!! Aborting...")
        phantom.exit();
      }
      return scrapePitching();
    });

    console.log(JSON.stringify(stats))
    // End of scraping
    phantom.exit();
  };

  console.log("Retrieving page...");

  var redirectURL = null;

  var page = require('webpage').create();
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

  page.open(url, function(status) {
    console.log(status);
    if (redirectURL) {
      console.log("Redirecting...");
      retrievePage(redirectURL);
    }
    else if (status !== "success") {
      console.log("Unable to access network");
      phantom.exit();
    } else {

      var waitFor = function(testFx, onReady, timeOutMillis) {
        console.log("Waiting...");
        var maxtimeOutMillis = timeOutMillis ? timeOutMillis : 6000, //< Default Max Timout is 3s
          start = new Date().getTime(),
          condition = false,
          interval = setInterval(function() {
              if ( (new Date().getTime() - start < maxtimeOutMillis) && !condition ) {
                  // If not time-out yet and condition not yet fulfilled
                  condition = (typeof(testFx) === "string" ? eval(testFx) : testFx()); //< defensive code
              } else {
                  if(!condition) {
                      // If condition still not fulfilled (timeout but condition is 'false')
                      page.render("stats.png");
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

      console.log("Waiting...");
      waitFor(function() {
                return page.evaluate(function() {
                  return true;
                });
                return true;
              }, function() { setTimeout(scrapePage, 2000); });
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
