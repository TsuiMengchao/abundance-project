<template>
  <q-page class="row q-pa-md">
    <div class="tool-page">
      <button class="back-btn" @click="$router.push('/')">← 返回工具箱</button>
      <h2>🌐 IP 查询</h2>
      <div class="network-status">
        <span :class="['status-dot', online ? '' : 'offline']"></span>
        {{ online ? '网络连接正常' : '离线状态，无法查询' }}
      </div>
      <input v-model="ip" placeholder="输入IP地址 (留空查询本机)" />
      <button @click="queryIP" :disabled="!online">查询</button>
      <div v-if="result" class="result-box">{{ result }}</div>
      <div v-if="error" class="result-box" style="color:#ef4444;">{{ error }}</div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

const ip = ref<string>('');
const result = ref<string>('');
const error = ref<string>('');
const online = ref<boolean>(navigator.onLine);

// 监听网络状态变化
const handleOnline = () => online.value = true;
const handleOffline = () => online.value = false;

onMounted(() => {
  window.addEventListener('online', handleOnline);
  window.addEventListener('offline', handleOffline);
});

onUnmounted(() => {
  window.removeEventListener('online', handleOnline);
  window.removeEventListener('offline', handleOffline);
});

// 查询IP信息
const queryIP = async () => {
  error.value = '';
  result.value = '查询中...';

  try {
    const res = await fetch(`https://ipapi.co/${ip.value || ''}/json/`);
    const data = await res.json();
    result.value = JSON.stringify(data, null, 2);
  } catch (e) {
    error.value = '请求失败，请检查网络';
    result.value = '';
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

.result-box {
  background: #f1f5f9;
  padding: 14px;
  border-radius: 14px;
  margin-top: 12px;
  word-break: break-all;
  font-family: monospace;
}

.network-status {
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 12px;
  color: #64748b;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #22c55e;
}

.status-dot.offline {
  background: #ef4444;
}
</style>
