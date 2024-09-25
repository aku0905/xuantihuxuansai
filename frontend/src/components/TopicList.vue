<template>
  <div class="topic-list">
    <h2 class="page-title">选题管理</h2>

    <!-- 提交选题 -->
    <div class="add-topic card">
      <h3>提交选题</h3>

      <div class="add-topic-row">
        <p class="topic-info"><strong>本期主题：</strong> {{ latestDirection.direction_name }}</p>
      </div>

      <div class="add-topic-row">
        <p class="topic-info"><strong>主题描述：</strong> {{ latestDirection.description }}</p>
      </div>

      <div class="add-topic-row">
        <input v-model="newTopic.title" placeholder="输入你要提出的题目：（不少于5个字符）" class="input-field" />
        <textarea v-model="newTopic.description" placeholder="你希望认领的友友写什么？（不少于10个字符）" class="input-field"></textarea>
        <button @click="addTopic" class="submit-button2">提交</button>
      </div>
    </div>

    <div v-if="currentUser && topics.length > 0">

      <!-- 我的已选选题 -->
      <div v-if="myClaimedTopics.length" class="topic-section">
        <h2>我的已选选题</h2>
        <div class="topics-grid">
          <div v-for="topic in myClaimedTopics" :key="topic.topic_id" class="topic-item card">
            <div class="topic-header">
              <span class="topic-title">{{ topic.topic_name }}</span>
            </div>
            <p class="topic-description">{{ topic.topic_description }}</p>
            <div class="topic-meta">
              <span class="topic-status">状态: {{ topic.status }}</span>
              <span class="topic-owner">出题人: {{ topic.proposed_by_username }}</span>
            </div>
            <div class="submission-section">
              <template v-if="topic.submission_link">
                <a :href="topic.submission_link" target="_blank" class="hover-info">点击查看文章</a>
                <input v-model="submissionLinks[topic.topic_id]" placeholder="重新提交链接" class="input-field" />
                <button @click="submitLink(topic.topic_id)" class="submit-button">重新提交</button>
              </template>
              <template v-else>
                <input v-model="submissionLinks[topic.topic_id]" placeholder="提交链接" class="input-field" />
                <button @click="submitLink(topic.topic_id)" class="submit-button">提交</button>
                <button @click="cancelClaim(topic.topic_id)" class="cancel-button">取消</button>
              </template>
            </div>
          </div>
        </div>
      </div>

      <!-- 未认领选题 -->
      <div v-if="unclaimedTopics.length" class="topic-section">
        <h2>待认领选题</h2>
        <div class="topics-grid">
          <div v-for="topic in unclaimedTopics" :key="topic.topic_id" class="topic-item card">
            <div class="topic-header">
              <span class="topic-title">{{ topic.topic_name }}</span>
            </div>
            <p class="topic-description">{{ topic.topic_description }}</p>
            <div class="topic-meta small-text">
              <span class="topic-status">状态: {{ topic.status }}</span>
              <span class="topic-owner">出题人: {{ topic.proposed_by_username }}</span>
            </div>
            <div class="submission-section">
              <button @click="claimTopic(topic.topic_id)" class="submit-button3">认领</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 其他用户已认领的选题 -->
      <div v-if="otherClaimedTopics.length" class="topic-section">
        <h2>其他用户已选选题</h2>
        <div class="topics-grid">
          <div
              v-for="topic in otherClaimedTopics"
              :key="topic.topic_id"
              class="topic-item card"
          >
            <div class="topic-header">
              <span class="topic-title">{{ topic.topic_name }}</span>
              <span class="topic-owner">出题人: {{ topic.proposed_by_username }}</span>
            </div>
            <p class="topic-description">{{ topic.topic_description }}</p>
            <div class="topic-meta small-text">
              <span class="topic-status">状态: {{ topic.status }}</span>
              <span class="topic-claimer">认领人: {{ topic.claimed_by_username }}</span>
            </div>
            <template v-if="topic.submission_link"  >

              <span class="hover-info" @click="openLink(topic.submission_link)">点击查看文章</span>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>





<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '../services/apiService';

// 声明相关的响应式变量
const topics = ref([]);
const isLoggedIn = ref(false);
const currentUser = ref(null);
const newTopic = ref({
  title: '',
  description: '',
});
const submissionLinks = ref({});  // 定义一个响应式对象submissionLinks，用于存储提交链接
const directions = ref([]);   // 定义一个响应式数组directions，用于存储选题方向

