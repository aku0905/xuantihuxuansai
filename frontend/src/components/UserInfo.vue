<template>
  <div class="user-info">
    <h2>用户信息</h2>

    <!-- 用户信息展示 -->
    <div v-if="userData" class="user-card">
      <p>用户名: {{ userData.username }}</p>
      <p>剩余积分: {{ userData.availablePoints }}</p>
      <p>总积分: {{ userData.totalPoints }}</p>
<!--      <p>———————</p>-->
<!--      <p>收件姓名: {{ userData.recipient_name }}</p>-->
<!--      <p>收件地址: {{ userData.address }}</p>-->
<!--      <p>手机号: {{ userData.phone_number }}</p>-->


      <!-- 更改个人信息按钮 -->
      <button v-if="!editMode" @click="toggleEditMode">更改密码</button>
    </div>

    <!-- 编辑模式：显示可编辑表单 -->
    <div v-if="editMode" class="edit-form">
      <form @submit.prevent="updateUserInfo">
<!--        <label for="recipient_name">收件人姓名:</label>-->
<!--        <input v-model="formData.recipient_name" id="recipient_name" placeholder="留空表示不修改">-->

<!--        <label for="address">收件地址:</label>-->
<!--        <input v-model="formData.address" id="address" placeholder="留空表示不修改">-->

<!--        <label for="phone_number">手机号:</label>-->
<!--        <input v-model="formData.phone_number" id="phone_number" placeholder="留空表示不修改">-->

        <label for="password">新密码:</label>
        <div class="password-input">
          <input :type="passwordVisible ? 'text' : 'password'" v-model="formData.password" id="password" placeholder="留空表示不修改">
          <span @click="togglePasswordVisibility">{{ passwordVisible ? '🙈' : '👁️' }}</span>
        </div>

        <label for="confirm_password">确认新密码:</label>
        <div class="password-input">
          <input :type="passwordVisible ? 'text' : 'password'" v-model="formData.confirm_password" id="confirm_password" placeholder="再输入一次密码">
        </div>

        <button type="submit">保存（注销后重新登录）</button>
        <button @click="toggleEditMode">取消</button>
      </form>
    </div>

    <!-- 加载提示 -->
    <div v-else-if="!userData">
      <p>正在加载用户信息...</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/apiService';
import { useRouter } from 'vue-router'; // 导入路由以便跳转

const userData = ref(null);
const editMode = ref(false); // 控制是否显示编辑表单
const passwordVisible = ref(false); // 控制密码的可见性
const formData = ref({
  // recipient_name: '',
  // address: '',
  // phone_number: '',
  password: '', // 新密码
  confirm_password: '' // 确认密码
});
const router = useRouter(); // 用于跳转

// 切换编辑模式
function toggleEditMode() {
  editMode.value = !editMode.value;
}

// 切换密码可见性
function togglePasswordVisibility() {
  passwordVisible.value = !passwordVisible.value;
}

// 获取用户数据
async function fetchUserData() {
  try {
    const token = localStorage.getItem('authToken');
    const response = await api.get('/users/me', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    userData.value = response.data;
  } catch (error) {
    console.error('获取用户数据失败:', error);
  }
}

// 提交更新用户信息的表单
async function updateUserInfo() {
  // 验证密码输入是否一致
  if (formData.value.password && formData.value.password !== formData.value.confirm_password) {
    alert('两次密码输入不一致，请重新输入');
    return;
  }

  const token = localStorage.getItem('authToken');

  // 仅发送不为空的字段
  const updatedData = {};
  // if (formData.value.recipient_name) {
  //   updatedData.recipient_name = formData.value.recipient_name;
  // }
  // if (formData.value.address) {
  //   updatedData.address = formData.value.address;
  // }
  // if (formData.value.phone_number) {
  //   updatedData.phone_number = formData.value.phone_number;
  // }
  if (formData.value.password) {
    updatedData.password = formData.value.password;
  }

  try {
    const response = await api.put(`/users/${userData.value.user_id}`, updatedData, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    if (response.status === 200) {
      alert('用户信息更新成功！请重新登录。');
      // 清除本地 token 并跳转到登录页面
      localStorage.removeItem('authToken');
      router.push('/');
    }
  } catch (error) {
    console.error('更新用户信息失败:', error);
  }
}

// 获取用户数据
onMounted(() => {
  fetchUserData();
});
</script>

<style scoped>
.user-info {
  margin: 10px 0;
}

.user-card {
  background-color: #e7e7e7;
  padding: 5px;
  border-radius: 8px;
  margin: 5px 0px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center; /* 让内容水平居中 */
  line-height: 0.2; /* 行高设置为1.2，可以根据需要调整 */
}

.edit-form {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  margin: 0 10px;
  justify-content: center;
  align-items: center;
  display: flex;
  flex-direction: column; /* 让编辑表单和按钮居中 */
}

form {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 5px;
}

input {
  margin-bottom: 15px;
  padding: 8px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.password-input {
  display: flex;
  align-items: center;
}

.password-input input {
  flex: 1;
}

.password-input span {
  cursor: pointer;
  margin-left: 10px;
}

button {
  padding: 10px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-bottom: 10px;
  align-items: center;
}

button:hover {
  background-color: #218838;
}
</style>
