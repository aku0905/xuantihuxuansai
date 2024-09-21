// src/main.js

// 从 vue 包中导入 createApp 函数，用于创建 Vue 应用实例
import {createApp} from 'vue';

// 导入根组件 App.vue
import App from './App.vue';

// 导入路由配置
import router from './router';

// import './assets/global.scss'; // 引入全局样式

// 导入API设置
import api from './services/apiService';

//导入插件
import apiPlugin from './plugins/apiPlugin';

// 使用 createApp 函数创建一个 Vue 应用实例
const app = createApp(App);

// 使用应用实例的 use 方法安装路由插件
app.use(router);

// 将应用实例挂载到 DOM 元素上，#app 是挂载点的选择器
app.mount('#app');

