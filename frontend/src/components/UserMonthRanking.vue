<template>
  <div class="user-ranking">
    <h2>本月积分排名</h2>
    <div v-if="isLoggedIn">
      <div v-if="users.length > 0" class="ranking-list">
        <div v-for="(user, index) in users" :key="user.user_id" class="ranking-item">
          <span class="rank">{{ index + 1 }}</span>
          <span class="username">{{ user.username }}</span>
          <span class="points">{{ user.total_points }} 分</span>
        </div>
      </div>
      <div v-else>
        <p>没有用户数据或正在加载中...</p>
      </div>
    </div>
    <div v-else>
      <p>请先登录以查看积分排名。</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/apiService'; // 导入 API 服务

const users = ref([]);
const isLoggedIn = ref(false);

async function checkLoginStatus() {
  const token = localStorage.getItem('authToken');
  if (token) {
    try {
      // 验证用户是否已登录
      const response = await api.get('/users/me', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.status === 200) {
        isLoggedIn.value = true;
        fetchUsers(); // 获取积分排名
      } else {
        isLoggedIn.value = false;
      }
    } catch (error) {
      console.error('验证失败:', error.message);
      isLoggedIn.value = false;
    }
  } else {
    isLoggedIn.value = false;
  }
}

async function fetchUsers() {
  try {
    // 获取用户积分排名
    const response = await api.get('/users/ranking');
    if (response.status === 200) {
      users.value = response.data; // 获取用户积分排名数据
    } else {
      console.error('获取用户排名失败:', response.statusText);
    }
  } catch (error) {
    console.error('获取用户排名失败:', error.message);
  }
}

onMounted(() => {
  checkLoginStatus(); // 组件挂载时检查登录状态
});
</script>

<style scoped>
.user-ranking {
  margin: 20px;
}

.ranking-list {
  display: flex;
  flex-direction: column;
  gap: 10px; /* 增加间隔 */
}

.ranking-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f7f7f7;
  padding: 10px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.rank {
  font-weight: bold;
  width: 30px;
  text-align: center;
}

.username {
  flex: 1;
  text-align: center;
}

.points {
  font-weight: bold;
}
</style>
