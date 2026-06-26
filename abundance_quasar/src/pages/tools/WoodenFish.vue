<template>
  <q-page class="row q-pa-md">
    <div class="tool-page">
      <button class="back-btn" @click="$router.push('/')">← 返回工具箱</button>
      <h2>🪷 电子木鱼</h2>

      <div style="text-align:center; margin:20px 0">
        <div style="font-size:24px; font-weight:bold; margin-bottom:20px">
          功德：{{ count }}
        </div>

        <div
          @click="knock"
          style="font-size:100px; cursor:pointer; transition:0.2s; user-select:none"
          :style="{ transform: isKnock ? 'scale(0.9)' : 'scale(1)' }"
        >
          🪔
        </div>

        <button @click="reset" style="margin-top:20px; background:#ef4444;">
          重置功德
        </button>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

const count = ref<number>(0);
const isKnock = ref<boolean>(false);
let audio: HTMLAudioElement;

// 初始化音频和本地存储
onMounted(() => {
  // 读取本地缓存的功德数
  const savedCount = localStorage.getItem('fish_count');
  if (savedCount) {
    count.value = parseInt(savedCount);
  }

  // 初始化音频
  audio = new Audio(
    'data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmImBze5u+wVRwASe7UAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='
  );
});

// 敲击木鱼
const knock = () => {
  audio.currentTime = 0;
  audio.play().catch(() => {});

  count.value++;
  localStorage.setItem('fish_count', count.value.toString());

  isKnock.value = true;
  setTimeout(() => {
    isKnock.value = false;
  }, 150);
};

// 重置功德
const reset = () => {
  count.value = 0;
  localStorage.setItem('fish_count', '0');
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
