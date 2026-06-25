<template>
  <q-page class="row q-pa-md" :style="containerStyle">
    <q-card class="col-12 q-pa-lg">
      <!-- 顶部操作栏 -->
      <div class="flex justify-between items-center mb-4">
        <q-btn
          v-if="!isFullScreen"
          label="← 返回工具箱"
          icon="arrow_back"
          @click="$router.push('/')"
        />
        <q-btn
          label="全屏"
          icon="fullscreen"
          @click="toggleFullScreen"
        />
      </div>

      <h2 v-if="!isFullScreen" class="text-center mb-5">📱 二维码生成 (云端离线)</h2>

      <!-- 缓存状态 -->
      <q-badge v-if="!isFullScreen" :color="cached ? 'green' : 'orange'" class="mb-4">
        <q-icon :name="cached ? 'check_circle' : 'sync'" class="mr-2" />
        {{ cached ? '页面已缓存，可离线使用' : '正在缓存页面资源...' }}
      </q-badge>

      <q-input
        v-model="text"
        placeholder="输入文本或链接"
        class="mb-4"
        label="二维码内容"
        filled
      />

      <q-btn
        label="生成二维码"
        icon="qr_code"
        color="primary"
        class="mb-4"
        @click="generate"
      />

      <q-card v-if="qrData" class="q-pa-4 text-center">
        <img :src="qrData" alt="二维码" style="max-width:280px; width:100%;" />
      </q-card>

      <p v-if="!isFullScreen" class="text-caption mt-2 text-grey-600">
        * 二维码生成完全在本地执行，无需网络。
      </p>
    </q-card>
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
