<template>
  <q-page class="flex flex-center">
    <div class="tool-page">
      <button class="back-btn" @click="$router.push('/')">← 返回工具箱</button>
      <h2>🔐 Base64 编码转换</h2>

      <input
        v-model="content"
        placeholder="请输入要转换的文本或 Base64 字符串"
        style="min-height:80px;white-space:pre-wrap;word-break:break-all"
      />

      <div style="display:flex;gap:10px;margin:10px 0">
        <button @click="encode" style="flex:1">编码 → Base64</button>
        <button @click="decode" style="flex:1">Base64 → 解码</button>
      </div>

      <button @click="copyResult" v-if="result" style="background:#10b981;width:100%">
        复制结果
      </button>

      <div v-if="result" class="result-box" style="margin-top:12px;">
        {{ result }}
      </div>
      <div v-if="error" class="result-box" style="color:#ef4444;margin-top:12px;">
        {{ error }}
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const content = ref<string>('');
const result = ref<string>('');
const error = ref<string>('');

// Base64编码
const encode = () => {
  error.value = '';
  if (!content.value) {
    error.value = '请输入内容';
    result.value = '';
    return;
  }

  try {
    result.value = btoa(unescape(encodeURIComponent(content.value)));
  } catch (e) {
    error.value = '编码失败';
    result.value = '';
  }
};

// Base64解码
const decode = () => {
  error.value = '';
  if (!content.value) {
    error.value = '请输入内容';
    result.value = '';
    return;
  }

  try {
    result.value = decodeURIComponent(escape(atob(content.value)));
  } catch (e) {
    error.value = 'Base64 格式无效，解码失败';
    result.value = '';
  }
};

// 复制结果
const copyResult = () => {
  if (!result.value) return;

  navigator.clipboard.writeText(result.value)
    .then(() => {
      window.alert('复制成功！');
    })
    .catch(() => {
      window.alert('复制失败，请手动复制');
    });
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
