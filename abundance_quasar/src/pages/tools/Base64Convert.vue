<template>
  <q-page class="flex flex-center">
    <q-card class="col-12 q-pa-lg">
      <q-btn label="← 返回工具箱" icon="arrow_back" class="mb-4" @click="$router.push('/')" />
      <h2 class="text-center mb-5">🔐 Base64 编码转换</h2>

      <q-input
        v-model="content"
        placeholder="请输入要转换的文本或 Base64 字符串"
        class="mb-4"
        label="转换内容"
        filled
        type="textarea"
        rows="4"
      />

      <div class="flex gap-3 mb-4">
        <q-btn
          label="编码 → Base64"
          icon="encode"
          color="primary"
          class="flex-1"
          @click="encode"
        />
        <q-btn
          label="Base64 → 解码"
          icon="decode"
          color="secondary"
          class="flex-1"
          @click="decode"
        />
      </div>

      <q-btn
        v-if="result"
        label="复制结果"
        icon="content_copy"
        color="green"
        class="w-full mb-4"
        @click="copyResult"
      />

      <q-card v-if="result" class="q-pa-4 bg-grey-100 mb-4">
        {{ result }}
      </q-card>

      <q-card v-if="error" class="q-pa-4 bg-red-100 text-red-600">
        {{ error }}
      </q-card>
    </q-card>
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
