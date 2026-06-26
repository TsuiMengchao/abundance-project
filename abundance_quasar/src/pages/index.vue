<template>
  <q-layout view="lHh Lpr lFf">
    <div>
      <h1 style="font-size:1.8rem; margin-bottom:4px;">🧰 万能工具箱</h1>
      <q-btn
        label="云端配置"
        color="primary"
        icon="cloud_settings"
        size="sm"
        @click="openConfigDialog"
        class="q-mr-sm"
      />
      <p style="color:#64748b; margin-bottom:20px;">全端适配 · 离线/联网智能分类</p>
      <!-- 云端配置按钮 -->

      <!-- 一级标签区域 -->
      <div class="category-tabs">
        <div v-for="cat in currentTabs" :key="cat.key"
             :class="['category-tab', activeTab === cat.key ? 'active' : '']"
             @click="activeTab = cat.key; resetAllFold()">
          {{ cat.label }}
          <span class="badge">{{ getToolCount(cat.key) }}</span>
        </div>
      </div>

      <!-- 独立上下排列分类卡片 -->
      <div class="sub-card-wrap" v-if="subCategoryList.length">
        <div class="sub-card" v-for="cate in subCategoryList" :key="cate.id">
          <!-- 卡片头部 -->
          <div class="sub-card-head" @click="toggleFold(cate.id)">
            <span class="sub-card-name">{{ cate.name }} ({{ getCateToolNum(cate.id) }})</span>
            <span class="fold-icon" :style="{transform: foldMap[cate.id] ? 'rotate(-90deg)' : 'rotate(0deg)'}">▼</span>
          </div>
          <!-- 卡片内容区域，带动效展开收起 -->
          <div class="sub-card-body" :class="{open: !foldMap[cate.id]}">
            <div class="tools-grid">
              <div v-for="tool in getToolsByCate(cate.id)" :key="tool.id"
                   class="tool-card" @click="handleToolClick(tool)">
                <span class="tool-icon">{{ tool.icon }}</span>
                <span class="tool-name">{{ tool.name }}</span>
                <span class="tool-desc">{{ tool.desc }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="filteredTools.length === 0" style="text-align:center; padding:40px; color:#94a3b8;">
        暂无工具
      </div>
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
const toggleFold = (cateId: string) => {
  foldMap.value[cateId] = !foldMap.value[cateId];
};
const resetAllFold = () => {
  Object.keys(foldMap.value).forEach(k => {
    foldMap.value[k] = false;
  });
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

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
  background: #f5f7fb;
  color: #1e293b;
  display: flex;
  justify-content: center;
  min-height: 100vh;
}

/* 响应式容器 */
@media (max-width: 768px) {
  #app {
    padding: 12px;
  }
}

/* 分类导航卡片 */
.category-tabs {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 24px;
}

.category-tab {
  flex: 1 1 auto;
  min-width: 100px;
  padding: 12px 16px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  text-align: center;
  font-weight: 600;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
  user-select: none;
}

.category-tab.active {
  border-color: #3b82f6;
  background: #eff6ff;
  color: #1e40af;
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(59, 130, 246, 0.2);
}

.category-tab .badge {
  display: inline-block;
  background: #e2e8f0;
  color: #475569;
  border-radius: 20px;
  padding: 2px 10px;
  font-size: 0.75rem;
  margin-left: 6px;
  font-weight: 500;
}

/* 工具网格 */
.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 16px;
  margin-top: 8px;
}

@media (max-width: 480px) {
  .tools-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }
}

.tool-card {
  background: white;
  border-radius: 20px;
  padding: 20px 12px;
  text-align: center;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
  transition: 0.2s;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  border: 1px solid rgba(0, 0, 0, 0.03);
}

.tool-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.08);
}

.tool-icon {
  font-size: 2.2rem;
}

.tool-name {
  font-weight: 600;
  font-size: 0.9rem;
  line-height: 1.3;
}

.tool-desc {
  font-size: 0.7rem;
  color: #64748b;
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

/* 二级分类外层容器，上下间距隔开卡片 */
.sub-card-wrap {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
/* 完整独立卡片，白底阴影，不和背景融合 */
.sub-card {
  background: #ffffff;
  border-radius: 14px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  border: 1px solid #e2e8f0;
  overflow: hidden;
}
/* 卡片头部区域 */
.sub-card-head {
  padding: 14px 20px;
  background: #f8fafc;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  user-select: none;
  transition: background 0.2s;
}
.sub-card-head:hover {
  background: #f1f5f9;
}
.sub-card-name {
  font-weight: 500;
  font-size: 15px;
}
.fold-icon {
  font-size: 15px;
  width:24px;
  text-align:center;
  transition: transform 0.25s ease;
}
/* 卡片内容容器，高度过渡实现折叠动效 */
.sub-card-body {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.15s ease, padding 0.15s ease;
}
.sub-card-body.open {
  max-height: 2000px;
  padding: 16px 20px;
}
/* 原有工具网格布局完全不变 */
.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 12px;
}
.tool-card {
  padding: 14px;
  background: #f8fafc;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.tool-icon {
  font-size: 24px;
}
.tool-name {
  font-weight: 500;
}
.tool-desc {
  font-size: 12px;
  color: #64748b;
}

.category-tabs {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  margin-bottom: 24px;
}
.category-tab {
  padding:12px 20px;
  background: #ffffff;
  border:1px solid #e2e8f0;
  border-radius:12px;
  cursor: pointer;
  transition:0.2s;
}
.category-tab.active {
  border-color:#3b82f6;
  background:#eff6ff;
}
.badge {
  font-size:12px;
  background:#e5e7eb;
  padding:2px 6px;
  border-radius:8px;
  margin-left:6px;
}
/* 外层卡片容器垂直排列 */
.sub-card-wrap {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
/* 独立大块分类卡片 白底阴影 区分背景 */
.sub-card {
  background:#fff;
  border-radius:16px;
  box-shadow:0 1px 6px rgba(0,0,0,0.06);
  overflow:hidden;
}
/* 卡片头部区域 */
.sub-card-head {
  padding:16px 20px;
  display:flex;
  justify-content:space-between;
  align-items:center;
  cursor:pointer;
  font-size:16px;
  font-weight:500;
}
.fold-icon {
  font-size:16px;
  transition:transform 0.25s ease;
  color:#555;
}
/* 折叠动画容器 */
.sub-card-body {
  max-height:0;
  overflow:hidden;
  transition:max-height 0.3s ease, padding 0.3s ease;
  padding:0 20px;
}
.sub-card-body.open {
  max-height:3000px;
  padding:0 20px 20px 20px;
}
/* 工具网格布局 */
.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(165px, 1fr));
  gap:16px;
}
.tool-card {
  background:#f7f8fc;
  border-radius:14px;
  padding:20px 12px;
  text-align:center;
  cursor:pointer;
  transition:0.2s;
}
.tool-card:hover {
  background:#eff6ff;
}
.tool-icon {
  font-size:34px;
  display:block;
  margin-bottom:8px;
}
.tool-name {
  font-weight:500;
  font-size:15px;
  display:block;
  margin-bottom:4px;
}
.tool-desc {
  font-size:12px;
  color:#64748b;
}
</style>
