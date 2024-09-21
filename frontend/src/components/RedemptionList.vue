<template>
  <div>
    <h1>积分兑换记录</h1>
    <ul class="redemption-list">
      <li v-for="redemption in redemptions" :key="redemption.redemption_id" class="redemption-item">
        <div class="redemption-content">
          <span class="column">奖品名称: {{ redemption.reward_name }}</span>
          <span class="column">数量: {{ redemption.quantity }}</span>
          <span class="column">消耗积分: {{ redemption.points_spent }}</span>
          <span class="column">状态: {{ redemption.status }}</span>
          <span class="column">领取时间: {{ new Date(redemption.created_at).toLocaleString() }}</span>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import apiService from '../services/apiService';

export default {
  data() {
    return {
      redemptions: [],
      userId: null,
      token: null
    };
  },
  async mounted() {
    const { loggedIn, user } = await this.checkLoginStatus();
    if (loggedIn && user) {
      this.userId = user.user_id;
      this.token = localStorage.getItem('authToken');
      this.fetchRedemptions();
    } else {
      console.log('用户未登录');
    }
  },
  methods: {
    async checkLoginStatus() {
      try {
        const response = await apiService.get('/users/me');
        if (response.status === 200) {
          return { loggedIn: true, user: response.data };
        } else {
          return { loggedIn: false };
        }
      } catch (error) {
        console.error('登录验证失败:', error.message);
        return { loggedIn: false };
      }
    },
    async fetchRedemptions() {
      try {
        const response = await apiService.get('/redemptions', {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        });
        if (response.status === 200) {
          this.redemptions = response.data;
        }
      } catch (error) {
        console.error('获取兑换记录失败:', error.message);
      }
    }
  }
};
</script>

<style scoped>
.redemption-list {
  list-style-type: none;
  padding: 0;
}

.redemption-item {
  background-color: #f8f9fa;
  margin: 10px 0;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
}

.redemption-content {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.column {
  flex: 1;
  text-align: left;  /* 垂直左对齐 */
  padding: 5px 10px;
  font-size: 14px;
  color: #333;
}

h1 {
  margin-bottom: 20px;
  color: #2c3e50;
  font-weight: bold;
}

button {
  background-color: #007bff !important;
  color: white;
  padding: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-bottom: 20px;
  display: block;
  width: 100%;
}

@media (max-width: 768px) {
  .redemption-content {
    flex-direction: column;
  }

  .column {
    margin-bottom: 10px;
    text-align: left;
  }
}
</style>
