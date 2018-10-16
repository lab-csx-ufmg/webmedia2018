const path = require('path')
// const webpack = require('webpack')

const HtmlWebpackPlugin = require('html-webpack-plugin')
// const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin

const htmlPage = new HtmlWebpackPlugin({
  minify: {
    collapseWhitespace: true
  },
  // hash: true,
  chunksSortMode: 'dependency',
  template: './src/index.ejs'
})

module.exports = (env) => ({
  context: __dirname,
  devtool: 'inline-sourcemap',
  mode: 'development',
  entry: {
    scripts: ['./src/index.js']
  },
  output: {
    path: path.join(__dirname, 'build'),
    filename: '[name].bundle.js',
    publicPath: '/'
  },
  devServer: {
    contentBase: path.join(__dirname, '/build'),
    // compress: true,
    stats: 'errors-only',
    historyApiFallback: true,
    host: '0.0.0.0',
    // open: true,
    // hot: true,
    openPage: '',
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH, OPTIONS',
      'Access-Control-Allow-Headers': 'X-Requested-With, content-type, Authorization'
    },
    watchContentBase: true,
    watchOptions: {
      ignored: /node_modules/
    }
  },
  module: {
    rules: [
      {
        test: /sigma.*/,
        use: 'imports-loader?this=>window'
      },
      { test: /\.html$/, use: { loader: 'html-loader' } },
      { test: /\.js$/, loader: 'babel-loader', exclude: /node_modules/ },
      { test: /\.css$/, use: [ 'style-loader', 'css-loader' ] },
      {
        test: /\.less$/,
        use: [
          { loader: 'style-loader' },
          { loader: 'css-loader' },
          { loader: 'less-loader' }
        ]
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        use: [
          {
            loader: 'file-loader',
            options: {}
          }
        ]
      }
    ]
  },
  plugins: [
    htmlPage
    // ,new BundleAnalyzerPlugin({
    //   analyzerMode: 'static'
    // })
  ],
  optimization: {
    splitChunks: {
      // chunks: 'all',
      chunks: 'initial'
    }
  }
})
