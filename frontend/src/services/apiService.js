// src/services/apiService.js
import axios from 'axios';

const apiUrl = process.env.VUE_APP_API_URL || 'http://134.175.170.70:5000';

const api = axios.create({
    baseURL: apiUrl,
    timeout: 5000, // 增加超时时间
});

// 请求拦截器
api.interceptors.request.use(config => {
    // 从 localStorage 获取 Token
    const token = localStorage.getItem('authToken');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, error => {
    return Promise.reject(error);
});

// 响应拦截器
api.interceptors.response.use(
    response => response,
    error => {
        console.error('API Error:', error.response ? error.response.data : error.message);
        return Promise.reject(error);
    }
);

export default api;
