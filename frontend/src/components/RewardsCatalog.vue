<template>
  <div class="rewards-container">
    <h1>积分商城-奖品列表</h1>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="rewards-grid">
      <div v-for="reward in sortedRewards" :key="reward.reward_id" class="reward-card">
        <img :src="reward.image_url" alt="Reward Image" class="reward-image" v-if="reward.image_url" />
        <h2 class="reward-name">{{ reward.name }}</h2>
        <p class="reward-description">{{ reward.description }}</p>
        <p class="reward-points">所需积分: {{ reward.points_required }}</p>
        <p class="reward-stock" v-if="reward.stock">库存: {{ reward.stock }}</p>
        <p class="reward-stock" v-else>库存不足</p>
        <button1
            :class="{'disabled': userPoints < reward.points_required || reward.stock === 0}"
            @click="handleRedeemClick(reward)"
            :title="userPoints < reward.points_required ? '积分不足，继续写文章积攒积分吧！' : ''"
        >
          马上兑换
        </button1>
      </div>
    </div>
  </div>
</template>

<script>
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
      const token = localStorage.getItem('authToken');
      const headers = {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      };

      const response = await api.get('/rewards', {headers});
      this.rewards = response.data;
    } catch (err) {
      this.error = '加载奖品失败';
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
        const token = localStorage.getItem('authToken');
        const headers = {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        };

        await api.post(`rewards/${rewardId}/redeem`, {userId: 1}, {headers});
        alert('奖励兑换成功！');
        this.userPoints -= this.rewards.find(r => r.reward_id === rewardId).points_required;
      } catch (err) {
        alert('兑换奖励失败。');
        console.error(err);
      }
    }
  }
};
</script>

<style lang="scss" scoped>

@import "../assets/global.scss";

.rewards-container {
  padding: 20px;
}

button1 {
  background-color: #2ecc71; /* 使用绿色作为主色 */
  color: white;
  padding: 10px;
  border: none;
  border-radius: 8px; /* 增加圆角 */
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-bottom: 20px;
  display: block;
  width: 100%;

  &.disabled {
    background-color: grey; /* 禁用状态颜色 */
    cursor: not-allowed;
  }

  &:hover:not(.disabled) {
    background-color: #27ae60; /* 悬停效果，使用深绿色 */
  }
}
</style>



