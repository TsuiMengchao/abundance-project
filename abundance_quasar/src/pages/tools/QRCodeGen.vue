<template>
  <q-page class="row q-pa-md">
    <div class="tool-page" :style="containerStyle">
      <!-- 顶部栏：返回 + 全屏按钮 -->
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;">
        <button class="back-btn" @click="$router.push('/')" v-if="!isFullScreen">← 返回工具箱</button>
      </div>

      <h2 v-if="!isFullScreen">📱 二维码生成 (云端离线)</h2>
      <div class="network-status" v-if="!isFullScreen">
        <span :class="['status-dot', cached ? '' : 'offline']"></span>
        {{ cached ? '页面已缓存，可离线使用' : '正在缓存页面资源...' }}
      </div>

      <input v-model="text" placeholder="输入文本或链接" />
      <button @click="generate" style="margin-top:8px;">生成二维码</button>

      <div v-if="qrData" class="result-box" style="text-align:center; margin-top:16px;">
        <img :src="qrData" alt="真实二维码" style="max-width:280px; width:100%;" />
      </div>

      <p style="font-size:0.8rem; margin-top:8px;" v-if="!isFullScreen">* 二维码生成完全在本地执行，无需网络。</p>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
// 需安装 qrcode 包: npm install qrcode
import QRCode from 'qrcode';

const text = ref<string>('');
const qrData = ref<string | null>(null);
const cached = ref<boolean>(true);
const isFullScreen = ref<boolean>(false);

// 全屏样式计算属性
const containerStyle = computed(() => {
  if (isFullScreen.value) {
    return {
      position: 'fixed',
      top: '0',
      left: '0',
      width: '100vw',
      height: '100vh',
      margin: '0',
      padding: '20px',
      zIndex: '99999',
      background: '#ffffff',
      borderRadius: '0'
    };
  }
  return {};
});

// 生成二维码
const generate = () => {
  if (!text.value.trim()) {
    window.alert('请输入内容');
    return;
  }

  QRCode.toDataURL(text.value, {
    width: 280,
    margin: 1,
    color: {
      dark: '#000000',
      light: '#ffffff'
    }
  }, (err, url) => {
    if (err) {
      console.error(err);
      window.alert('生成失败');
      return;
    }
    qrData.value = url;
  });
};

// 监听缓存状态
onMounted(() => {
  if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
    navigator.serviceWorker.controller.postMessage({ type: 'CHECK_CACHE', url: '/cloud-offline/qrcode' });
    navigator.serviceWorker.addEventListener('message', (e) => {
      if (e.data && e.data.type === 'CACHE_STATUS') {
        cached.value = e.data.cached;
      }
    });
  } else {
    cached.value = true;
  }
});

// 切换全屏
const toggleFullScreen = () => {
  isFullScreen.value = !isFullScreen.value;
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
