<template>
  <div class="home-page grid-container">
    <div>
      <!-- 用户信息组件，展示用户的基本信息 -->
      <UserInfo />
      <Rules />
    </div>
    <!-- 选题列表组件，展示所有选题信息 -->
    <TopicList />
    <!-- 用户排名组件，展示所有用户的排名信息，限制宽度占比 -->
    <div class="user-ranking-container">
      <User_monthRanking />
    </div>
  </div>
</template>

<script>
import UserInfo from '@/components/UserInfo.vue';
import UserRanking from '@/components/UserRanking.vue';
import User_monthRanking from "@/components/UserMonthRanking.vue";
import RewardsCatalog from "@/components/RewardsCatalog.vue";
import TopicList from "@/components/TopicList.vue";
import Rules from "@/components/Rules.vue";

export default {
  name: 'HomePage',
  components: {
    Rules,
    UserInfo,
    UserRanking,
    User_monthRanking,
    RewardsCatalog,
    TopicList
  }
}
</script>

<style scoped>
.home-page {
  padding: 30px; /* 添加内边距 */
  margin: 0 30px; /* 添加左右外边距以留白 */
}

.grid-container {
  display: grid;
  grid-template-columns: 1.5fr 3fr 0.8fr; /* 调整列宽比例，使选题组件更宽 */
  gap: 20px;
  align-self: start;
}

/* 用户排名组件容器 */
.user-ranking-container {
  width: 100%; /* 让排名组件占满其父容器 */
  margin: 0 auto; /* 居中对齐 */
}

/* 子组件的对齐与边距调整 */
.grid-container > div {
  align-self: start;
  margin-top: 10px;
  box-sizing: border-box;
}
</style>
