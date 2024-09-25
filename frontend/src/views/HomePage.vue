<template>
  <div class="home-page grid-container">
    <div>
      <!-- 用户信息组件，展示用户的基本信息 -->
      <UserInfo />
      <rules />
    </div>
    <!-- 选题列表组件，展示所有选题信息 -->
    <topicList />
    <!-- 用户排名组件 展示所有用户的排名信息-->
    <User_monthRanking />

<!--    &lt;!&ndash; 奖励组件，展示用户的奖励信息 &ndash;&gt;-->
<!--    <RewardsCatalog.vue />-->

  </div>
</template>

<script>
// 导入用户信息组件
// import UserInfo from '../components/UserInfo.vue';
import UserInfo from '@/components/UserInfo.vue';
import UserRanking from '@/components/UserRanking.vue';
import User_monthRanking from "@/components/UserMonthRanking.vue";
import RewardsCatalog from "@/components/RewardsCatalog.vue";
import topicList  from "@/components/TopicList.vue";
import Rules from "@/components/Rules.vue";

export default {
  name: 'HomePage', // 页面名称
  components: {
    Rules,
    UserInfo, // 用户信息组件
    UserRanking, // 用户排名组件
    User_monthRanking,
    RewardsCatalog, // 奖励目录组件
    topicList
  }
}
</script>

<style scoped>
/* 网格布局样式定义 */
.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  align-self: start;  /* 确保所有网格行的子项在顶部对齐 */
}

/* 子组件的对齐与边距调整 */
.grid-container > div {
  align-self: start; /* 确保每个子项在其网格行内顶部对齐 */
  margin-top: 10px; /* 统一顶部外边距 */
  box-sizing: border-box; /* 包括边框和内边距在宽度和高度内 */
}

/* 样式定义 */
.home-page {
  padding: 20px;
}
</style>