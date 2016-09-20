var system = require('system');
var args = system.args;

if (args.length === 1) {
  console.log('No args specified. Please specify url of sortable stats.');
  phantom.exit();
}

var url = args[1];

var quote = function(value) {
  return('"' + value + '"');
};

var print_row = function(row, colNames) {
  var values = [];
  for (var i = 0; i < colNames.length; i++) {
      values.push(quote(row[colNames[i]]));
  }
  console.log(values.join());
};

var print_header_row = function(colNames, displayNames) {
  names = colNames.map(function(name) {
    return displayNames[name] || name;
  });
  console.log(names.map(quote).join());
};

var write_csv = function(stats) {
  print_header_row(stats['colNames'], stats['displayNames']);
  for (var i=0; i < stats['data'].length; i++) {
    row = stats['data'][i];
    print_row(row, stats['colNames']);
  }
};

var page = require('webpage').create();
page.onError = function (msg, trace) {
    console.log(msg);
    trace.forEach(function(item) {
        console.log('  ', item.file, ':', item.line);
    });
};

page.open(url, function(status) {
  var stats = page.evaluate(function() {

    var extractColumnName = function(className) {
      colname = className;
      matches = /^dg-(\w+).*$/.exec(colname);
      if (matches.length > 1) {
        colname = matches[1];
      }
      return colname;
    };

    var data = [];
    //console.log("page.evaluate()...");
    var rows = document.getElementsByClassName("stats_table")[0].getElementsByTagName("tr");

    // header row
    var colNames = [];
    var displayNames = {};

    // Store column, display names
    for (var i=0; i<rows[0].children.length; i++) {
      var child = rows[0].children[i];
      var colname = extractColumnName(child.className);
      colNames.push(colname);
      displayName = child.textContent;
      if (displayName) {
        displayNames[colname] = displayName;
      }
    }

    // Store data
    for (var i=1; i<rows.length; i++) {
      var row = rows[i];
      var rowData = {}
      for (var j=0; j<row.children.length; j++) {
        cell = row.children[j];
        //        console.log(cell.className + ": " + cell.textContent)
        rowData[extractColumnName(cell.className)] = cell.textContent
      }
      data.push(rowData);
    }

    return {'colNames' : colNames,
            'displayNames' : displayNames,
            'data' : data};
  });

  write_csv(stats);
  phantom.exit();
});