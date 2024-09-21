// router/index.js
// 导入vue-router库中的createRouter和createWebHistory函数
import { createRouter, createWebHistory } from 'vue-router';
// 导入各个页面组件
import HomePage from '@/views/HomePage.vue';
import LoginRegisterPage from '@/views/LoginRegisterPage.vue';
import reward from '@/views/Reward.vue';
import topic from '@/views/Topic.vue';
import RedemptionList from "@/components/RedemptionList.vue";
import PointRecordList from "@/components/PointRecordList.vue";
import rules from "@/components/Rules.vue";
import topichistory from "@/components/TopicHistory.vue";
import UserRanking from "@/views/AllRanking.vue"

// 定义路由数组，每个路由映射一个组件
const routes = [
    { path: '/', name: 'LoginRegisterPage', component: LoginRegisterPage }, // 登录注册页
    { path: '/home', name: 'home', component: HomePage }, // 主页
    { path: '/reward', name: 'reward', component: reward } ,// 奖励页
    { path: '/topic', name: 'topic', component: topic},
    { path: '/RedemptionList', name: 'RedemptionList', component: RedemptionList },
    { path: '/PointRecordList', name: 'PointRecordList', component: PointRecordList },
    { path: '/rules', name: 'rules', component: rules },
    { path: '/topichistory', name: 'topichistory', component: topichistory},
    { path: '/UserRanking', name:'UserRanking', component: UserRanking},

];

// 创建路由实例，配置路由历史记录模式和路由数组
const router = createRouter({
    history: createWebHistory(), // 使用HTML5历史记录模式
    routes, // 路由配置数组
});

// 导出路由实例，供其他模块使用
export default router;
