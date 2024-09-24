<template>
  <div class="user-info">
    <h2 class="title">用户信息</h2>

    <div v-if="userData" class="user-card">
      <div class="info-item">
        <i class="fas fa-user"></i>
        <span>用户名: {{ userData.username }}</span>
      </div>
      <div class="info-item">
        <i class="fas fa-coins"></i>
        <span>剩余积分: {{ userData.availablePoints }}</span>
      </div>
      <div class="info-item">
        <i class="fas fa-star"></i>
        <span>总积分: {{ userData.totalPoints }}</span>
      </div>

      <button v-if="!editMode" @click="toggleEditMode" class="edit-button">
        <i class="fas fa-key"></i> 更改密码
      </button>
    </div>

    <div v-if="editMode" class="edit-form">
      <form @submit.prevent="updateUserInfo">
        <div class="form-group">
          <label for="password">新密码:</label>
          <div class="password-input">
            <input
                :type="passwordVisible ? 'text' : 'password'"
                v-model="formData.password"
                id="password"
                placeholder="留空表示不修改"
            >
            <i
                :class="passwordVisible ? 'fas fa-eye-slash' : 'fas fa-eye'"
                @click="togglePasswordVisibility"
            ></i>
          </div>
        </div>

        <div class="form-group">
          <label for="confirm_password">确认新密码:</label>
          <div class="password-input">
            <input
                :type="passwordVisible ? 'text' : 'password'"
                v-model="formData.confirm_password"
                id="confirm_password"
                placeholder="再输入一次密码"
            >
          </div>
        </div>

        <div class="form-actions">
          <button type="submit" class="submit-button">保存</button>
          <button @click="toggleEditMode" class="cancel-button">取消</button>
        </div>
      </form>
    </div>

    <div v-if="!userData" class="loading">
      <i class="fas fa-spinner fa-spin"></i> 正在加载用户信息...
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '../services/apiService';
import { useRouter } from 'vue-router';

const userData = ref(null);
const editMode = ref(false);
const passwordVisible = ref(false);
const formData = ref({
  password: '',
  confirm_password: ''
});
const router = useRouter();

function toggleEditMode() {
  editMode.value = !editMode.value;
  if (!editMode.value) {
    formData.value = { password: '', confirm_password: '' };
  }
}

function togglePasswordVisibility() {
  passwordVisible.value = !passwordVisible.value;
}

async function fetchUserData() {
  try {
    const token = localStorage.getItem('authToken');
    const response = await api.get('/users/me', {
      headers: { Authorization: `Bearer ${token}` },
    });
    userData.value = response.data;
  } catch (error) {
    console.error('获取用户数据失败:', error);
  }
}

async function updateUserInfo() {
  if (formData.value.password && formData.value.password !== formData.value.confirm_password) {
    alert('两次密码输入不一致，请重新输入');
    return;
  }

  const token = localStorage.getItem('authToken');
  const updatedData = {};
  if (formData.value.password) {
    updatedData.password = formData.value.password;
  }

  try {
    const response = await api.put(`/users/${userData.value.user_id}`, updatedData, {
      headers: { Authorization: `Bearer ${token}` },
    });
    if (response.status === 200) {
      alert('密码更新成功！请重新登录。');
      localStorage.removeItem('authToken');
      router.push('/');
    }
  } catch (error) {
    console.error('更新用户信息失败:', error);
    alert('更新失败，请稍后再试。');
  }
}

onMounted(() => {
  fetchUserData();
});
</script>

<style lang="scss" scoped>

$primary-color: #3498db;
$secondary-color: #2ecc71;
$background-color: #f5f7fa;
$text-color: #34495e;
$error-color: #e74c3c;

.user-info {
  max-width: 600px;
  margin: 0 auto;
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

.user-card {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  margin-bottom: 20px;
}

.info-item {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  font-size: 1.1rem;

  i {
    width: 25px;
    margin-right: 10px;
    color: $primary-color;
  }
}

.edit-button, .submit-button, .cancel-button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s ease;
}

.edit-button {
  background-color: $primary-color;
  color: white;
  display: block;
  margin: 20px auto 0;

  &:hover {
    background-color: darken($primary-color, 10%);
  }
}

.edit-form {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.form-group {
  margin-bottom: 20px;

  label {
    display: block;
    margin-bottom: 5px;
    color: $text-color;
  }
}

.password-input {
  position: relative;

  input {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 1rem;
  }

  i {
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    cursor: pointer;
    color: $text-color;
  }
}

.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.submit-button {
  background-color: $secondary-color;
  color: white;

  &:hover {
    background-color: darken($secondary-color, 10%);
  }
}

.cancel-button {
  background-color: $error-color;
  color: white;

  &:hover {
    background-color: darken($error-color, 10%);
  }
}

.loading {
  text-align: center;
  color: $text-color;
  font-size: 1.1rem;

  i {
    margin-right: 10px;
    color: $primary-color;
  }
}

@media (max-width: 480px) {
  .user-info {
    padding: 15px;
  }

  .title {
    font-size: 1.5rem;
  }

  .form-actions {
    flex-direction: column;
    gap: 10px;
  }

  .submit-button, .cancel-button {
    width: 100%;
  }
}
</style>