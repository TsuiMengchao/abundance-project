import { defineStore } from 'pinia'
import {Ref, UnwrapRef} from "vue";

export interface ToolItem {
  id: string
  name: string
  icon: string
  desc: string
  tab: 'offline' | 'online'
  category: string
  routePath: string
  src?: string
}
export interface CategoryItem {
  id: string
  name: string
  rank: number
}
export interface TabItem {
  key: string
  label: string
  desc: string
}
export interface ServerConfig {
  url: string
}
interface LocalConfigResp {
  categories: CategoryItem[]
  tools: ToolItem[]
}

export const useToolStore = defineStore('tool', {
  state: () => ({
    // 本地存储key
    CLOUD_CONFIG_STORAGE_KEY: 'toolbox_cloud_config',
    // 本地内置工具（/config/tools.json）
    tools: [] as ToolItem[],
    categories: [] as CategoryItem[],
    // 云端远程工具（/public/tools.json）
    cloudTools: [] as ToolItem[],
    cloudCategories: [] as CategoryItem[],
    serverConfig: {} as ServerConfig,
    // 加载标记，防止重复请求
    loadedLocal: false,
    loadedCloud: false
  }),
  actions: {
    // 加载本地配置，仅首次执行
    async loadLocalConfig() {
      if (this.loadedLocal) return
      try {
        const res = await fetch('/config/tools.json')
        if (!res.ok) throw new Error('本地配置加载失败')
        const data: LocalConfigResp = await res.json()
        this.tools = data.tools
        this.categories = data.categories
        this.loadedLocal = true
      } catch (err) {
        console.error('加载 /config/tools.json 失败', err)
        this.tools = []
        this.categories = []
      }
    },
    // 加载云端配置，仅首次执行
    async loadCloudData() {
      if (this.loadedCloud) return
      try {
        const res = await fetch(this.serverConfig.url+'/config/tools.json')
        if (!res.ok) throw new Error('云端工具加载失败')
        const json = await res.json()
        this.cloudCategories = json.categories || []
        this.cloudTools = (json.tools || []).map((item: ToolItem) => ({
          ...item,
          id: 'cloud-'+item.id,
          src: item.routePath==='/tools/NativeIFrame' ? this.serverConfig.url+item.src : vitem.routePath,
          routePath: '/tools/NativeIFrame?id=cloud-' + item.id,
        }))
        this.loadedCloud = true
      } catch (err) {
        console.warn('云端工具加载失败', err)
        this.cloudCategories = []
        this.cloudTools = []
      }
    },
    // 加载本地存储的云端配置
    loadServerConfig() {
      try {
        const savedConfig = localStorage.getItem(this.CLOUD_CONFIG_STORAGE_KEY)
        if (savedConfig) {
          this.serverConfig = JSON.parse(savedConfig)
        }
      } catch (error) {
        console.error('加载云端配置失败:', error)
      }
    },
    saveServerConfig(serverConfig: ServerConfig) {
      // 持久化到localStorage
      localStorage.setItem(
        this.CLOUD_CONFIG_STORAGE_KEY,
        JSON.stringify(serverConfig)
      )

      this.serverConfig = serverConfig

      // 可以在这里添加调用云端接口验证地址的逻辑
      // 例如: await toolStore.syncCloudTools(cloudConfig.value.url)

      // 提示成功（如果有全局提示组件可以使用）
      console.log('云端配置保存成功')

      // 如果需要，可以触发工具数据重新加载
      // toolStore.loadCloudTools(cloudConfig.value.url)
    }
  }
})

// 公共常量，可全局导入使用
export const tabsWeb: TabItem[] = [
  { key: 'offline', label: '离线工具', desc: '云端加载·可缓存离线' },
  { key: 'online', label: '联网工具', desc: '云端加载·全程联网' }
]
export const tabsApplication: TabItem[] = [
  { key: 'local-offline', label: '本地离线', desc: '内置页面·断网可用' },
  { key: 'local-online', label: '本地联网', desc: '内置页面·需联网' },
  { key: 'cloud-offline', label: '云端离线', desc: '云端加载·可缓存离线' },
  { key: 'cloud-online', label: '云端联网', desc: '云端加载·全程联网' }
]
export const isMobileApp = () => {
  if (window.__NATIVE__ || window.electron || window.uni || window.wx || window.plus) {
    return true;
  }
  return true;
};
