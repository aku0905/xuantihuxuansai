<template>
  <div class="rewards-container">
    <h1> 积分商城-奖品列表 </h1>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="rewards-grid">
      <div v-for="reward in sortedRewards" :key="reward.reward_id" class="reward-card">
        <img :src="reward.image_url" alt="Reward Image" class="reward-image" v-if="reward.image_url" />
        <h2 class="reward-name">{{ reward.name }}</h2>
        <p class="reward-description">{{ reward.description }}</p>
        <p class="reward-points">所需积分: {{ reward.points_required }}</p>
        <p class="reward-stock" v-if="reward.stock">库存: {{ reward.stock }}</p>  <!-- 添加库存显示 -->
        <p class="reward-stock" v-else>库存不足</p>  <!-- 库存为 0 时的提示 -->
        <!-- 按钮用于兑换奖励，根据用户的积分和奖励的库存状态来决定是否禁用按钮 -->
        <!-- 如果用户积分不足或者奖励库存为0，则按钮被禁用 -->
        <!-- 点击按钮时触发兑换操作 -->
        <!-- 如果用户积分不足，按钮标题显示提示信息 -->
        <button
            :class="{'disabled': userPoints < reward.points_required || reward.stock === 0}"
            @click="handleRedeemClick(reward)"
            :title="userPoints < reward.points_required ? '积分不足，继续写文章积攒积分吧！' : ''"
        >
          马上兑换
        </button>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import api from "@/services/apiService";

export default {
  name: 'RewardsList',
  data() {
    return {
      rewards: [],
      loading: true,
      error: null,
      userPoints: 1000,  // 示例用户积分，实际情况可以从用户数据中获取
    };
  },
  computed: {
    // 对 rewards 按积分排序
    sortedRewards() {
      return this.rewards.slice().sort((a, b) => a.points_required - b.points_required);
    }
  },
  async created() {
    try {
      // 获取存储在 localStorage 中的 token
      const token = localStorage.getItem('authToken');  // 替换为实际存储 token 的方式

      const headers = {
        Authorization: `Bearer ${token}`,  // 添加 token 到请求头
        'Content-Type': 'application/json',
      };

      // 发送请求的时候包含 headers
      const response = await api.get('/rewards',{headers});  // 替换成你的 API URL
      this.rewards = response.data;
    } catch (err) {
      this.error = 'Failed to load rewards';
      console.error(err);
    } finally {
      this.loading = false;
    }
  },
  methods: {
    handleRedeemClick(reward) {
      if (this.userPoints < reward.points_required) {
        alert('积分不足，继续写文章积攒积分吧！');
        return;
      }

      const confirmed = confirm(`兑换需要扣除 ${reward.points_required} 积分，是否确认兑换？`);
      if (confirmed) {
        this.redeemReward(reward.reward_id);
      }
    },
    async redeemReward(rewardId) {
      try {
        // 获取存储在 localStorage 中的 token
        const token = localStorage.getItem('authToken');  // 替换为实际存储 token 的方式

        const headers = {
          Authorization: `Bearer ${token}`,  // 添加 token 到请求头
          'Content-Type': 'application/json',
        };

        // 调用兑换 API
        await api.post(`rewards/${rewardId}/redeem`, { userId: 1 }, { headers });
        alert('奖励兑换成功！');
        // 更新用户积分
        this.userPoints -= this.rewards.find(r => r.reward_id === rewardId).points_required;
      } catch (err) {
        alert('兑换奖励失败。');
        console.error(err);
      }
    }

  }
};
</script>

<style scoped>
  @import "../assets/global.scss";
  button {
    background-color: #007bff !important;
    color: white;
    padding: 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-bottom: 20px;
    display: block;
    width: 100%;
  }
</style>
