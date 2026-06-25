<template>
  <q-page class="row q-pa-md">
    <q-card class="col-12 q-pa-lg text-center">
      <q-btn label="← 返回工具箱" icon="arrow_back" class="mb-4" @click="$router.push('/')" />
      <h2 class="mb-5">🪷 电子木鱼</h2>

      <div class="text-2xl font-bold mb-6">
        功德：{{ count }}
      </div>

      <div
        @click="knock"
        class="text-9xl cursor-pointer transition-transform"
        :style="{ transform: isKnock ? 'scale(0.9)' : 'scale(1)' }"
        role="button"
      >
        🪔
      </div>

      <q-btn
        label="重置功德"
        icon="refresh"
        color="red"
        class="mt-6"
        @click="reset"
      />
    </q-card>
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
