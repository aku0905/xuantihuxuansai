<template>
  <div id="app">
    <!-- 应用的主标题 -->


    <!-- 动态显示导航链接 -->
    <div v-if="isLoggedIn">
      <h1>帅气的{{ userName }}，欢迎来到选题互选赛！</h1>
      <router-link to="/home">首页</router-link> |
      <router-link to="/reward">积分商城</router-link> |
      <router-link to="/topic">选题管理</router-link> |
      <router-link to="/RedemptionList">奖品兑换记录</router-link> |
      <router-link to="/PointRecordList">积分变更记录</router-link> |
      <router-link to="/rules">规则介绍</router-link> |
      <router-link to="/topichistory">历史选题</router-link> |
      <router-link to="/userRanking">用户排名</router-link> |
<!--      <span>欢迎, {{ userName }}!</span> |-->
      <a href="#" @click="logout">登出</a> <!-- 点击登出 -->
    </div>

    <!-- 如果未登录，显示登录链接 -->
    <div v-else>
      <h1>你好，欢迎来到选题互选赛！</h1>
      <p> 先登录吧~ </p>
    </div>

    <!-- 渲染主内容 -->
    <router-view></router-view>
  </div>
</template>

<script>
import authService from '@/services/authService';

export default {
  name: 'App',
  data() {
    return {
      isLoggedIn: false, // 登录状态
      userName: ''       // 用户名
    };
  },
  created() {
    this.checkLoginStatus();  // 在应用加载时检查用户的登录状态
  },
  methods: {
    async checkLoginStatus() {
      const status = await authService.checkLoginStatus();
      if (status.loggedIn) {
        this.isLoggedIn = true;
        this.userName = status.user.username;
      } else {
        this.isLoggedIn = false;
        this.userName = '';
      }
    },
    async logout() {
      authService.logout();
      this.isLoggedIn = false;
      this.userName = '';
      await this.$router.push('/'); // 跳转到登录页面
      location.reload(); // 强制刷新页面，确保状态更新
    }
  },
  watch: {
    // 监听路由变化，如果路由变化，重新检查登录状态
    $route(to, from) {
      this.checkLoginStatus();
    }
  }
};
</script>

<style>
/* 样式保持不变 */
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
