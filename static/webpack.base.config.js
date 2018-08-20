var path = require("path");
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
var ExtractTextPlugin = require('extract-text-webpack-plugin');

module.exports = {
  context: __dirname,

  entry: {
    main: ['./src/js/index.js', './src/scss/index.scss'],
  },

  output: {
    path: path.resolve('./build/'),
    filename: '[name]-[hash].js',
  },

  plugins: [],

  module: {
    rules: [
      {
        test: /\.scss$/,
        use: ExtractTextPlugin.extract({
          use: [{
            loader: "css-loader" // translates CSS into CommonJS
          }, {
            loader: "sass-loader" // compiles Sass to CSS
          }],
          // use style-loader in development
          fallback: "style-loader"
        })
      }
    ],
  }
}
