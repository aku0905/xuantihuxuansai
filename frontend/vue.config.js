const webpack = require('webpack');

module.exports = {
    css: {
        loaderOptions: {
            scss: {
                additionalData: `@import "@/assets/global.scss";`
            }
        }
    },
    chainWebpack: config => {
        config.plugin('define')
            .use(webpack.DefinePlugin, [{
                'process.env': {
                    NODE_ENV: JSON.stringify(process.env.NODE_ENV || 'development'),
                    VUE_APP_API_URL: JSON.stringify(process.env.VUE_APP_API_URL || 'http://134.175.170.70:5000')
                }
            }]);
    }
};
