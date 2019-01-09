var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

var config = require('./webpack.base.config.js');

// DEVELOPMENT
config.mode = 'development';

// Use webpack dev server
for (var name in config.entry) {
  config.entry[name] = config.entry[name].concat(['webpack-dev-server/client?http://localhost:3000', 'webpack/hot/only-dev-server'])
}

// Override django's STATIC_URL for webpack bundles
config.output.publicPath = 'http://localhost:3000/assets/bundles/';

// Simplify name of generated file
config.output.filename = '[name].js';

// Add HotModuleReplacementPlugin and BundleTracker plugins
config.plugins = config.plugins.concat([
  new webpack.NoEmitOnErrorsPlugin(), // don't reload if there is an error
  new webpack.HotModuleReplacementPlugin({}),
  new webpack.NamedModulesPlugin(),
  new ExtractTextPlugin('[name].css')
]);

// Add a loader for JS files with react-hot enabled
config.module.rules.push(
  {
    test: /\.js$/,
    exclude: /node_modules/,
    loader: 'babel-loader',
    options: {
      // This is a feature of `babel-loader` for webpack (not Babel itself).
      // It enables caching results in ./node_modules/.cache/babel-loader/
      // directory for faster rebuilds.
      cacheDirectory: true,
      plugins: ['react-hot-loader/babel'],
    },
  },
);

module.exports = config;