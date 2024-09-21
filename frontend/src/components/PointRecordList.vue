<template>
  <div>
    <h1>积分记录</h1>
    <ul class="record-list">
      <li v-for="record in records" :key="record.action_id" class="record-item">
        <div class="record-content">
          <span class="column">记录类型: {{ record.action_type }}</span>
          <span class="column">数量: {{ record.points }}</span>
          <span class="column">选题ID: {{ record.topic_id }}</span>
          <span class="column">时间: {{ new Date(record.created_at).toLocaleString() }}</span>
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
    const {loggedIn, user} = await this.checkLoginStatus();
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
        if (response.status === 200) {
          return {loggedIn: true, user: response.data};
        } else {
          return {loggedIn: false};
        }
      } catch (error) {
        console.error('登录验证失败:', error.message);
        return {loggedIn: false};
      }
    },
    async fetchRecords() {
      try {
        const response = await apiService.get('/records', {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        });
        if (response.status === 200) {
          this.records = response.data;
        }
      } catch (error) {
        console.error('获取积分记录失败:', error.message);
      }
    }
  }
};
</script>

<style scoped>
.record-list {
  list-style-type: none;
  padding: 0;
}

.record-item {
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

.record-content {
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

@media (max-width: 768px) {
  .record-content {
    flex-direction: column;
  }

  .column {
    margin-bottom: 10px;
    text-align: left;
  }
}
</style>
