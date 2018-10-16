const path = require('path')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const UglifyJsPlugin = require('uglifyjs-webpack-plugin')

const htmlPage = new HtmlWebpackPlugin({
  minify: {
    collapseWhitespace: true
  },
  // hash: true,
  chunksSortMode: 'dependency',
  template: './src/index.ejs'
})

module.exports = {
  context: __dirname,
  devtool: false,
  mode: 'production',
  entry: {
    scripts: ['./src/index.js']
  },
  output: {
    path: path.join(__dirname, 'build'),
    filename: '[name].js',
    publicPath: '/'
  },
  module: {
    rules: [
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
        test: /\.(png|jpg|gif)$/,
        use: [
          {
            loader: 'file-loader',
            options: {}
          }
        ]
      }
    ]
  },
  optimization: {
    splitChunks: {
      // chunks: 'all',
      chunks: 'initial'
    },
    minimizer: [
      new UglifyJsPlugin({
        minify (file, sourceMap) {
          // https://github.com/mishoo/UglifyJS2#minify-options
          const uglifyJsOptions = { /* your `uglify-js` package options */ }

          if (sourceMap) {
            uglifyJsOptions.sourceMap = {
              content: sourceMap
            }
          }

          return require('uglify-js').minify(file, uglifyJsOptions)
        }
      })
    ]
  },
  plugins: [htmlPage]
}
