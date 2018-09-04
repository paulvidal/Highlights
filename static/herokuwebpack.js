var fs = require('fs');
var info = JSON.parse(fs.readFileSync('webpack-stats-prod.json', 'utf8'));
var path = require("path");

var currentDir = path.resolve(".");

for (var chunk in info.chunks) {
  for (var name in info.chunks[chunk]) {
    name = info.chunks[chunk][name]

    name.path = name.path.replace(currentDir, '~/static')
  }
}

// rewrite to file
fs.writeFile('webpack-stats-prod.json', JSON.stringify(info), function(err) {
    if(err) {
        return console.log(err);
    }

    console.log("File 'webpack-stats-prod.json' was saved!");
});