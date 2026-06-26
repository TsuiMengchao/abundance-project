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
        <q-btn
          label="新标签页打开"
          icon="open_in_new"
          @click="openInNewTab"
        />
      </div>

      <h2 v-if="!isFullScreen && tool" class="text-center mb-5">
        {{ tool.icon }} {{ tool.name }}
      </h2>

      <div v-if="!tool" class="text-center q-pa-xl text-red-5">
        未找到对应工具，请检查id参数
      </div>

      <!-- IFrame核心 -->
      <iframe
        v-if="tool"
        :src="tool.src"
        style="width:100%; border:none; border-radius:12px; transition: all 0.2s;"
        :style="iframeStyle"
      />
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useToolStore } from '@/stores/tools-store';
import type { ToolItem } from '@/stores/tools-store';

const route = useRoute();
const $router = useRouter();
const toolStore = useToolStore();
const isFullScreen = ref<boolean>(false);

// 1. 获取url上的id参数 /#/tools/NativeIFrame?id=device-info
const toolId = computed(() => route.query.id as string);

// 2. 根据id从全局工具列表匹配tool
const tool = computed<ToolItem | undefined>(() => {
  if (!toolId.value) return undefined;
  // 本地内置工具 + 云端工具合并查询
  const allTools = [...toolStore.tools, ...toolStore.cloudTools];
  console.log(allTools.find(item => item.id === toolId.value));
  return allTools.find(item => item.id === toolId.value);
});

// 容器样式
const containerStyle = computed(() => {
  return isFullScreen.value ? {
    position: 'fixed',
    top: '0',
    left: '0',
    width: '100vw',
    height: '100vh',
    margin: '0',
    padding: '12px',
    zIndex: '99999',
    background: '#ffffff',
    borderRadius: '0'
  } : {};
});

// IFrame样式
const iframeStyle = computed(() => {
  return isFullScreen.value ? {
    height: 'calc(100vh - 60px)',
    borderRadius: '0'
  } : {
    height: 'calc(100vh - 200px)'
  };
});

// 切换全屏
const toggleFullScreen = () => {
  isFullScreen.value = !isFullScreen.value;
};

// 新标签打开iframe页面
const openInNewTab = () => {
  if (!tool.value) return;
  window.open(tool.value.src);
};
</script>
