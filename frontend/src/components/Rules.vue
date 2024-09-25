<template>
  <div class="rules-container">
    <h1>🎉 在线选题互选赛规则介绍</h1>
    <p>欢迎参加我们的选题互选赛！为了确保活动的顺利进行，请仔细阅读以下积分规则和参与方式。</p>

    <h2>📅 活动概述</h2>
    <p>
      每周五，小助理将在群内公布新的选题，为期一周。参与者可以在选题方向中自拟题目进行写作、给他人出题或使用他人出的题目进行写作，均可获得不同的积分（积分会实时更新在个人信息中，每周会有上限）。
    </p>

    <h2>📊 积分统计</h2>
    <table>
      <thead>
      <tr>
        <th>行为</th>
        <th>积分</th>
        <th>备注</th>
      </tr>
      </thead>
      <tbody>
      <tr>
        <td>每周出一个新题目</td>
        <td>+2 积分</td>
        <td>上限 6 积分/每周</td>
      </tr>
      <tr>
        <td>出的题目被选中并完成</td>
        <td>+5 积分</td>
        <td>上限 15 积分/每周</td>
      </tr>
      <tr>
        <td>每周选择一个题目并提交作品</td>
        <td>+15 积分</td>
        <td>上限 15 积分/每周</td>
      </tr>
      </tbody>
    </table>

    <h2>👥 参与者说明</h2>
    <p>
      - <strong>提出者</strong>：出题目的人。<br>
      - <strong>认领人</strong>：选择并提交作品的人。<br>
      - 参与者可以同时作为提出者和认领人。
    </p>

    <h2>🔍 积分行为解析</h2>
    <ol>
      <li>每周出一个新题目：每提供一个新题目，积分+2，积分上限为6分/每周。</li>
      <li>出的题目被选中并完成：若提出的题目被完成，提出者积分+5，积分上限为15分/每周。</li>
      <li>每周选择一个题目并提交作品：完成题目后，认领人积分+15，积分上限为15分/每周。</li>
      <li>同一提交的特殊情况：若完成题目时，出题人和认领人为同一人，提出者积分-7（此前出题积分已+2,题目被完成积分+5）。</li>
    </ol>

    <h2>🏆 积分兑换</h2>
    <p>
      积分可用于兑换奖品。请访问页面的“积分商城”选择兑换，兑换后将扣除相应积分。
    </p>

    <h2>⚠️ 温馨提示</h2>
    <p>
      提交作品时，请附上正确链接【验证格式：https://cloud.tencent.com/developer/article/{column}，column为文章编号，正常打开文章复制url即可】，以便积分统计顺利进行。希望大家积极参与，祝您在活动中取得好成绩！
    </p>
  </div>
</template>

<style scoped lang="scss">
.rules-container {
  max-width: 1200px; /* 添加最大宽度 */
  margin: 20px auto; /* 居中 */
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f5f7fa; /* 与其他页面背景统一 */
  font-family: Arial, sans-serif;
  line-height: 1.6;
  text-align: left;
}

h1 {
  color: #2c3e50;
  text-align: center; /* 标题居中 */
}

h2 {
  color: #2980b9;
  margin-top: 20px; /* 增加顶部间距 */
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
}

table, th, td {
  border: 1px solid #ddd;
  padding: 8px;
}

th {
  background-color: #2980b9;
  color: white;
}

ul, ol {
  margin-left: 20px;
}

p {
  word-wrap: break-word; /* 支持旧版浏览器的自动换行 */
  overflow-wrap: break-word; /* 标准方式处理自动换行 */
  word-break: break-all; /* 防止超长单词溢出 */
}
</style>
