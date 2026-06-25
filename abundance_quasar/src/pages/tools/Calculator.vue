<template>
  <q-page class="row q-pa-md">
    <q-card class="col-12 q-pa-lg">
      <q-btn label="← 返回工具箱" icon="arrow_back" class="mb-4" @click="$router.push('/')" />
      <h2 class="text-center mb-5">🧮 科学计算器</h2>

      <q-input
        v-model="expression"
        @keyup.enter="calculate"
        placeholder="输入表达式，如 sin(pi/2)+2^3"
        class="mb-4"
        label="计算表达式"
        filled
      />

      <q-btn
        label="计算"
        icon="calculate"
        color="primary"
        class="mb-4"
        @click="calculate"
      />

      <q-card v-if="result !== null" class="q-pa-4 bg-grey-100">
        {{ result }}
      </q-card>

      <q-card class="q-pa-4 mt-4 bg-grey-50">
        <p class="text-caption text-grey-600">
          支持: + - * / % ^ sin cos tan sqrt log abs PI E
        </p>
      </q-card>
    </q-card>
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
