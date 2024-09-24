<template>
  <div class="user-ranking">
    <h2 class="title">本月积分排名</h2>
    <div v-if="isLoggedIn">
      <div v-if="users.length > 0" class="ranking-list">
        <div v-for="(user, index) in users" :key="user.user_id"
             class="ranking-item"
             :class="{ 'top-three': index < 3 }">
          <span class="rank" :class="'rank-' + (index + 1)">{{ index + 1 }}</span>
          <span class="username">{{ user.username }}</span>
          <span class="points">{{ user.total_points }} 分</span>
        </div>
      </div>
      <div v-else class="loading">
        <p>加载中...</p>
        <div class="spinner"></div>
      </div>
    </div>
    <div v-else class="login-message">
      <p>请先登录以查看积分排名。</p>
      <button @click="redirectToLogin" class="login-button">登录</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/apiService';
import { useRouter } from 'vue-router';

const users = ref([]);
const isLoggedIn = ref(false);
const router = useRouter();

async function checkLoginStatus() {
  const token = localStorage.getItem('authToken');
  if (token) {
    try {
      const response = await api.get('/users/me', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.status === 200) {
        isLoggedIn.value = true;
        fetchUsers();
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
    const response = await api.get('/users/ranking');
    if (response.status === 200) {
      users.value = response.data;
    } else {
      console.error('获取用户排名失败:', response.statusText);
    }
  } catch (error) {
    console.error('获取用户排名失败:', error.message);
  }
}

function redirectToLogin() {
  router.push('/login');
}

onMounted(() => {
  checkLoginStatus();
});
</script>

<style lang="scss" scoped>
$primary-color: #3498db;
$secondary-color: #2ecc71;
$background-color: #f5f7fa;
$text-color: #34495e;
$gold: #ffd700;
$silver: #c0c0c0;
$bronze: #cd7f32;

.user-ranking {
  width: 100%; /* 使用百分比宽度 */
  padding: 20px;
  background-color: $background-color;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.title {
  color: $primary-color;
  text-align: center;
  font-size: 2rem;
  margin-bottom: 20px;
}

.ranking-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.ranking-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: white;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  &.top-three {
    background-color: lighten($primary-color, 40%);
  }
}

.rank {
  font-weight: bold;
  width: 30px;
  height: 30px;
  line-height: 30px;
  text-align: center;
  border-radius: 50%;
  background-color: $primary-color;
  color: white;

  &.rank-1 { background-color: $gold; }
  &.rank-2 { background-color: $silver; }
  &.rank-3 { background-color: $bronze; }
}

.username {
  flex: 1;
  text-align: left;
  margin-left: 15px;
  font-weight: 500;
}

.points {
  font-weight: bold;
  color: $secondary-color;
}

.loading {
  text-align: center;
  color: $text-color;

  .spinner {
    width: 40px;
    height: 40px;
    margin: 20px auto;
    border: 4px solid #f3f3f3;
    border-top: 4px solid $primary-color;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
}

.login-message {
  text-align: center;
  color: $text-color;

  .login-button {
    margin-top: 10px;
    padding: 10px 20px;
    background-color: $primary-color;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;

    &:hover {
      background-color: darken($primary-color, 10%);
    }
  }
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 480px) {
  .user-ranking {
    padding: 15px;
  }

  .title {
    font-size: 1.5rem;
  }

  .ranking-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
  }

  .username, .points {
    width: 100%;
    text-align: left;
  }
}
</style>
