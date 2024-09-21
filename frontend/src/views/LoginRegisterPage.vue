<template>
  <div class="login-register-container">
    <h1>Register/Login Page</h1>
    <h2>{{ isLogin ? '登录' : '注册' }}</h2>
    <button @click="toggleForm">{{ isLogin ? '去注册' : '去登录' }}</button>

    <form @submit.prevent="handleSubmit">
      <!-- 登录时显示用户名和密码 -->
      <div v-if="isLogin" class="form-group">
        <div class="form-row">
          <label for="login-username">用户名:</label>
          <input type="text" id="login-username" v-model="form.username" required>
        </div>
        <div class="form-row">
          <label for="login-password">密码:</label>
          <input type="password" id="login-password" v-model="form.password" required>
        </div>
        <span v-if="loginError" class="error">{{ loginError }}</span>
      </div>

      <!-- 注册时显示额外信息 -->
      <div v-if="!isLogin" class="form-group">
        <div class="form-row">
          <label for="register-username">用户名:</label>
          <input type="text" id="register-username" v-model="registerForm.username" required>
        </div>
        <div class="form-row">
          <label for="register-password">密码:</label>
          <input type="password" id="register-password" v-model="registerForm.password" required>
        </div>
<!--        <div class="form-row">-->
<!--          <label for="name">姓名:</label>-->
<!--          <input type="text" id="recipient_name" v-model="registerForm.recipient_name" required>-->
<!--        </div>-->
<!--        <div class="form-row">-->
<!--          <label for="phone">电话:</label>-->
<!--          <input type="tel" id="phone_number" v-model="registerForm.phone_number" required>-->
<!--        </div>-->
<!--        <div class="form-row">-->
<!--          <label for="address">地址:</label>-->
<!--          <input type="text" id="address" v-model="registerForm.address" required>-->
<!--        </div>-->
      </div>

      <button type="submit">{{ isLogin ? '登录' : '注册' }}</button>
      <span v-if="formError" class="error">{{ formError }}</span>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router'; // 导入路由
import api from '../services/apiService'; // 直接导入 apiService

const isLogin = ref(true);
const form = ref({
  username: '',
  password: ''
});
const registerForm = ref({
  username: '',
  password: '',
  // recipient_name: '',
  // phone_number: '',
  // address: ''
});
const formError = ref(null);
const loginError = ref(null);
const router = useRouter();

function toggleForm() {
  isLogin.value = !isLogin.value;
}

async function handleSubmit() {
  formError.value = null;
  loginError.value = null;

  try {
    if (isLogin.value) {
      // 使用 api 进行请求
      const response = await api.post('/users/login', form.value);
      if (!response.data) throw new Error('登录失败，请检查用户名和密码');
      localStorage.setItem('authToken', response.data.token);
      router.push('/home'); // 跳转到首页
    } else {
      // 使用 api 进行请求
      const response = await api.post('/users', registerForm.value);
      if (!response.data) throw new Error('注册失败，请检查输入信息');
      console.log('注册成功:', response.data);
      alert('注册成功，请登录');
      toggleForm();
    }
  } catch (error) {
    if (isLogin.value) {
      loginError.value = error.message;
    } else {
      formError.value = error.message;
    }
  }
}
</script>

<style scoped>
.login-register-container {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: center; /* 居中对齐整个卡片的内容 */
}

h1, h2 {
  margin-bottom: 20px;
}

button {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-bottom: 20px;
}

button:hover {
  background-color: #0056b3;
}

form {
  display: flex;
  flex-direction: column;
  align-items: center; /* 表单内容水平居中 */
}

.form-group {
  width: 100%;
}

.form-row {
  display: flex;
  align-items: center;
  width: 100%;
  margin-bottom: 15px;
}

label {
  flex: 0 0 120px; /* 固定标签宽度 */
  margin-right: 10px; /* 标签和输入框之间的间距 */
  text-align: right; /* 标签右对齐 */
}

input {
  flex: 1; /* 输入框占用剩余空间 */
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>
