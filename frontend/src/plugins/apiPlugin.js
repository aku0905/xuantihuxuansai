// src/plugins/apiPlugin.js

// 导入api服务模块
import api from '../services/apiService';

// 定义一个插件对象，默认导出
export default {
    // 安装插件的方法，接收一个app实例作为参数
    install(app) {
        // 将api服务对象挂载到app实例的全局属性上，使得所有组件都能访问
        app.config.globalProperties.$api = api;
    }
};
