<template>
  <q-page class="row q-pa-md">
    <div class="tool-page">
      <button class="back-btn" @click="$router.push('/')">← 返回工具箱</button>
      <h2>☁️ 天气查询 (云端联网)</h2>
      <input v-model="city" placeholder="输入城市名称 (英文)" />
      <button @click="fetchWeather">查询天气</button>
      <div v-if="weather" class="result-box">{{ weather }}</div>
      <div v-if="error" class="result-box" style="color:#ef4444;">{{ error }}</div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const city = ref<string>('Beijing');
const weather = ref<string>('');
const error = ref<string>('');

const fetchWeather = async () => {
  error.value = '';
  weather.value = '加载中...';
  try {
    const res = await fetch(`https://wttr.in/${city.value}?format=%C+%t+%w`);
    const text = await res.text();
    weather.value = text;
  } catch (e) {
    error.value = '请求失败，请检查网络';
    weather.value = '';
  }
};
</script>

<style scoped>
/* 工具页面容器 */
.tool-page {
  background: white;
  border-radius: 24px;
  padding: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  margin-top: 12px;
  flex: 1;
}

.back-btn {
  background: none;
  border: none;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 6px;
  color: #3b82f6;
  cursor: pointer;
  margin-bottom: 18px;
  padding: 6px 12px;
  border-radius: 30px;
  transition: 0.2s;
}

.back-btn:hover {
  background: #eff6ff;
}

input,
select,
textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  font-size: 1rem;
  margin: 8px 0;
  background: #f8fafc;
}

button {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 30px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
  font-size: 0.95rem;
}

button:hover {
  background: #2563eb;
}

.result-box {
  background: #f1f5f9;
  padding: 14px;
  border-radius: 14px;
  margin-top: 12px;
  word-break: break-all;
  font-family: monospace;
}
</style>
