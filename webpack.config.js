const path = require('path');
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');


module.exports = {
    entry: {
        layout: "./src/js/layout.js",
        courses: "./src/js/courses.js",
        course_detail:"./src/js/course_detail.js",
        cart: "./src/js/cart.js"
    },
    output: {
        filename: '[name].js',
        path: path.resolve(__dirname, 'dist'),
        clean: true,
        assetModuleFilename: '[name][ext]',
    },
    plugins: [
        new WebpackManifestPlugin(),
        new CopyWebpackPlugin({
            patterns: [
                { from: './src/ephora', to: 'ephora' },
                { from: './src/ckeditor', to: 'ckeditor' }
            ],
        }),
    ],
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    'style-loader',
                    'css-loader'
                ]
            },
            {
                test: /\.(png|jpe?g|gif|svg)$/i,
                use: [
                    {
                        loader: 'url-loader',
                        options: {
                            limit: 8192,
                            name: '[name].[ext]',
                            outputPath: 'images', // Output path for images
                        },
                    },
                ],
            },
            {
                test: require.resolve("jquery"),
                loader: "expose-loader",
                options: {
                    exposes: ["$", "jQuery"],
                },
            }
        ]
    },
};
