<template>
  <div class="records-container">
    <h1 class="page-title">积分记录</h1>
    <div v-if="records.length === 0" class="no-records">
      暂无积分记录
    </div>
    <ul v-else class="record-list">
      <li v-for="record in records" :key="record.action_id" class="record-item">
        <div class="record-content">
          <span class="column action-type">
            <i class="fas fa-tag"></i>
            {{ record.action_type }}
          </span>
          <span class="column points" :class="{ positive: record.points > 0, negative: record.points < 0 }">
            <i class="fas fa-coins"></i>
            {{ record.points > 0 ? '+' : '' }}{{ record.points }}
          </span>
          <span class="column topic-id">
            <i class="fas fa-hashtag"></i>
            {{ record.topic_id || '无' }}
          </span>
          <span class="column created-at">
            <i class="far fa-clock"></i>
            {{ formatDate(record.created_at) }}
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
      records: [],
      userId: null,
      token: null
    };
  },
  async mounted() {
    const { loggedIn, user } = await this.checkLoginStatus();
    if (loggedIn && user) {
      this.userId = user.user_id;
      this.token = localStorage.getItem('authToken');
      this.fetchRecords();
    } else {
      console.log('用户未登录');
    }
  },
  methods: {
    async checkLoginStatus() {
      try {
        const response = await apiService.get('/users/me');
        return response.status === 200 ? { loggedIn: true, user: response.data } : { loggedIn: false };
      } catch (error) {
        console.error('登录验证失败:', error.message);
        return { loggedIn: false };
      }
    },
    async fetchRecords() {
      try {
        const response = await apiService.get('/records', {
          headers: { Authorization: `Bearer ${this.token}` }
        });
        if (response.status === 200) {
          this.records = response.data;
        }
      } catch (error) {
        console.error('获取积分记录失败:', error.message);
      }
    },
    formatDate(dateString) {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' };
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
$positive-color: #2ecc71;
$negative-color: #e74c3c;

.records-container {
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

.record-list {
  list-style-type: none;
  padding: 0;
}

.record-item {
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

.record-content {
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
    width: 20px;
    text-align: center;
  }
}

.action-type { font-weight: bold; color: $primary-color; }
.points {
  font-weight: bold;
  &.positive { color: $positive-color; }
  &.negative { color: $negative-color; }
}
.topic-id { color: $secondary-color; }
.created-at { font-size: 0.9rem; color: #7f8c8d; }

@media (max-width: 768px) {
  .record-content {
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
</style>