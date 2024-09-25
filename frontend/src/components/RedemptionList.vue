<template>
  <div class="redemption-container">
    <h1 class="page-title">积分兑换记录</h1>
    <div v-if="redemptions.length === 0" class="no-records">
      暂无兑换记录
    </div>
    <ul v-else class="redemption-list">
      <li v-for="redemption in redemptions" :key="redemption.redemption_id" class="redemption-item">
        <div class="redemption-content">
          <span class="column reward-name">
            <i class="fas fa-gift"></i>
            {{ redemption.reward_name }}
          </span>
          <span class="column quantity">
            <i class="fas fa-hashtag"></i>
            {{ redemption.quantity }}
          </span>
          <span class="column points-spent">
            <i class="fas fa-coins"></i>
            {{ redemption.points_spent }}
          </span>
          <span class="column status" :class="redemption.status.toLowerCase()">
            <i class="fas fa-info-circle"></i>
            已兑换
          </span>
          <span class="column created-at">
            <i class="far fa-calendar-alt"></i>
            {{ formatDate(redemption.created_at) }}
          </span>
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
    const {loggedIn, user} = await this.checkLoginStatus();
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
        return response.status === 200 ? {loggedIn: true, user: response.data} : {loggedIn: false};
      } catch (error) {
        console.error('登录验证失败:', error.message);
        return {loggedIn: false};
      }
    },
    async fetchRedemptions() {
      try {
        const response = await apiService.get('/redemptions', {
          headers: {Authorization: `Bearer ${this.token}`}
        });
        if (response.status === 200) {
          this.redemptions = response.data;
        }
      } catch (error) {
        console.error('获取兑换记录失败:', error.message);
      }
    },
    formatDate(dateString) {
      const options = {year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit'};
      return new Date(dateString).toLocaleDateString('zh-CN', options);
    }
  }
};
</script>

<style lang="scss" scoped>
$primary-color: #3498db;
$secondary-color: #2ecc71;
$background-color: #f5f7fa;
$text-color: #34495e;
$status-pending: #f39c12;
$status-completed: #2ecc71;
$status-cancelled: #e74c3c;

.redemption-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: $background-color;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.page-title {
  font-size: 2.5rem;
  color: $primary-color;
  text-align: center;
  margin-bottom: 30px;
  font-weight: 300;
}

.no-records {
  text-align: center;
  font-size: 1.2rem;
  color: $text-color;
  margin-top: 50px;
}

.redemption-list {
  list-style-type: none;
  padding: 0;
}

.redemption-item {
  background-color: white;
  margin: 15px 0;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  }
}

.redemption-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
}

.column {
  flex: 1 1 200px;
  padding: 10px;
  font-size: 1rem;
  color: $text-color;
  display: flex;
  align-items: center;

  i {
    margin-right: 10px;
    font-size: 1.2rem;
  }
}

.reward-name {
  font-weight: bold;
  color: $primary-color;
}

.quantity {
  color: $secondary-color;
}

.points-spent {
  font-weight: bold;
}

.status {
  &.pending {
    color: $status-pending;
  }

  &.completed {
    color: $status-completed;
  }

  &.cancelled {
    color: $status-cancelled;
  }
}

.created-at {
  font-size: 0.9rem;
  color: #7f8c8d;
}

@media (max-width: 768px) {
  .redemption-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .column {
    margin-bottom: 10px;
    flex-basis: 100%;
  }

  .page-title {
    font-size: 2rem;
  }
}

.column {
  flex: 1 1 200px;
  padding: 10px;
  font-size: 1rem;
  color: $text-color;
  display: flex;
  align-items: center;

  i {
    margin-right: 10px;
    font-size: 1.2rem;
    width: 20px; // 确保图标宽度一致
    text-align: center; // 居中对齐图标
  }
}


</style>