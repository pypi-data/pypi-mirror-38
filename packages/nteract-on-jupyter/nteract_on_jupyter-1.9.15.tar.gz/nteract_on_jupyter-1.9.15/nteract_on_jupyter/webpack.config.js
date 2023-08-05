// @flow
const configurator = require("@nteract/webpack-configurator");
const LodashModuleReplacementPlugin = require("lodash-webpack-plugin");
const webpack = require("webpack");
const MonacoWebpackPlugin = require("monaco-editor-webpack-plugin");

const babelFlowConfig = require("../../../babel.flow.config");
const babelTypescriptConfig = require("../../../babel.typescript.config");

const nodeEnv = process.env.NODE_ENV || "development";
const isProd = nodeEnv === "production";

const ASSET_PATH = process.env.ASSET_PATH || "/nteract/static/dist";

module.exports = {
  externals: ["canvas"],
  mode: isProd ? "production" : "development",
  devtool: isProd ? "hidden-source-map" : "cheap-eval-source-map",
  entry: {
    app: "./app/index.js"
  },
  devServer: isProd
    ? {}
    : {
        hot: true,
        headers: { "Access-Control-Allow-Origin": "*" }
      },
  target: "web",
  output: {
    // Note: this gets overriden by our use of __webpack_public_path__ later
    publicPath: ASSET_PATH,
    chunkFilename: "[name]-[chunkhash].bundle.js"
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: configurator.exclude,
        loader: "babel-loader",
        options: babelFlowConfig()
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"]
      },
      {
        test: /\.tsx?$/,
        exclude: configurator.exclude,
        loader: "babel-loader",
        options: babelTypescriptConfig()
      }
    ]
  },
  resolve: {
    mainFields: ["nteractDesktop", "module", "main"],
    extensions: [".js", ".jsx", ".ts", ".tsx"],
    alias: configurator.mergeDefaultAliases()
  },
  plugins: [
    new LodashModuleReplacementPlugin(),
    new webpack.DefinePlugin({
      "process.env.ASSET_PATH": JSON.stringify(ASSET_PATH)
    }),
    //new webpack.IgnorePlugin(/\.(css|less)$/),
    new MonacoWebpackPlugin(),

    new webpack.IgnorePlugin(
      /^((fs)|(path)|(os)|(crypto)|(source-map-support))$/,
      /vs\/language\/typescript\/lib/
    )
  ]
};
