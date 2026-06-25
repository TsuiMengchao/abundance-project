<template>
  <q-layout view="lHh Lpr lFf">
    <div class="q-mb-lg flex justify-between items-center">
      <div>
        <h1 class="text-h4 q-mb-xs">🧰 万能工具箱</h1>
        <p class="text-grey-6">全端适配 · 离线/联网智能分类</p>
      </div>
      <!-- 云端配置按钮 -->
      <q-btn
        label="云端配置"
        color="primary"
        icon="cloud_settings"
        size="sm"
        @click="openConfigDialog"
        class="q-mr-sm"
      />
    </div>

    <q-tabs v-model="activeTab" class="q-mb-lg">
      <q-tab
        v-for="tab in currentTabs"
        :key="tab.key"
        :name="tab.key"
        label-class="text-weight-medium"
      >
        <template #default>
          {{ tab.label }}
          <q-badge color="blue-5" class="q-ml-xs">{{ getToolCount(tab.key) }}</q-badge>
        </template>
      </q-tab>
    </q-tabs>

    <div class="row q-col-gutter-md">
      <div class="col-12" v-for="cate in subCategoryList" :key="cate.id">
        <q-card bordered>
          <q-card-section
            class="row items-center justify-between cursor-pointer"
            @click="foldMap[cate.id] = !foldMap[cate.id]"
          >
            <span class="text-subtitle1">
              {{ cate.name }} ({{ getCateToolNum(cate.id) }})
            </span>
            <q-icon
              name="expand_more"
              :style="{ transform: foldMap[cate.id] ? 'rotate(-90deg)' : 'rotate(0deg)' }"
              class="transition-all duration-300"
            />
          </q-card-section>

          <q-slide-transition>
            <q-card-section v-if="!foldMap[cate.id]" class="q-pt-none">
              <div class="row q-col-gutter-md">
                <div
                  class="col-6 col-sm-4 col-md-3 col-lg-2"
                  v-for="tool in getToolsByCate(cate.id)"
                  :key="tool.id"
                >
                  <q-card
                    bordered
                    class="cursor-pointer hover-shadow-lg transition-all"
                    @click="handleToolClick(tool)"
                  >
                    <q-card-section class="text-center">
                      <div class="text-h4 q-mb-xs">{{ tool.icon }}</div>
                      <div class="text-weight-medium text-sm q-mb-xs">{{ tool.name }}</div>
                      <div class="text-caption text-grey-6">{{ tool.desc }}</div>
                    </q-card-section>
                  </q-card>
                </div>
              </div>
            </q-card-section>
          </q-slide-transition>
        </q-card>
      </div>
    </div>

    <div v-if="filteredTools.length === 0" class="text-center q-pa-xl text-grey-5">
      暂无工具
    </div>

    <!-- 云端配置弹窗 -->
    <q-dialog v-model="configDialogOpen">
      <q-card class="q-pa-lg" style="width: 500px; max-width: 90vw;">
        <q-card-section class="q-pb-sm">
          <h3 class="text-h5">云端配置</h3>
          <p class="text-grey-6">配置云端工具库地址，将持久化存储在浏览器中</p>
        </q-card-section>

        <q-card-section class="q-pt-sm">
          <q-input
            v-model="cloudConfig.url"
            label="云端地址"
            placeholder="例如: https://api.example.com/tools"
            type="url"
            filled
            class="q-mb-md"
            :error="urlError"
            error-message="请输入有效的URL地址"
          />
        </q-card-section>

        <q-card-actions align="right" class="q-pt-sm">
          <q-btn label="取消" @click="configDialogOpen = false" />
          <q-btn
            label="保存配置"
            color="primary"
            @click="saveCloudConfig"
            :loading="savingConfig"
            class="q-ml-sm"
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router'
import { useToolStore, tabsWeb, tabsApplication, ServerConfig, isMobileApp } from '@/stores/tools-store'
import type { ToolItem, CategoryItem, TabItem } from '@/stores/tools-store'

