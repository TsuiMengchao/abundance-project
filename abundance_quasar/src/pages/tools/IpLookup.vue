<template>
  <q-page class="row q-pa-md">
    <q-card class="col-12 q-pa-lg">
      <q-btn label="← 返回工具箱" icon="arrow_back" class="mb-4" @click="$router.push('/')" />
      <h2 class="text-center mb-5">🌐 IP 查询</h2>

      <!-- 网络状态 -->
      <q-badge :color="online ? 'green' : 'red'" class="mb-4">
        <q-icon :name="online ? 'wifi' : 'wifi_off'" class="mr-2" />
        {{ online ? '网络连接正常' : '离线状态，无法查询' }}
      </q-badge>

      <q-input
        v-model="ip"
        placeholder="输入IP地址 (留空查询本机)"
        class="mb-4"
        label="IP地址"
        filled
      />

      <q-btn
        label="查询"
        icon="public"
        color="primary"
        class="mb-4"
        @click="queryIP"
        :disabled="!online"
      />

      <q-card v-if="result" class="q-pa-4 bg-grey-100">
        <pre>{{ result }}</pre>
      </q-card>

      <q-card v-if="error" class="q-pa-4 bg-red-100 text-red-600">
        {{ error }}
      </q-card>
    </q-card>
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
