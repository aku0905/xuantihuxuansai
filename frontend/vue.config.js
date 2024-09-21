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
        // 添加 DefinePlugin 插件
        config.plugin('define')
            .use(webpack.DefinePlugin, [{
                '__VUE_PROD_HYDRATION_MISMATCH_DETAILS__': JSON.stringify(true),
                // 如果有其他需要的标志，可以在这里添加
            }]);
    }
};