// 全局仓库
const toolStore = useToolStore()
const $router = useRouter()

// 页面本地状态
const activeTab = ref<string>('');
const foldMap = ref<Record<string, boolean>>({});

// 云端配置相关状态
const configDialogOpen = ref(false)
const savingConfig = ref(false)
const urlError = ref(false)

const cloudConfig = ref<ServerConfig>({
  url: '',
})

// 初始化默认标签（无需请求，仅赋值）
const appMode = isMobileApp()
activeTab.value = appMode ? 'local-offline' : 'offline'

// 初始化云端配置
onMounted(() => {
  cloudConfig.value = toolStore.serverConfig
})

// 打开配置弹窗
const openConfigDialog = () => {
  configDialogOpen.value = true
  // 重置错误状态
  urlError.value = false
}

// 验证URL格式
const validateUrl = (url: string): boolean => {
  if (!url) return false
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

// 保存云端配置
const saveCloudConfig = async () => {
  // 验证URL
  if (cloudConfig.value.url && !validateUrl(cloudConfig.value.url)) {
    urlError.value = true
    return
  }

  savingConfig.value = true

  try {
    toolStore.saveServerConfig(cloudConfig.value)

    // 可以在这里添加调用云端接口验证地址的逻辑
    // 例如: await toolStore.syncCloudTools(cloudConfig.value.url)
    // 关闭弹窗
    configDialogOpen.value = false
  } catch (error) {
    console.error('保存云端配置失败:', error)
    // 可以添加错误提示
  } finally {
    savingConfig.value = false
  }
}

const currentTabs = computed<TabItem[]>(() => {
  return appMode ? tabsApplication : tabsWeb;
});

// 筛选当前tab工具
const filteredTools = computed<ToolItem[]>(() => {
  const tabKey = activeTab.value;
  let list: ToolItem[] = [];
  if (appMode) {
    const localTabMap = { 'local-offline': 'offline', 'local-online': 'online' };
    const cloudTabMap = { 'cloud-offline': 'offline', 'cloud-online': 'online' };
    if (['local-offline', 'local-online'].includes(tabKey)) {
      list = toolStore.tools.filter(t => t.tab === localTabMap[tabKey as keyof typeof localTabMap]);
    } else {
      list = toolStore.cloudTools.filter(t => t.tab === cloudTabMap[tabKey as keyof typeof cloudTabMap]);
    }
  } else {
    list = toolStore.tools.filter(t => t.tab === tabKey);
  }
  return list;
});

// 过滤有工具的分类
const subCategoryList = computed<CategoryItem[]>(() => {
  const toolList = filteredTools.value;
  const existCatIds = [...new Set(toolList.map(item => item.category).filter(Boolean))];
  let sourceCats = [...toolStore.categories];
  sourceCats = sourceCats.filter(c => existCatIds.includes(c.id));
  return sourceCats.sort((a, b) => a.rank - b.rank);
});

// 获取tab总数
const getToolCount = (tabKey: string) => {
  if (appMode) {
    if (tabKey === 'local-offline') return toolStore.tools.filter(t => t.tab === 'offline').length;
    if (tabKey === 'local-online') return toolStore.tools.filter(t => t.tab === 'online').length;
    if (tabKey === 'cloud-offline') return toolStore.cloudTools.filter(t => t.tab === 'offline').length;
    if (tabKey === 'cloud-online') return toolStore.cloudTools.filter(t => t.tab === 'online').length;
  } else {
    return toolStore.tools.filter(t => t.tab === tabKey).length;
  }
  return 0;
};

const getToolsByCate = (cateId: string) => filteredTools.value.filter(item => item.category === cateId);
const getCateToolNum = (cateId: string) => getToolsByCate(cateId).length;

// 跳转逻辑
const handleToolClick = (tool: ToolItem) => {
  if (tool.routePath === '/tools/NativeIFrame' && tool.src) {
    $router.push({
      path: tool.routePath,
      query: { id: tool.id}
    })
  } else {
    $router.push(tool.routePath)
  }
}
</script>