// 将 latestDirection 定义为一个对象，包含方向的名字、描述和ID
const latestDirection = ref({
  direction_name: '最新一期',  // 设置默认值
  description: '暂无描述',      // 默认描述
  direction_id: null            // ID 默认空值
});

// 提示信息
const message = ref('');
const messageType = ref(''); // 'success' or 'error'

// 检查用户的登录状态并获取必要的数据
async function checkLoginStatus() {
  const token = localStorage.getItem('authToken');
  if (token) {
    try {
      const response = await api.get('/users/me', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.status === 200) {
        isLoggedIn.value = true;
        currentUser.value = response.data;
        await fetchDirections(); // 获取方向信息
        if (latestDirection.value.direction_id) {
          await fetchTopics(); // 只有在有方向 ID 时才获取选题
        } else {
          console.error('无法获取最新方向 ID');
        }
      } else {
        isLoggedIn.value = false;
      }
    } catch (error) {
      console.error('登录验证失败:', error.message);
      isLoggedIn.value = false;
    }
  } else {
    isLoggedIn.value = false;
  }
}

// 获取选题方向及描述
async function fetchDirections() {
  try {
    const response = await api.get('/directions', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('authToken')}` }
    });
    if (response.status === 200 && response.data.length > 0) {
      directions.value = response.data;
      const lastDirection = directions.value[directions.value.length - 1];
      latestDirection.value = {
        direction_name: lastDirection.direction_name || '最新一期',
        description: lastDirection.description || '暂无描述',
        direction_id: lastDirection.direction_id
      };
      // console.log('最新选题方向:', latestDirection.value);
    } else {
      console.error('获取选题方向失败或没有方向数据');
    }
  } catch (error) {
    console.error('获取选题方向失败:', error.message);
  }
}

// 根据最新方向ID获取选题
async function fetchTopics() {
  if (!latestDirection.value.direction_id) {
    console.error('Direction ID is not set');
    return;
  }

  // console.log('当前方向 ID:', latestDirection.value.direction_id);

  try {
    const response = await api.get('/topics/current', {
      params: {
        direction: latestDirection.value.direction_id
      }
    });

    if (response.status === 200) {
      topics.value = response.data;
      topics.value.forEach(topic => {
        submissionLinks.value[topic.topic_id] = topic.submission_link || '';
      });
    } else {
      console.error('获取选题失败:', response.statusText);
    }
  } catch (error) {
    console.error('获取选题失败:', error.message);
  }
}




// 当前用户已认领的选题
const myClaimedTopics = computed(() => {
  if (!currentUser.value) {
    return []; // 或者返回一个包含默认值的数组
  }
  // 过滤出由当前用户认领的选题
  return topics.value.filter(topic => {
    return (String(topic.claimed_by) === String(currentUser.value.user_id)) ||
        (topic.claimed_by === currentUser.value.username);
  });
});

// 其他用户已认领的选题
const otherClaimedTopics = computed(() => {
  if (!currentUser.value) {
    return []; // 或者返回一个包含默认值的数组
  }
  return topics.value.filter(topic => {
    return topic.claimed_by &&
        (String(topic.claimed_by) !== String(currentUser.value.user_id)) &&
        (topic.claimed_by !== currentUser.value.username);
  });
});

// 未认领的选题
const unclaimedTopics = computed(() => {
  return topics.value.filter(topic => !topic.claimed_by);
});




// 取消认领选题
async function cancelClaim(topic_id) {
  const token = localStorage.getItem('authToken');
  if (!token) {
    showMessage('未找到Token，请先登录', 'error');
    return;
  }

  try {
    const response = await api.put(`/topics/${topic_id}`, {
      claimed_by: null,
      status: '待认领'
    }, {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    if (response.status === 200) {
      await fetchTopics(); // 刷新选题列表
      showMessage('取消认领成功！', 'success');
    } else {
      showMessage('取消认领失败: ' + response.statusText, 'error');
    }
  } catch (error) {
    showMessage('取消认领失败: ' + error.message, 'error');
  }
}



// 添加选题
async function addTopic() {
  const token = localStorage.getItem('authToken');
  if (!token) {
    showMessage('未找到Token，请先登录', 'error');
    return;
  }

  // 检查标题和描述的非空及字符长度
  if (!newTopic.value.title || newTopic.value.title.length < 5) {

    showMessage('选题标题不能为空，且不少于5个字符。', 'error');
    alert("选题描述不能为空，且不少于5个字符。")
    return;
  }

  if (!newTopic.value.description || newTopic.value.description.length < 10) {
    showMessage('选题描述不能为空，且不少于10个字符。', 'error');
    alert("选题描述不能为空，且不少于10个字符。")
    return;
  }
  if (!latestDirection.value.direction_id || isNaN(latestDirection.value.direction_id)) {
    showMessage('无效的最新方向 ID', 'error');
    return;
  }

  try {
    const response = await api.post('/topics', {
      direction_id: latestDirection.value.direction_id,
      topic_name: newTopic.value.title,
      topic_description: newTopic.value.description,
      proposed_by: currentUser.value.user_id,
      status: '待认领'
    }, {
      headers: { 'Authorization': `Bearer ${token}` }
    });
    alert('添加新选题成功！')

    if (response.status === 201) {
      newTopic.value = { title: '', description: '' };
      await fetchTopics(); // 刷新选题列表
      showMessage('选题提交成功！', 'success');
    } else {
      showMessage('添加选题失败: ' + response.statusText, 'error');
    }
  } catch (error) {
    console.error('API 请求出错:', error); // 添加错误日志
    showMessage('添加选题失败: ' + error.message, 'error');
  }
}

// 提交文章链接
async function submitLink(topic_id) {
  const token = localStorage.getItem('authToken');
  if (!token) {
    showMessage('未找到Token，请先登录', 'error');
    return;
  }

  const link = submissionLinks.value[topic_id];
  if (!link) {
    showMessage('请提供一个有效的文章链接', 'error');
    return;
  }

  const linkPattern = /^https:\/\/cloud\.tencent\.com\/developer\/article\/\d+$/;
  if (!linkPattern.test(link)) {
    alert('文章链接格式不正确，请复制正确的url格式。');
    return;
  }

  try {
    const response = await api.put(`/topics/${topic_id}`, {
      submission_link: link,
      status: '已提交'
    }, {
      headers: { 'Authorization': `Bearer ${token}` }
    });

    if (response.status === 200) {
      submissionLinks.value[topic_id] = ''; // 清空输入框
      await fetchTopics(); // 刷新选题列表
      alert('提交结果成功！', 'success');
    } else {
      alert('提交结果失败: ' + response.statusText, 'error');
    }
  } catch (error) {
    alert('提交结果失败: ' + error.message, 'error');
  }
}


// 认领选题
async function claimTopic(topic_id) {
  const token = localStorage.getItem('authToken');
  if (!token) {
    showMessage('未找到Token，请先登录', 'error');
    return;
  }

  if (myClaimedTopics.value.length >= 2) {
    showMessage('每个用户最多只能认领 2 个选题', 'error');
    alert('每个用户最多只能认领 2 个选题, 可在已认领选题中取消认领');
    return;
  }

  try {
    const response = await api.put(`/topics/${topic_id}`, {
      claimed_by: currentUser.value.user_id,
      status: '已认领'
    }, {
      headers: {'Authorization': `Bearer ${token}`}
    });

    if (response.status === 200) {
      await fetchTopics(); // 刷新选题列表
      showMessage('选题认领成功！', 'success');
      alert('认领成功！');
    } else {
      showMessage('认领选题失败: ' + response.statusText, 'error');
    }
  } catch (error) {
    showMessage('认领选题失败: ' + error.message, 'error');
  }
}

// 点击查看文章跳转
// 添加 openLink 函数
function openLink(link) {
  if (link) {
    window.open(link, '_blank');
  } else {
    console.warn('No link provided');
  }
}

// 使用 onMounted 钩子进行调试
onMounted(async () => {
  try {
    await checkLoginStatus(); // 确保用户登录状态
    await fetchDirections(); // 先获取方向
    if (latestDirection.value.direction_id) {
      await fetchTopics(); // 然后获取选题，只有在有方向 ID 时才获取
    }
    // 获取用户信息
    const userResponse = await api.get('/users/me');
    if (userResponse.status === 200) {
      currentUser.value = userResponse.data;
    }
  } catch (error) {
    console.error("获取数据失败：", error);
  }
});

// 提示信息函数
function showMessage(msg, type) {
  message.value = msg;
  messageType.value = type;

  // 清除消息
  setTimeout(() => {
    message.value = '';
    messageType.value = '';
  }, 3000);
}

</script>

<style lang="scss" scoped>
@import "../assets/TopicList.scss";
</style>
