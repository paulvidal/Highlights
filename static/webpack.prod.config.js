var path = require("path");
var webpack = require('webpack');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

var UglifyJsPlugin = require('uglifyjs-webpack-plugin');
var OptimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');

var config = require('./webpack.base.config.js');

// PRODUCTION
config.mode = 'production';

// Give distribution path
config.output.path = path.resolve('./dist');

config.plugins = config.plugins.concat([
  new ExtractTextPlugin('[name].css'),

  // Removes a lot of debugging code in React
  new webpack.DefinePlugin({
    'process.env': {
      'NODE_ENV': JSON.stringify('production')
  }}),

  // Keeps hashes consistent between compilations
  new webpack.optimize.OccurrenceOrderPlugin(),
]);

// Minifies the code
config.optimization = {
  minimizer: [
    new UglifyJsPlugin({}),
    new OptimizeCssAssetsPlugin({})
  ]
};

// Add a loader for JS files with react-hot enabled
config.module.rules.push(
  {
    test: /\.js$/,
    exclude: /node_modules/,
    loader: 'babel-loader',
  }
);

module.exports = config;