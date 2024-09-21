import api from './apiService';
import axios from 'axios';

// const api = axios.create({
//     baseURL: 'http://134.175.170.70/api',
// });

// 拦截请求，自动在 headers 中添加 Authorization
api.interceptors.request.use(config => {
    const token = localStorage.getItem('authToken');
    if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
});

// 获取存储的 Token
function getToken() {
    return localStorage.getItem('authToken');
}

// 检查用户是否已登录
async function checkLoginStatus() {
    const token = getToken();
    if (token) {
        try {
            const response = await api.get('/users/me');
            if (response.status === 200) {
                return { loggedIn: true, user: response.data };
            } else {
                return { loggedIn: false };
            }
        } catch (error) {
            console.error('登录验证失败:', error.message);
            return { loggedIn: false };
        }
    } else {
        return { loggedIn: false };
    }
}

// 处理用户登录
async function login(username, password) {
    try {
        const response = await api.post('/login', { username, password });
        if (response.status === 200) {
            localStorage.setItem('authToken', response.data.token);
            return { success: true };
        } else {
            return { success: false, message: response.statusText };
        }
    } catch (error) {
        return { success: false, message: error.message };
    }
}

// 处理用户登出
function logout() {
    localStorage.removeItem('authToken');
}

export default {
    getToken,
    checkLoginStatus,
    login,
    api,
    logout
};
