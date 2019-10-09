const path = require('path');
const webpack = require('webpack');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');

const mode = process.env.NODE_ENV === 'production' ? 'production' : 'development';

module.exports = {
    mode: mode,
    context: __dirname,
    entry: ['./app'],
    output: {
        path: path.resolve('./bundles/'),
        filename: 'app.js'
    },

    optimization: {
        minimizer: [
            new UglifyJsPlugin({
                cache: true,
                parallel: true,
                sourceMap: false,
                extractComments: 'all',
                uglifyOptions: {
                    compress: true,
                    output: null
                }
            })
        ]
    },

    plugins: [
        new VueLoaderPlugin()
    ],

    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                loader: 'babel-loader'
            },
            {
                test: /\.vue$/,
                loader: 'vue-loader',
            },
            {test: /\.scss?$/, loaders: ['style-loader', 'css-loader', 'sass-loader']},
            {test: /\.css?$/, loaders: ['style-loader', 'css-loader', 'sass-loader']},
            {
                test: /\.svg$/,
                loader: 'svg-inline-loader'
            },
            {
                test: /\.(woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            name: '[name].[ext]',
                            outputPath: 'fonts/'
                        }
                    }
                ]
            }
        ],
    },
    resolve: {
        modules: ['node_modules'],
        alias: {vue: mode === 'production' ? 'vue/dist/vue.min.js' : 'vue/dist/vue.js'}
    },
};
