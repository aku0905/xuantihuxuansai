<template>
  <div class="topic-history">
    <h1>往期回顾</h1>

    <div class="direction">
      <label for="topic-select">选择主题方向:</label>
      <select id="topic-select" v-model="selectedTopic" @change="fetchQuestions">
        <option value="">请选择主题方向</option>
        <option v-for="topic in topics" :key="topic.direction_id" :value="topic.direction_id">
          {{ topic.direction_name }}
        </option>
      </select>
    </div>

    <div v-if="loading" class="loading">加载中...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <table v-if="!loading && !error && questions.length" class="question-table">
      <thead>
      <tr>
        <th @click="sortQuestions('proposed_by_username')">
          出题人
          <span v-if="sortKey === 'proposed_by_username'">
              {{ sortOrder === 1 ? '▲' : '▼' }}
            </span>
        </th>
        <th @click="sortQuestions('topic_name')">
          题目
          <span v-if="sortKey === 'topic_name'">
              {{ sortOrder === 1 ? '▲' : '▼' }}
            </span>
        </th>
        <th @click="sortQuestions('topic_description')">
          描述
          <span v-if="sortKey === 'topic_description'">
              {{ sortOrder === 1 ? '▲' : '▼' }}
            </span>
        </th>
        <th @click="sortQuestions('claimed_by_username')">
          认领人
          <span v-if="sortKey === 'claimed_by_username'">
              {{ sortOrder === 1 ? '▲' : '▼' }}
            </span>
        </th>
        <th>题目链接</th>
        <th @click="sortQuestions('submitted_at')">
          提交时间
          <span v-if="sortKey === 'submitted_at'">
              {{ sortOrder === 1 ? '▲' : '▼' }}
            </span>
        </th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="question in questions" :key="question.topic_id">
        <td>{{ question.proposed_by_username }}</td>
        <td>{{ question.topic_name }}</td>
        <td>{{ question.topic_description }}</td>
        <td>{{ question.claimed_by_username || '未认领' }}</td>
        <td>
          <template v-if="question.submission_link">
            <a :href="question.submission_link" target="_blank">查看链接</a>
          </template>
          <template v-else>
            <span class="empty-link">暂无链接</span>
          </template>
        </td>
        <td>{{ formatDate(question.submitted_at) }}</td>
      </tr>
      </tbody>
    </table>
    <div v-else-if="!loading && !error">没有相关选题。</div>
  </div>
</template>

<script>
import api from '../services/apiService';

export default {
  data() {
    return {
      topics: [],
      selectedTopic: '',
      questions: [],
      loading: false,
      error: null,
      sortKey: null,
      sortOrder: 1,
    };
  },
  mounted() {
    this.loadTopics();
  },
  methods: {
    async loadTopics() {
      try {
        const response = await api.get('/directions');
        this.topics = response.data;
        console.log('Loaded topics:', this.topics);
      } catch (error) {
        console.error('加载主题方向失败:', error);
        this.error = '加载主题方向失败';
      }
    },
    async fetchQuestions() {
      if (!this.selectedTopic) {
        this.questions = [];
        return;
      }

      this.loading = true;
      this.error = null;

      try {
        const response = await api.get('/topics/current', {
          params: {direction: this.selectedTopic},
        });
        this.questions = response.data;
        console.log('Fetched questions:', this.questions);
        this.sortQuestions(this.sortKey || 'submitted_at'); // 默认按提交时间排序
      } catch (error) {
        console.error('加载选题失败:', error);
        this.error = '加载选题失败';
      } finally {
        this.loading = false;
      }
    },
    sortQuestions(key) {
      this.sortKey = key;
      this.sortOrder = this.sortKey === key ? -this.sortOrder : 1;

      this.questions.sort((a, b) => {
        let aValue = a[key];
        let bValue = b[key];

        if (key === 'submitted_at') {
          return this.sortOrder * (new Date(bValue) - new Date(aValue));
        }

        if (key === 'claimed_by_username') {
          // 处理认领人排序
          if (!aValue && !bValue) return 0; // 两个都未认领
          if (!aValue) return this.sortOrder; // a 未认领，b 已认领
          if (!bValue) return -this.sortOrder; // a 已认领，b 未认领
          // 两个都已认领，按字母顺序排序
          return this.sortOrder * aValue.localeCompare(bValue, 'zh-CN');
        }

        if (typeof aValue === 'string') aValue = aValue.toLowerCase();
        if (typeof bValue === 'string') bValue = bValue.toLowerCase();

        if (aValue < bValue) return -this.sortOrder;
        if (aValue > bValue) return this.sortOrder;
        return 0;
      });
    },

    formatDate(dateString) {
      const options = {year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit'};
      return new Date(dateString).toLocaleDateString('zh-CN', options);
    }
  },
};
</script>

<style lang="scss" scoped>
@import "../assets/TopicHistory.scss";

.question-table {
  table-layout: fixed;
  width: 100%;

  th, td {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  th:nth-child(1), td:nth-child(1) {
    width: 10%;
  }

  // 出题人
  th:nth-child(2), td:nth-child(2) {
    width: 15%;
  }

  // 题目
  th:nth-child(3), td:nth-child(3) {
    width: 30%;
  }

  // 描述
  th:nth-child(4), td:nth-child(4) {
    width: 10%;
  }

  // 认领人
  th:nth-child(5), td:nth-child(5) {
    width: 15%;
  }

  // 题目链接
  th:nth-child(6), td:nth-child(6) {
    width: 20%;
  }

  .empty-link {
    color: #999;
    font-style: italic;
  }

  // 提交时间

  th {
    cursor: pointer;
    user-select: none;

    &:hover {
      background-color: darken($primary-color, 5%);
    }
  }

  td {
    padding: 10px;
  }
}
</style>