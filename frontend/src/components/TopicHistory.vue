<template>
  <div>
    <h1>往期回顾</h1>

    <div class="direction">
      <label for="topic-select" style="font-size: 18px;">选择主题方向:</label>
      <select v-model="selectedTopic" @change="fetchQuestions" style="font-size: 18px; text-align: left;">
        <option v-for="topic in topics" :key="topic.direction_id" :value="topic.direction_id">
          {{ topic.direction_name }}
        </option>
      </select>
    </div>

    <div v-if="loading">加载中...</div>
    <div v-if="error">{{ error }}</div>

    <table v-if="questions.length" class="question-table">
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
        <td>{{ question.claimed_by_username }}</td>
        <td><a :href="question.submission_link" target="_blank">查看链接</a></td>
        <td>{{ new Date(question.submitted_at).toLocaleString() }}</td>
      </tr>
      </tbody>
    </table>
    <div v-else>没有相关选题。</div>
  </div>
</template>

<script>
import api from '../services/apiService';

export default {
  data() {
    return {
      topics: [],
      selectedTopic: null,
      questions: [],
      loading: false,
      error: null,
      sortKey: null,
      sortOrder: 1, // 1 为升序，-1 为降序
    };
  },
  mounted() {
    this.loadTopics();
  },
  methods: {
    async loadTopics() {
      try {
        const response = await api.get('/directions'); // 确保路径正确
        this.topics = response.data;
      } catch (error) {
        console.error('加载主题方向失败:', error);
        this.error = '加载主题方向失败';
      }
    },
    async fetchQuestions() {
      if (!this.selectedTopic) {
        this.error = '请先选择一个主题方向';
        return;
      }

      this.loading = true;
      this.error = null;

      try {
        const response = await api.get('/topics/current', {
          params: { direction: this.selectedTopic }, // 将选题方向 ID 作为参数传递
        });
        this.questions = response.data;
        this.sortQuestions(this.sortKey); // 确保在获取数据后进行排序
      } catch (error) {
        console.error('加载选题失败:', error);
        this.error = '加载选题失败';
      } finally {
        this.loading = false;
      }
    },
    sortQuestions(key) {
      // 如果点击的是同一个列，则切换排序顺序
      if (this.sortKey === key) {
        this.sortOrder = -this.sortOrder;
      } else {
        this.sortKey = key;
        this.sortOrder = 1; // 默认升序
      }

      this.questions.sort((a, b) => {
        let aValue = a[key];
        let bValue = b[key];

        if (key === 'claimed_by_username') {
          // 先按是否为空排序
          if (!aValue && bValue) return -1 * this.sortOrder; // a 为空，b 不为空
          if (aValue && !bValue) return 1 * this.sortOrder; // b 为空，a 不为空
        } else if (key === 'proposed_by_username') {
          // 对出题人按照拼音首字母排序
          aValue = aValue ? aValue.charCodeAt(0) : '';
          bValue = bValue ? bValue.charCodeAt(0) : '';
        } else if (key === 'submitted_at') {
          // 对提交时间进行排序
          aValue = new Date(a.submitted_at).getTime();
          bValue = new Date(b.submitted_at).getTime();
        }

        if (aValue < bValue) return -1 * this.sortOrder; // 升序或降序
        if (aValue > bValue) return 1 * this.sortOrder;  // 升序或降序
        return 0; // 相等时不排序
      });
    },
  },
};
</script>

<style scoped>
.question-table {
  width: 80%;
  border-collapse: collapse;
  margin: 0 auto;
}

.direction {
  width: 80%;
  margin: 0 auto;
  margin-bottom: 20px;
  text-align: left;
}

.direction select {
  font-size: 16px; /* 调整字体大小 */
  color: #333; /* 设置字体颜色 */
  padding: 8px; /* 添加内边距 */
  border: 1px solid #ccc; /* 添加边框 */
  border-radius: 4px; /* 添加圆角 */
  width: 30%; /* 设置下拉框宽度 */
  box-sizing: border-box; /* 确保内边距和边框不会增加元素的宽度 */
  appearance: none; /* 移除默认的下拉箭头 */
  -webkit-appearance: none; /* 移除默认的下拉箭头（针对Safari） */
  background: url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.9.0/icons/arrow-down-circle.svg') no-repeat right 8px center/16px 16px; /* 添加自定义下拉箭头 */
  background-color: #fff; /* 设置背景颜色 */
}

.question-table th,
.question-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
  cursor: pointer; /* 添加指针样式 */
}

.question-table th {
  background-color: #f2f2f2;
}

.question-table th:nth-child(1),
.question-table td:nth-child(1) {
  width: 10%; /* 第一列宽度 */
}

.question-table th:nth-child(2),
.question-table td:nth-child(2) {
  width: 20%; /* 第二列宽度 */
}

.question-table th:nth-child(3),
.question-table td:nth-child(3) {
  width: 35%; /* 第三列宽度 */
}

.question-table th:nth-child(4),
.question-table td:nth-child(4) {
  width: 10%; /* 第四列宽度 */
}

.question-table th:nth-child(5),
.question-table td:nth-child(5) {
  width: 10%; /* 第五列宽度 */
}

.question-table th:nth-child(6),
.question-table td:nth-child(6) {
  width: 15%; /* 第六列宽度 */
}



</style>
