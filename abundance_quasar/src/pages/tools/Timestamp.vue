<template>
  <q-page class="row q-pa-md">
    <div class="tool-page">
      <button class="back-btn" @click="$router.push('/')">← 返回工具箱</button>
      <h2>🕒 时间戳转换</h2>
      <input v-model="timestamp" placeholder="输入Unix时间戳 (秒)" type="number" />
      <button @click="convert">转换</button>
      <div v-if="result" class="result-box">
        <p>本地时间：{{ result.local }}</p>
        <p>UTC时间：{{ result.utc }}</p>
        <p>ISO格式：{{ result.iso }}</p>
      </div>
      <div style="margin-top:16px;">
        <button @click="nowTimestamp">获取当前时间戳</button>
        <span v-if="currentTs" style="margin-left:12px;">当前：{{ currentTs }}</span>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface TimeResult {
  local: string;
  utc: string;
  iso: string;
}

const timestamp = ref<string>('');
const result = ref<TimeResult | null>(null);
const currentTs = ref<number | null>(null);

// 转换时间戳
const convert = () => {
  const ts = parseInt(timestamp.value);
  if (isNaN(ts)) return;

  const date = new Date(ts * 1000);
  result.value = {
    local: date.toLocaleString(),
    utc: date.toUTCString(),
    iso: date.toISOString()
  };
};

// 获取当前时间戳
const nowTimestamp = () => {
  currentTs.value = Math.floor(Date.now() / 1000);
  timestamp.value = currentTs.value.toString();
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
