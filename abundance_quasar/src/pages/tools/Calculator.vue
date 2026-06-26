<template>
  <q-page class="row q-pa-md">
    <div class="tool-page">
      <button class="back-btn" @click="$router.push('/')">← 返回工具箱</button>
      <h2>🧮 科学计算器</h2>
      <input v-model="expression" @keyup.enter="calculate" placeholder="输入表达式，如 sin(pi/2)+2^3" />
      <button @click="calculate">计算</button>
      <div v-if="result !== null" class="result-box">{{ result }}</div>
      <div style="margin-top:12px; font-size:0.8rem; color:#64748b;">
        支持: + - * / % ^ sin cos tan sqrt log abs PI E
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const expression = ref<string>('');
const result = ref<number | string | null>(null);

const calculate = () => {
  try {
    let expr = expression.value
      .replace(/\^/g, '**')
      .replace(/sin/g, 'Math.sin')
      .replace(/cos/g, 'Math.cos')
      .replace(/tan/g, 'Math.tan')
      .replace(/sqrt/g, 'Math.sqrt')
      .replace(/log/g, 'Math.log10')
      .replace(/ln/g, 'Math.log')
      .replace(/abs/g, 'Math.abs')
      .replace(/PI/g, 'Math.PI')
      .replace(/E/g, 'Math.E');

    // 安全执行表达式（生产环境建议用更安全的方式）
    result.value = eval(expr);
  } catch (e) {
    result.value = '表达式错误';
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
