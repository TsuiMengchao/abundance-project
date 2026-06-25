<template>
  <router-view />
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useToolStore, isMobileApp } from '@/stores/tools-store'

const toolStore = useToolStore()

// 应用初始化仅加载一次所有工具配置
onMounted(async () => {
  await toolStore.loadLocalConfig()
  const appMode = isMobileApp()
  if (appMode) {
    toolStore.loadServerConfig()
    await toolStore.loadCloudData()
  }
})
</script>
