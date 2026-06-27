<template>
  <q-page class="row q-pa-md">
    <div id="app">
      <div class="header">
        <div class="title">📖 <span>{{ t('appTitle') }}</span></div>
        <button class="btn" @click="toggleRecycleBin" :class="{accent: showRecycleBin}">
          🗑️ {{ showRecycleBin ? t('backToHome') : t('recycleBin') }} ({{ deletedCount }})
        </button>
        <button class="btn accent" @click="addChild(null)" v-if="!showRecycleBin">＋ {{ t('addRoot') }}</button>
        <select class="btn" v-model="viewMode" @change="onViewModeChange">
          <option value="tree">🌳 {{ t('treeView') }}</option>
          <option value="breadcrumb">🧭 {{ t('breadcrumbView') }}</option>
          <option value="flat">📄 {{ t('flatView') }}</option>
        </select>
        <select class="btn" v-model="currentTheme" @change="setTheme">
          <option value="light">☀️ {{ t('lightTheme') }}</option>
          <option value="dark">🌙 {{ t('darkTheme') }}</option>
        </select>
        <select class="btn" v-model="currentLang" @change="setLang">
          <option value="zh-CN">简</option>
          <option value="zh-TW">繁</option>
          <option value="en">EN</option>
        </select>
        <button class="btn" @click="openUserIdModal">👤 {{ currentUserId || 'Set UserID' }}</button>
        <button class="btn" @click="triggerImport">📥 {{ t('import') }}</button>
        <button class="btn" @click="showExportMenu = !showExportMenu">📤 {{ t('export') }}</button>
        <div v-if="showExportMenu" class="modal-overlay" @click.self="showExportMenu=false" style="position:fixed;inset:0;z-index:250;">
          <div class="modal" style="max-width:360px;">
            <h3>{{ t('exportAs') }}</h3>
            <button class="btn" @click="doExport('json')">JSON</button>
            <button class="btn" @click="doExport('xml')">XML</button>
            <button class="btn" @click="doExport('txt')">TXT</button>
            <button class="btn" @click="doExport('yml')">YML</button>
            <button class="btn" @click="doExport('properties')">Properties</button>
            <button class="btn" @click="doExport('excel')">Excel</button>
            <div class="modal-actions"><button class="btn" @click="showExportMenu=false">{{ t('cancel') }}</button></div>
          </div>
        </div>
        <input type="file" ref="importFileInput" style="display:none" @change="handleImportFile" accept=".json,.xml,.txt,.yml,.yaml,.properties,.xlsx,.xls,.csv">
      </div>

      <div class="toolbar">
        <input type="text" class="search-input" v-model="searchQuery" :placeholder="t('searchPlaceholder')" @input="onSearch">
        <span style="font-size:0.8rem;color:var(--text2);" v-if="searchQuery">{{ filteredCount }} {{ t('results') }}</span>
        <span class="sep"></span>
        <span style="font-size:0.75rem;color:var(--text2);">{{ t('totalEntries') }}: {{ allEntries.length }}, {{ t('activeEntries') }}: {{ activeCount }}</span>
      </div>

      <!-- 面包屑导航 (面包屑模式) -->
      <div class="breadcrumb" v-if="viewMode==='breadcrumb' && breadcrumbStack.length>0">
        <span @click="navBreadcrumb(-1)">🏠 {{ showRecycleBin ? t('recycleBin') : t('root') }}</span>
        <template v-for="(bc, idx) in breadcrumbStack" :key="bc.id">
          <span class="sep-bc">›</span>
          <span v-if="idx < breadcrumbStack.length-1" @click="navBreadcrumb(idx)">{{ bc.content }}</span>
          <span v-else class="current-bc">{{ bc.content }}</span>
        </template>
      </div>

      <div class="main-content">
        <div class="entry-list" :class="{recycle: showRecycleBin}" v-if="displayEntries.length > 0">
          <template v-if="viewMode==='tree' || viewMode==='flat'">
            <entry-row-renderer v-for="entry in displayEntries"
                                :key="entry.id"
                                :entry="entry" :depth="0"
                                :is-recycle="showRecycleBin"
                                :force-show="showRecycleBin ? isTopDeleted(entry) : !entry.isDeleted"
                                :expanded-ids="expandedIds"
                                :view-mode="viewMode"
                                :has-any-children-fn="hasAnyChildren"
                                :get-all-children-fn="getAllChildren"
                                :sort-score-fn="sortScore"
                                :is-top-deleted-fn="isTopDeleted"
                                @copy="copyEntry"
                                @add-child="addChild"
                                @edit="editEntry"
                                @history="showHistory"
                                @delete="deleteEntry"
                                @restore="restoreEntry"
                                @update="refreshData">
            </entry-row-renderer>
          </template>
          <template v-if="viewMode==='breadcrumb'">
            <entry-row-renderer v-for="entry in displayEntries" :key="entry.id" :entry="entry" :depth="0"
                                :is-recycle="showRecycleBin"
                                :force-show="true"
                                :breadcrumb-mode="true"
                                :expanded-ids="expandedIds"
                                :view-mode="viewMode"
                                :has-any-children-fn="hasAnyChildren"
                                :get-all-children-fn="getAllChildren"
                                :sort-score-fn="sortScore"
                                :is-top-deleted-fn="isTopDeleted"
                                @copy="copyEntry"
                                @add-child="addChild"
                                @edit="editEntry"
                                @history="showHistory"
                                @delete="deleteEntry"
                                @restore="restoreEntry"
                                @drill="drillDownList"
                                @update="refreshData">
            </entry-row-renderer>
          </template>
        </div>
        <div class="empty-state" v-else>
          <span class="icon">{{ showRecycleBin ? '🗑️' : '📭' }}</span>
          <span>{{ showRecycleBin ? t('emptyRecycle') : breadcrumbStack.length ? t('noChildren') : t('emptyHint') }}</span>
          <button
            class="btn accent"
            v-if="!showRecycleBin"
            @click="addChild(viewMode === 'breadcrumb' && breadcrumbStack.length ? breadcrumbStack.at(-1)!.id : null)"
          >
            ＋ {{ viewMode === 'breadcrumb' && breadcrumbStack.length ? t('addChild') : t('addFirst') }}
          </button>
        </div>
      </div>

      <!-- 编辑模态框 -->
      <div class="modal-overlay" v-if="editModal.visible" @click.self="cancelEditModal">
        <div class="modal">
          <h3>{{ editModal.mode === 'edit' ? t('editEntry') : t('addEntry') }}</h3>
          <textarea v-model="editModal.content" :placeholder="editModal.mode==='add' ? t('multiAddHint') : ''" autofocus></textarea>
          <div class="hint" v-if="editModal.mode==='add'">{{ t('multiAddHint') }}</div>
          <div class="modal-actions">
            <button class="btn accent" @click="submitEditModal">{{ editModal.mode === 'edit' ? t('save') : t('add') }}</button>
            <button class="btn" @click="cancelEditModal">{{ t('cancel') }}</button>
          </div>
        </div>
      </div>

      <!-- 历史模态框 -->
      <div class="modal-overlay" v-if="historyModalVisible" @click.self="historyModalVisible=false">
        <div class="modal" style="max-width:600px;">
          <h3>📜 {{ t('historyFor') }}: {{ historyEntry?.content?.substring(0,40) || '' }}</h3>
          <div class="history-list">
            <div class="history-item" v-for="h in historyEntry?.historyRecords||[]" :key="h.version"
                 :style="{background: 'transparent'}">
              <span class="h-version">v{{ getEntryHistoryVersion(historyEntry, h.id) }}</span>
              <span class="h-content">{{ h.content }}</span>
              <span style="font-size:0.7rem;color:var(--text2);">{{ formatTime(h.timestamp) }}</span>
              <button class="btn btn-small" @click="restoreVersion(historyEntry.id, h.id)">{{ t('restore') }}</button>
            </div>
          </div>
          <div class="modal-actions"><button class="btn" @click="historyModalVisible=false">{{ t('close') }}</button></div>
        </div>
      </div>

      <div class="toast" v-if="toastMsg" @click="toastMsg=''">{{ toastMsg }}</div>

      <!-- 用户ID设置弹窗 -->
      <div class="modal-overlay" v-if="userIdModal.visible" @click.self="closeUserIdModal">
        <div class="modal">
          <h3>👤 Set User ID</h3>
          <input v-model="userIdModal.inputId" placeholder="输入用户ID" style="width:100%;padding:8px;">
          <div class="modal-actions">
            <button class="btn accent" @click="confirmSetUserId">确认</button>
            <button class="btn" @click="closeUserIdModal">{{ t('cancel') }}</button>
          </div>
        </div>
      </div>

      <div class="toast" v-if="toastMsg" @click="toastMsg=''">{{ toastMsg }}</div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted, type ComputedRef } from 'vue'
import { useI18n } from 'vue-i18n'
import * as XLSX from 'xlsx'
import EntryRowRenderer from '@/components/EntryRowRenderer.vue'

// ==================== 类型定义 ====================
interface EntryHistoryItem {
  id: string
  entryId: string
  content: string
  timestamp: number
  userId: string
}

/** 词条复制记录 */
interface EntryCopyItem {
  id: string
  entryId: string
  content: string
  timestamp: number
  userId: string
}

/** 词条主体 */
interface Entry {
  id: string
  parentId: string | null
  content: string
  historyRecords: EntryHistoryItem[]
  copyRecords: EntryCopyItem[]
  isDeleted: boolean
  deletedAt: number | null
  createdAt: number
  updatedAt: number
  userId: string
}

interface EditModalState {
  visible: boolean
  mode: 'add' | 'edit'
  parentId: string | null
  entryId: string | null
  content: string
}

interface UserIdModalState {
  visible: boolean
  inputId: string
}

interface BreadcrumbItem {
  id: string
  content: string
}

// ==================== IndexedDB 封装工具 ====================
const DB_NAME = 'EntryReaderDB'
const DB_VERSION = 1
let dbInstance: IDBDatabase | null = null

/** 初始化数据库与对象仓库 */
const initDB = (): Promise<IDBDatabase> => {
  return new Promise((resolve, reject) => {
    if (dbInstance) return resolve(dbInstance)
    const req = indexedDB.open(DB_NAME, DB_VERSION)
    req.onupgradeneeded = (ev) => {
      const db = (ev.target as IDBOpenDBRequest).result
      // 词条主表
      if (!db.objectStoreNames.contains('entries')) {
        const store = db.createObjectStore('entries', { keyPath: 'id' })
        store.createIndex('idx_parentId', 'parentId')
      }
      // 历史记录子表
      if (!db.objectStoreNames.contains('historyRecords')) {
        const store = db.createObjectStore('historyRecords', { keyPath: 'id' })
        store.createIndex('idx_entryId', 'entryId')
      }
      // 复制记录子表
      if (!db.objectStoreNames.contains('copyRecords')) {
        const store = db.createObjectStore('copyRecords', { keyPath: 'id' })
        store.createIndex('idx_entryId', 'entryId')
      }
    }
    req.onsuccess = (ev) => {
      dbInstance = (ev.target as IDBOpenDBRequest).result
      resolve(dbInstance!)
    }
    req.onerror = () => reject(req.error)
  })
}

/** 工具：剥离history/copyRecords，生成纯净可入库主词条对象（解决Proxy克隆报错） */
const getPureEntry = (e: Entry): Omit<Entry, 'historyRecords' | 'copyRecords'> => ({
  id: e.id,
  parentId: e.parentId,
  content: e.content,
  isDeleted: e.isDeleted,
  deletedAt: e.deletedAt,
  createdAt: e.createdAt,
  updatedAt: e.updatedAt,
  userId: e.userId
})

/** 保存单条主词条（内部自动浅拷贝剥离Vue Proxy） */
const saveEntryToDB = async (entryRaw: Omit<Entry, 'historyRecords' | 'copyRecords'>): Promise<void> => {
  const db = await initDB()
  const entry = { ...entryRaw }
  return new Promise((resolve, reject) => {
    const tx = db.transaction('entries', 'readwrite')
    const store = tx.objectStore('entries')
    store.put(entry)
    tx.oncomplete = () => resolve()
    tx.onerror = () => reject(tx.error)
  })
}

/** 删除单条主词条 */
const deleteEntryFromDB = async (id: string): Promise<void> => {
  const db = await initDB()
  return new Promise((resolve, reject) => {
    const tx = db.transaction('entries', 'readwrite')
    const store = tx.objectStore('entries')
    store.delete(id)
    tx.oncomplete = () => resolve()
    tx.onerror = () => reject(tx.error)
  })
}

/** 批量添加历史记录（每条自动浅拷贝） */
const addHistoryToDB = async (items: EntryHistoryItem[]): Promise<void> => {
  if (!items.length) return
  const db = await initDB()
  return new Promise((resolve, reject) => {
    const tx = db.transaction('historyRecords', 'readwrite')
    const store = tx.objectStore('historyRecords')
    items.forEach(item => store.put({ ...item }))
    tx.oncomplete = () => resolve()
    tx.onerror = () => reject(tx.error)
  })
}

/** 批量添加复制记录（每条自动浅拷贝） */
const addCopyToDB = async (items: EntryCopyItem[]): Promise<void> => {
  if (!items.length) return
  const db = await initDB()
  return new Promise((resolve, reject) => {
    const tx = db.transaction('copyRecords', 'readwrite')
    const store = tx.objectStore('copyRecords')
    items.forEach(item => store.put({ ...item }))
    tx.oncomplete = () => resolve()
    tx.onerror = () => reject(tx.error)
  })
}

/** 全量清空重写（仅初始化导入兜底使用） */
const saveAllToDB = async (entries: Entry[]): Promise<void> => {
  const db = await initDB()
  const tx = db.transaction(['entries', 'historyRecords', 'copyRecords'], 'readwrite')
  const entryStore = tx.objectStore('entries')
  const histStore = tx.objectStore('historyRecords')
  const copyStore = tx.objectStore('copyRecords')

  await Promise.all([
    new Promise(r => entryStore.clear().onsuccess = r),
    new Promise(r => histStore.clear().onsuccess = r),
    new Promise(r => copyStore.clear().onsuccess = r)
  ])

  for (const entry of entries) {
    const entryPure = getPureEntry(entry)
    entryStore.put({ ...entryPure })
    entry.historyRecords.forEach(h => histStore.put({ ...h }))
    entry.copyRecords.forEach(c => copyStore.put({ ...c }))
  }

  await new Promise((res, rej) => { tx.oncomplete = res; tx.onerror = rej })
}

/** 全量读取组装完整词条树（仅页面初始化） */
const loadAllFromDB = async (): Promise<Entry[]> => {
  const db = await initDB()
  const tx = db.transaction(['entries', 'historyRecords', 'copyRecords'], 'readonly')
  const entryStore = tx.objectStore('entries')
  const histStore = tx.objectStore('historyRecords')
  const copyStore = tx.objectStore('copyRecords')

  const entriesPure = await new Promise<Omit<Entry, 'historyRecords' | 'copyRecords'>[]>(res => {
    const req = entryStore.getAll(); req.onsuccess = () => res(req.result)
  })
  const allHistory = await new Promise<EntryHistoryItem[]>(res => {
    const req = histStore.getAll(); req.onsuccess = () => res(req.result)
  })
  const allCopy = await new Promise<EntryCopyItem[]>(res => {
    const req = copyStore.getAll(); req.onsuccess = () => res(req.result)
  })

  const histMap: Record<string, EntryHistoryItem[]> = {}
  const copyMap: Record<string, EntryCopyItem[]> = {}
  allHistory.forEach(h => {
    if (!histMap[h.entryId]) histMap[h.entryId] = []
    histMap[h.entryId].push(h)
  })
  allCopy.forEach(c => {
    if (!copyMap[c.entryId]) copyMap[c.entryId] = []
    copyMap[c.entryId].push(c)
  })

  return entriesPure.map(pure => ({
    ...pure,
    historyRecords: histMap[pure.id] ?? [],
    copyRecords: copyMap[pure.id] ?? []
  }))
}

// ==================== 常量 & 工具函数 ====================
const SETTINGS_KEY = 'entry-reader-settings'
const USER_ID_KEY = 'entry-user-id'
const SEARCH_SIMILARITY_THRESHOLD = 0.25

// UUID生成
const uuid = (): string => 'e_' + Date.now().toString(36) + '_' + Math.random().toString(36).substring(2, 8)

// 实时计算词条当前版本号：历史条数 + 1
const getEntryVersion = (entry: Entry): number => {
  return (entry.historyRecords?.length || 0) + 1
}


// 根据历史记录ID，获取该历史快照对应的旧版本号
const getEntryHistoryVersion = (entry: Entry, historyItemId: string): number => {
  const sorted = [...(entry.historyRecords || [])].sort((a, b) => a.timestamp - b.timestamp)
  return sorted.findIndex(i => i.id === historyItemId) + 1
}

// 编辑距离算法
const levenshteinDistance = (a: string, b: string): number => {
  const m = a.length, n = b.length
  const dp: number[][] = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0))
  for (let i = 0; i <= m; i++) dp[i][0] = i
  for (let j = 0; j <= n; j++) dp[0][j] = j
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      dp[i][j] = Math.min(
        dp[i - 1][j] + 1, dp[i][j - 1] + 1,
        dp[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1)
      )
    }
  }
  return dp[m][n]
}

const similarity = (a: string, b: string): number => {
  const al = a.toLowerCase(), bl = b.toLowerCase()
  if (al.includes(bl) || bl.includes(al)) {
    return 0.7 + Math.min(al.length, bl.length) / Math.max(al.length, bl.length) * 0.3
  }
  const len = Math.max(al.length, bl.length)
  if (len === 0) return 1
  return 1 - levenshteinDistance(al, bl) / len
}

// XML特殊字符转义
const escapeXml = (str: string): string => str
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')

// ==================== i18n ====================
const { t, locale } = useI18n()

// ==================== 响应式状态 ====================
const currentUserId = ref<string>('')
const userIdModal = ref<UserIdModalState>({ visible: false, inputId: '' })

const allEntries = ref<Entry[]>([])
const showRecycleBin = ref<boolean>(false)
const viewMode = ref<'tree' | 'breadcrumb' | 'flat'>('tree')
const currentTheme = ref<'light' | 'dark'>('light')
const currentLang = ref<'zh-CN' | 'zh-TW' | 'en'>('zh-CN')
const searchQuery = ref<string>('')
const showExportMenu = ref<boolean>(false)
const historyModalVisible = ref<boolean>(false)
const historyEntry = ref<Entry | null>(null)
const breadcrumbStack = ref<BreadcrumbItem[]>([])
const toastMsg = ref<string>('')
const toastTimer = ref<number | null>(null)
const expandedIds = ref<Set<string>>(new Set())
const importFileInput = ref<HTMLInputElement | null>(null)

const editModal = ref<EditModalState>({
  visible: false, mode: 'add', parentId: null, entryId: null, content: ''
})

// ==================== 计算属性 ====================
const entryMap: ComputedRef<Record<string, Entry>> = computed(() => {
  return Object.fromEntries(allEntries.value.map(e => [e.id, e]))
})

const childrenMap: ComputedRef<Record<string, Entry[]>> = computed(() => {
  const map: Record<string, Entry[]> = {}
  allEntries.value.forEach(e => {
    const key = e.parentId || '__root__'
    if (!map[key]) map[key] = []
    map[key].push(e)
  })
  Object.values(map).forEach(list => list.sort((a, b) => sortScore(b) - sortScore(a)))
  return map
})

const rootEntries = computed(() => (childrenMap.value.__root__ || []).filter(e => !e.isDeleted))
const deletedRootEntries = computed(() => allEntries.value.filter(e => e.isDeleted && isTopDeleted(e)))

// 展示列表主逻辑
const displayEntries = computed((): Entry[] => {
  const entries = allEntries.value
  const cm = childrenMap.value

  // 平铺模式
  if (viewMode.value === 'flat') {
    let list = showRecycleBin.value ? entries.filter(e => e.isDeleted) : entries.filter(e => !e.isDeleted)
    if (searchQuery.value) list = list.filter(e => similarity(e.content, searchQuery.value) > SEARCH_SIMILARITY_THRESHOLD)
    return list.sort((a, b) => sortScore(b) - sortScore(a))
  }

  // 树形模式
  if (viewMode.value === 'tree') {
    if (searchQuery.value) {
      return entries.filter(e => !e.isDeleted && similarity(e.content, searchQuery.value) > SEARCH_SIMILARITY_THRESHOLD)
        .sort((a, b) => sortScore(b) - sortScore(a))
    }
    return showRecycleBin.value ? deletedRootEntries.value : rootEntries.value
  }

  // 面包屑层级模式
  if (viewMode.value === 'breadcrumb') {
    const pid = breadcrumbStack.value.at(-1)?.id || null
    let list = showRecycleBin.value
      ? (pid ? entries.filter(e => e.parentId === pid) : deletedRootEntries.value)
      : (pid ? getChildren(pid) : rootEntries.value)
    if (searchQuery.value) list = list.filter(e => similarity(e.content, searchQuery.value) > SEARCH_SIMILARITY_THRESHOLD)
    return list.sort((a, b) => sortScore(b) - sortScore(a))
  }
  return []
})

const activeCount = computed(() => allEntries.value.filter(e => !e.isDeleted).length)
const deletedCount = computed(() => allEntries.value.filter(e => e.isDeleted).length)
const filteredCount = computed(() => displayEntries.value.length)

// ==================== 公共工具方法 ====================
const sortScore = (e: Entry): number => {
  const age = (Date.now() - e.updatedAt) / 3600000
  const modify = e.historyRecords?.length || 0
  const copy = e.copyRecords?.length || 0
  return 10 / (1 + age * 0.1) + copy * 0.5 + modify * 0.3
}

const getChildren = (pid: string | null): Entry[] =>
  (childrenMap.value[pid || '__root__'] || []).filter(e => !e.isDeleted)

const getAllChildren = (pid: string | null): Entry[] =>
  childrenMap.value[pid || '__root__'] || []

const isTopDeleted = (entry: Entry): boolean => {
  if (!entry.isDeleted) return false
  if (!entry.parentId) return true
  const p = entryMap.value[entry.parentId]
  return !p || !p.isDeleted
}
// 是否存在子节点
const hasAnyChildren = (id: string): boolean => (childrenMap.value[id] || []).length > 0

// 时间格式化
const formatTime = (ts: number): string => {
  if (!ts) return ''
  return new Date(ts).toLocaleString(currentLang.value === 'en' ? 'en-US' : 'zh-CN', {
    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
  })
}

// Toast提示
const showToast = (msg: string): void => {
  toastMsg.value = msg
  if (toastTimer.value) clearTimeout(toastTimer.value)
  toastTimer.value = window.setTimeout(() => toastMsg.value = '', 2500)
}

// 刷新响应式列表
const refreshData = (): void => {
  allEntries.value = [...allEntries.value]
}

// 全量保存兜底（仅导入覆盖场景）
const saveData = async (): Promise<void> => {
  await saveAllToDB(allEntries.value)
}

const loadData = async (): Promise<void> => {
  try {
    allEntries.value = await loadAllFromDB()
  } catch (err) {
    allEntries.value = []
    showToast('数据加载异常，已重置')
  }
}

const saveSettings = (): void => {
  try {
    localStorage.setItem(SETTINGS_KEY, JSON.stringify({
      theme: currentTheme.value, lang: currentLang.value, viewMode: viewMode.value
    }))
    localStorage.setItem(USER_ID_KEY, currentUserId.value)
  } catch {}
}

const loadSettings = (): void => {
  try {
    const raw = localStorage.getItem(SETTINGS_KEY)
    if (raw) {
      const s = JSON.parse(raw)
      if (s.theme) currentTheme.value = s.theme
      if (s.lang) { currentLang.value = s.lang; locale.value = s.lang }
      if (s.viewMode) viewMode.value = s.viewMode
    }
    currentUserId.value = localStorage.getItem(USER_ID_KEY) || 'anonymous'
  } catch {}
  setTheme()
}

// 主题切换
const setTheme = (): void => {
  document.documentElement.setAttribute('data-theme', currentTheme.value)
  saveSettings()
}
// 语言切换
const setLang = (): void => {
  locale.value = currentLang.value
  saveSettings()
}

// ========== 用户ID弹窗逻辑 ==========
const openUserIdModal = () => {
  userIdModal.value.inputId = currentUserId.value
  userIdModal.value.visible = true
}

const confirmSetUserId = () => {
  const val = userIdModal.value.inputId.trim()
  currentUserId.value = val
  saveSettings()
  userIdModal.value.visible = false
  showToast(`用户ID已设置：${val || '空'}`)
}

const closeUserIdModal = () => {
  userIdModal.value.visible = false
}

// 复制词条
const copyEntry = async (entryId: string): Promise<void> => {
  const entry = entryMap.value[entryId]
  if (!entry || !currentUserId.value) return showToast('请先设置用户ID')

  const now = Date.now()
  const copyRecord: EntryCopyItem = {
    id: uuid(), entryId: entry.id, content: entry.content, timestamp: now, userId: currentUserId.value
  }

  try { await navigator.clipboard.writeText(entry.content) }
  catch {
    const ta = document.createElement('textarea')
    ta.value = entry.content; document.body.appendChild(ta)
    ta.select(); document.execCommand('copy'); document.body.removeChild(ta)
  }

  entry.copyRecords.push(copyRecord)
  await addCopyToDB([copyRecord])
  showToast('📋 ' + t('copied'))
}

// 新增词条弹窗
const addChild = (parentId: string | null): void => {
  if (!currentUserId.value) return showToast('请先设置用户ID')
  editModal.value = { visible: true, mode: 'add', parentId, entryId: null, content: '' }
}

const editEntry = (entryId: string): void => {
  if (!currentUserId.value) return showToast('请先设置用户ID')
  const e = entryMap.value[entryId]
  if (!e) return
  editModal.value = { visible: true, mode: 'edit', parentId: null, entryId, content: e.content }
}

const cancelEditModal = (): void => {
  editModal.value.visible = false
}

// 提交新增/编辑
const submitEditModal = async (): Promise<void> => {
  const { mode, parentId, entryId, content } = editModal.value
  const trim = content.trim()
  if (!trim) return showToast('内容不能为空')

  const now = Date.now()
  if (mode === 'add') {
    const lines = trim.split('\n\n').filter(l => l.trim())
    const added: Entry[] = lines.map(line => ({
      id: uuid(), parentId, content: line.trim(),
      historyRecords: [], copyRecords: [], isDeleted: false, deletedAt: null,
      createdAt: now, updatedAt: now, userId: currentUserId.value
    }))
    allEntries.value.push(...added)
    // 逐条提取纯净对象入库
    for (const e of added) {
      await saveEntryToDB(getPureEntry(e))
    }
    showToast(`${t('saved')} (${added.length})`)
  } else {
    const entry = entryMap.value[entryId!]
    if (!entry) return
    if (trim === entry.content) {
      showToast(t('contentUnchanged'))
      editModal.value.visible = false
      return
    }
    // 生成历史记录
    const hist: EntryHistoryItem = {
      id: uuid(), entryId: entry.id, content: entry.content, timestamp: now, userId: currentUserId.value
    }
    entry.historyRecords.push(hist)
    entry.content = trim
    entry.updatedAt = now
    // 纯净词条入库 + 历史记录入库
    await Promise.all([
      saveEntryToDB(getPureEntry(entry)),
      addHistoryToDB([hist])
    ])
    showToast(`${t('saved')} v${getEntryVersion(entry)}`)
  }
  editModal.value.visible = false
  refreshData()
}

// 删除词条
const deleteEntry = async (id: string): Promise<void> => {
  const e = entryMap.value[id]
  if (!e || !confirm(`${t('confirmDelete')}\n\n${e.content.substring(0, 60)}`)) return
  e.isDeleted = true
  e.deletedAt = Date.now()
  e.updatedAt = Date.now()
  await saveEntryToDB(getPureEntry(e))
  showToast('🗑️ ' + t('deleted'))
  refreshData()
}

// 恢复词条
const restoreEntry = async (id: string): Promise<void> => {
  const e = entryMap.value[id]
  if (!e || !e.isDeleted) return
  e.isDeleted = false
  e.deletedAt = null
  e.updatedAt = Date.now()
  await saveEntryToDB(getPureEntry(e))
  showToast('♻️ ' + t('restored'))
  refreshData()
}

// 打开历史弹窗
const showHistory = (id: string): void => {
  historyEntry.value = entryMap.value[id]
  historyModalVisible.value = true
}

// 回滚历史版本
const restoreVersion = async (entryId: string, historyItemId: string): Promise<void> => {
  const e = entryMap.value[entryId]
  if (!e) return
  const hist = e.historyRecords.find(h => h.id === historyItemId)
  if (!hist) return

  const now = Date.now()
  // 当前内容存入历史
  const newHist: EntryHistoryItem = {
    id: uuid(), entryId: e.id, content: e.content, timestamp: now, userId: currentUserId.value
  }
  e.historyRecords.push(newHist)
  // 回滚内容
  e.content = hist.content
  e.updatedAt = now
  // 入库
  await Promise.all([
    saveEntryToDB(getPureEntry(e)),
    addHistoryToDB([newHist])
  ])
  const oldVer = getEntryHistoryVersion(e, historyItemId)
  showToast(`${t('versionRestored')} v${oldVer} → v${getEntryVersion(e)}`)
  historyModalVisible.value = false
  refreshData()
}

// 面包屑导航
const drillDownList = (entryId: string): void => {
  console.log("drillDownList", breadcrumbStack)
  const e = entryMap.value[entryId]
  if (e) breadcrumbStack.value.push({ id: e.id, content: e.content })
  refreshData()
}

const navBreadcrumb = (idx: number): void => {
  console.log("navBreadcrumb", breadcrumbStack)
  breadcrumbStack.value = idx < 0 ? [] : breadcrumbStack.value.slice(0, idx + 1)
  refreshData()
}

// 视图切换
const onViewModeChange = (): void => {
  breadcrumbStack.value = []
  expandedIds.value.clear()
  refreshData()
}
// 回收站切换
const toggleRecycleBin = (): void => {
  showRecycleBin.value = !showRecycleBin.value
  breadcrumbStack.value = []
  expandedIds.value.clear()
  searchQuery.value = ''
  refreshData()
}
// 搜索输入
const onSearch = (): void => {
  expandedIds.value.clear()
  if (searchQuery.value && viewMode.value === 'tree' && !showRecycleBin.value) {
    allEntries.value.filter(e => !e.isDeleted).forEach(e => {
      if (similarity(e.content, searchQuery.value) > SEARCH_SIMILARITY_THRESHOLD) {
        let cur = e.parentId ? entryMap.value[e.parentId] : null
        while (cur) { expandedIds.value.add(cur.id); cur = cur.parentId ? entryMap.value[cur.parentId] : null }
      }
    })
  }
  refreshData()
}

// ==================== 导入逻辑 ====================
const triggerImport = (): void => {
  if (importFileInput.value) { importFileInput.value.value = ''; importFileInput.value.click() }
}

const handleImportFile = (e: Event): void => {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return
  const ext = file.name.split('.').pop()?.toLowerCase()
  const reader = new FileReader()
  reader.onload = async (ev) => {
    try {
      const text = ev.target?.result as string
      let list: Entry[] = []
      if (ext === 'json') list = parseJSON(text)
      else if (ext === 'xml') list = parseXML(text)
      else if (ext === 'txt') list = parseTXT(text)
      else if (ext === 'yml' || ext === 'yaml') list = parseYML(text)
      else if (ext === 'properties') list = parseProperties(text)
      else if (ext === 'csv') list = parseCSV(text)
      else if (ext === 'xlsx' || ext === 'xls') { await handleExcelImport(file); return }
      else { showToast('不支持该文件格式'); return }
      await smartMergeImport(list)
      showToast(`${t('imported')} (${list.length} 条词条)`)
    } catch (err) {
      showToast('导入失败：' + (err as Error).message)
    }
  }
  if (ext === 'xlsx' || ext === 'xls') reader.readAsArrayBuffer(file)
  else reader.readAsText(file)
}

// Excel导入
const handleExcelImport = async (file: File): Promise<void> => {
  if (!XLSX) {
    showToast('未引入SheetJS(XLSX)库，无法导入Excel')
    return
  }
  const reader = new FileReader()
  reader.onload = async (ev) => {
    try {
      const data = new Uint8Array(ev.target?.result as ArrayBuffer)
      const wb = XLSX.read(data, { type: 'array' })
      const sheet1 = wb.Sheets[wb.SheetNames[0]]
      if (!sheet1) {
        showToast('Excel缺少工作表')
        return
      }
      const rows1 = XLSX.utils.sheet_to_json(sheet1, { header: 1 }) as any[][]
      if (rows1.length < 2) {
        showToast('表格无数据')
        return
      }
      const historyMap: Record<string, EntryHistoryItem[]> = {}
      const copyMap: Record<string, EntryCopyItem[]> = {}
      // 第二工作表：历史记录
      if (wb.SheetNames.length > 1) {
        const sheet2 = wb.Sheets[wb.SheetNames[1]]
        const rows2 = XLSX.utils.sheet_to_json(sheet2, { header: 1 }) as any[][]
        if (rows2.length > 1) {
          const headers2 = rows2[0].map(h => String(h).toLowerCase().trim())
          const eidIdx = headers2.indexOf('entryid')
          const contIdx = headers2.indexOf('content')
          const timeIdx = headers2.indexOf('timestamp')
          const uidIdx = headers2.indexOf('userid')
          const idIdx = headers2.indexOf('id')
          for (let i = 1; i < rows2.length; i++) {
            const row = rows2[i]
            if (!row) continue
            const eid = row[eidIdx]?.toString() || ''
            const cont = row[contIdx]?.toString() || ''
            const ts = new Date(row[timeIdx]).getTime() || Date.now()
            const uid = row[uidIdx]?.toString() || ''
            const recId = row[idIdx]?.toString() || uuid()
            if (!eid) continue
            if (!historyMap[eid]) historyMap[eid] = []
            historyMap[eid].push({ id: recId, entryId: eid, content: cont, timestamp: ts, userId: uid })
          }
        }
      }
      // 第三工作表：复制记录
      if (wb.SheetNames.length > 2) {
        const sheet3 = wb.Sheets[wb.SheetNames[2]]
        const rows3 = XLSX.utils.sheet_to_json(sheet3, { header: 1 }) as any[][]
        if (rows3.length > 1) {
          const headers3 = rows3[0].map(h => String(h).toLowerCase().trim())
          const eidIdx = headers3.indexOf('entryid')
          const contIdx = headers3.indexOf('content')
          const timeIdx = headers3.indexOf('timestamp')
          const uidIdx = headers3.indexOf('userid')
          const idIdx = headers3.indexOf('id')
          for (let i = 1; i < rows3.length; i++) {
            const row = rows3[i]
            if (!row) continue
            const eid = row[eidIdx]?.toString() || ''
            const cont = row[contIdx]?.toString() || ''
            const ts = new Date(row[timeIdx]).getTime() || Date.now()
            const uid = row[uidIdx]?.toString() || ''
            const recId = row[idIdx]?.toString() || uuid()
            if (!eid) continue
            if (!copyMap[eid]) copyMap[eid] = []
            copyMap[eid].push({ id: recId, entryId: eid, content: cont, timestamp: ts, userId: uid })
          }
        }
      }
      const headers1 = rows1[0].map(h => String(h).toLowerCase().trim())
      const idCol = headers1.indexOf('id')
      const pidCol = headers1.indexOf('parentid')
      const contentCol = headers1.indexOf('content')
      const createdAtCol = headers1.indexOf('createdat')
      const updatedAtCol = headers1.indexOf('updatedat')
      const isDeletedCol = headers1.indexOf('isdeleted')
      const deletedAtCol = headers1.indexOf('deletedat')
      const uidCol = headers1.indexOf('userid')
      if (contentCol < 0) {
        showToast('表格缺少content列')
        return
      }
      const oldIdMap: Record<string, string> = {}
      const newEntries: Entry[] = []
      const now = Date.now()
      for (let i = 1; i < rows1.length; i++) {
        const row = rows1[i]
        if (!row || !row[contentCol]) continue
        const oldId = (idCol >= 0 && row[idCol]) ? String(row[idCol]) : uuid()
        const newId = uuid()
        oldIdMap[oldId] = newId
        const entry: Entry = {
          id: newId,
          parentId: (pidCol >= 0 && row[pidCol]) ? String(row[pidCol]) : null,
          content: String(row[contentCol]).trim(),
          copyRecords: [],
          historyRecords: [],
          userId: (uidCol >= 0 && row[uidCol]) ? String(row[uidCol]) : currentUserId.value,
          createdAt: (createdAtCol >= 0) ? (new Date(row[createdAtCol]).getTime() || now) : now,
          updatedAt: (updatedAtCol >= 0) ? (new Date(row[updatedAtCol]).getTime() || now) : now,
          isDeleted: (isDeletedCol >= 0) ? (String(row[isDeletedCol]).toLowerCase() === 'true') : false,
          deletedAt: (deletedAtCol >= 0) ? (new Date(row[deletedAtCol]).getTime() || null) : null,
        }
        newEntries.push(entry)
      }
      for (const entry of newEntries) {
        if (entry.parentId && oldIdMap[entry.parentId]) {
          entry.parentId = oldIdMap[entry.parentId]
        }
        let oldIdForEntry: string | null = null
        for (const [old, nid] of Object.entries(oldIdMap)) {
          if (nid === entry.id) { oldIdForEntry = old; break }
        }
        if (oldIdForEntry && historyMap[oldIdForEntry]) {
          entry.historyRecords = historyMap[oldIdForEntry].sort((a, b) => a.timestamp - b.timestamp)
        }
        if (oldIdForEntry && copyMap[oldIdForEntry]) {
          entry.copyRecords = copyMap[oldIdForEntry]
        }
      }
      await smartMergeImport(newEntries)
      refreshData()
    } catch (err) {
      console.error(err)
      showToast('Excel导入错误：' + (err as Error).message)
    }
  }
  reader.readAsArrayBuffer(file)
}

/** 智能合并导入数据：ID存在对比updatedAt，新覆盖旧跳过；不存在新增 */
const smartMergeImport = async (list: Entry[]): Promise<void> => {
  const localMap = entryMap.value
  const toAdd: Entry[] = []
  const toUpdate: Entry[] = []

  for (const item of list) {
    const local = localMap[item.id]
    if (!local) {
      toAdd.push(item)
      continue
    }
    // 本地存在同ID，导入更新时间更新则覆盖
    if (item.updatedAt > local.updatedAt) {
      local.content = item.content
      local.parentId = item.parentId
      local.isDeleted = item.isDeleted
      local.deletedAt = item.deletedAt
      local.createdAt = item.createdAt
      local.updatedAt = item.updatedAt
      local.userId = item.userId
      toUpdate.push(local)
    }
  }

  // 新增写入响应式列表并入库
  for (const e of toAdd) allEntries.value.push(e)
  for (const e of toAdd) await saveEntryToDB(getPureEntry(e))
  // 更新现有词条
  for (const e of toUpdate) await saveEntryToDB(getPureEntry(e))

  refreshData()
}

// 各类文件解析器
const parseJSON = (text: string): Entry[] => {
  const data = JSON.parse(text)
  const flat: Entry[] = []
  const now = Date.now()
  const flatten = (nodes: any[], pid: string | null): void => {
    if (!Array.isArray(nodes)) return
    nodes.forEach(n => {
      const entryId = n.id || uuid()
      const entry: Entry = {
        id: entryId,
        parentId: pid || null,
        content: n.content || n.text || '',
        historyRecords: Array.isArray(n.historyRecords)
          ? n.historyRecords.map((h: any) => ({
            id: h.id || uuid(),
            entryId,
            content: h.content,
            timestamp: h.timestamp || now,
            userId: h.userId || ''
          }))
          : [],
        copyRecords: Array.isArray(n.copyRecords)
          ? n.copyRecords.map((c: any) => ({
            id: c.id || uuid(),
            entryId,
            content: c.content,
            timestamp: c.timestamp || now,
            userId: c.userId || ''
          }))
          : [],
        isDeleted: n.isDeleted || false,
        deletedAt: null,
        createdAt: n.createdAt || now,
        updatedAt: n.updatedAt || now,
        userId: n.userId || currentUserId.value
      }
      flat.push(entry)
      if (n.children) flatten(n.children, entry.id)
    })
  }
  if (Array.isArray(data)) flatten(data, null)
  else if (data.entries) flatten(data.entries, null)
  else if (data.children) flatten(data.children, null)
  else flatten([data], null)
  return flat
}
const parseXML = (text: string): Entry[] => {
  const p = new DOMParser()
  const doc = p.parseFromString(text, 'text/xml')
  const flat: Entry[] = []
  const now = Date.now()
  const parseNode = (node: Element, pid: string | null): void => {
    for (const child of node.children) {
      if (child.tagName === 'entry' || child.tagName === 'item') {
        const c = child.getAttribute('content') || child.textContent?.trim() || ''
        const entryId = child.getAttribute('id') || uuid()
        const entry: Entry = {
          id: entryId,
          parentId: pid || null,
          content: c,
          historyRecords: [],
          copyRecords: [],
          isDeleted: child.getAttribute('isDeleted') === 'true',
          deletedAt: null,
          createdAt: now,
          updatedAt: now,
          userId: currentUserId.value
        }
        flat.push(entry)
        parseNode(child, flat[flat.length - 1].id)
      }
    }
  }
  parseNode(doc.documentElement, null)
  return flat
}
const parseTXT = (text: string): Entry[] => {
  const lines = text.split('\n').filter(l => l.trim())
  const now = Date.now()
  return lines.map(l => {
    const eid = uuid()
    return {
      id: eid, parentId: null, content: l.trim(),
      historyRecords: [], copyRecords: [],
      isDeleted: false, deletedAt: null, createdAt: now, updatedAt: now, userId: currentUserId.value
    }
  })
}
const parseYML = (text: string): Entry[] => {
  const flat: Entry[] = []
  const now = Date.now()
  const lines = text.split('\n')
  const stack: { indent: number; id: string | null }[] = [{ indent: -1, id: null }]
  for (const line of lines) {
    if (!line.trim() || line.trim().startsWith('#')) continue
    const indent = line.search(/\S/)
    const content = line.trim().replace(/^-\s*/, '').trim()
    if (!content) continue
    while (stack.length > 0 && stack[stack.length - 1].indent >= indent) stack.pop()
    const pid = stack.length > 0 ? stack[stack.length - 1].id : null
    const eid = uuid()
    const entry: Entry = {
      id: eid, parentId: pid, content,
      historyRecords: [], copyRecords: [],
      isDeleted: false, deletedAt: null, createdAt: now, updatedAt: now, userId: currentUserId.value
    }
    flat.push(entry)
    stack.push({ indent, id: entry.id })
  }
  return flat
}
const parseProperties = (text: string): Entry[] => {
  const flat: Entry[] = []
  const now = Date.now()
  const lines = text.split('\n')
  const pathMap: Record<string, string> = {}
  for (let line of lines) {
    line = line.trim()
    if (!line || line.startsWith('#') || line.startsWith('!')) continue
    const eq = line.indexOf('=')
    if (eq < 0) continue
    const key = line.substring(0, eq).trim()
    const val = line.substring(eq + 1).trim()
    if (!key || !val) continue
    const parts = key.split('.')
    let pid: string | null = null
    for (let i = 0; i < parts.length - 1; i++) {
      const pk = parts.slice(0, i + 1).join('.')
      if (pathMap[pk]) pid = pathMap[pk]
    }
    const eid = uuid()
    const entry: Entry = {
      id: eid, parentId: pid, content: val,
      historyRecords: [], copyRecords: [],
      isDeleted: false, deletedAt: null, createdAt: now, updatedAt: now, userId: currentUserId.value
    }
    flat.push(entry)
    pathMap[key] = entry.id
  }
  return flat
}
const parseCSV = (text: string): Entry[] => {
  const lines = text.split('\n').filter(l => l.trim())
  if (lines.length < 2) return []
  const headers = lines[0].split(',').map(h => h.trim().toLowerCase())
  const idCol = headers.findIndex(h => h === 'id')
  const pidCol = headers.findIndex(h => h === 'parentid' || h === 'parent_id' || h === 'parent')
  const contentCol = headers.findIndex(h => h === 'content' || h === 'text' || h === 'entry')
  if (contentCol < 0) return []
  const entries: Entry[] = []
  const now = Date.now()
  for (let i = 1; i < lines.length; i++) {
    const cols = lines[i].split(',').map(c => c.trim())
    if (!cols[contentCol]) continue
    const eid = (idCol >= 0 && cols[idCol]) ? cols[idCol] : uuid()
    entries.push({
      id: eid,
      parentId: (pidCol >= 0 && cols[pidCol]) ? cols[pidCol] : null,
      content: cols[contentCol],
      historyRecords: [],
      copyRecords: [],
      isDeleted: false, deletedAt: null, createdAt: now, updatedAt: now, userId: currentUserId.value
    })
  }
  return entries
}

// ==================== 导出逻辑（完全不变） ====================
const doExport = (format: 'json' | 'xml' | 'txt' | 'yml' | 'properties' | 'excel'): void => {
  showExportMenu.value = false
  const all = allEntries.value
  const nowStr = new Date().toISOString().slice(0, 10)
  try {
    let blob: Blob, fn: string
    switch (format) {
      case 'json':
        blob = new Blob([JSON.stringify(buildTreeForExport(all), null, 2)], { type: 'application/json' })
        fn = `entries_${nowStr}.json`
        break
      case 'xml':
        blob = new Blob([buildXML(all)], { type: 'application/xml' })
        fn = `entries_${nowStr}.xml`
        break
      case 'txt':
        blob = new Blob([all.filter(e => !e.parentId).map(e => e.content).join('\n')], { type: 'text/plain' })
        fn = `entries_${nowStr}.txt`
        break
      case 'yml':
        blob = new Blob([buildYML(all)], { type: 'text/yaml' })
        fn = `entries_${nowStr}.yml`
        break
      case 'properties':
        blob = new Blob([buildProperties(all)], { type: 'text/plain' })
        fn = `entries_${nowStr}.properties`
        break
      case 'excel':
        if (!XLSX) {
          showToast('缺少XLSX库，无法导出Excel')
          return
        }
        const buf = buildExcel(all)
        blob = new Blob([buf], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
        fn = `entries_${nowStr}.xlsx`
        break
      default:
        return
    }
    const url = URL.createObjectURL(blob!)
    const a = document.createElement('a')
    a.href = url
    a.download = fn
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    showToast(`${t('exported')}: ${fn}`)
  } catch (err) {
    showToast('导出失败：' + (err as Error).message)
  }
}
type ExportTreeItem = Omit<Entry, 'children'> & { children?: ExportTreeItem[] }
const buildTreeForExport = (entries: Entry[]): { entries: ExportTreeItem[] } => {
  const map: Record<string, ExportTreeItem> = {}
  entries.forEach(e => map[e.id] = { ...e, children: [] })
  const roots: ExportTreeItem[] = []
  entries.forEach(e => {
    if (e.parentId && map[e.parentId]) map[e.parentId].children!.push(map[e.id])
    else roots.push(map[e.id])
  })
  const clean = (n: ExportTreeItem): ExportTreeItem => {
    const { id, parentId, content, historyRecords, copyRecords, userId, createdAt, updatedAt, deletedAt, isDeleted, children } = n
    if (!children || children.length === 0) return { id, parentId, content, historyRecords, copyRecords, userId, createdAt, updatedAt, deletedAt, isDeleted }
    return { id, parentId, content, historyRecords, copyRecords, userId, createdAt, updatedAt, deletedAt, isDeleted, children: children.map(clean) }
  }
  return { entries: roots.map(clean) }
}
const buildXML = (entries: Entry[]): string => {
  const map: Record<string, Entry> = {}
  entries.forEach(e => map[e.id] = e)
  const roots = entries.filter(e => !e.parentId || !map[e.parentId])
  let xml = '<?xml version="1.0" encoding="UTF-8"?>\n<entries>\n'
  const render = (e: Entry, ind: number): void => {
    const s = '  '.repeat(ind)
    const esc = escapeXml(e.content)
    xml += `${s}<entry id="${e.id}" parentId="${e.parentId || ''}" content="${esc}" userId="${e.userId}" isDeleted="${e.isDeleted}">\n`
    const children = entries.filter(c => c.parentId === e.id)
    children.forEach(c => render(c, ind + 1))
    xml += `${s}</entry>\n`
  }
  roots.forEach(r => render(r, 1))
  xml += '</entries>'
  return xml
}
const buildYML = (entries: Entry[]): string => {
  const map: Record<string, Entry> = {}
  entries.forEach(e => { map[e.id] = e; });
  const roots = entries.filter(e => !e.parentId || !map[e.parentId]);
  let y = '';
  const render = (e: Entry, ind: number): void => {
    const p = '  '.repeat(ind) + '- ';
    y += p + e.content.replace(/\n/g, '\\n') + '\n';
    const children = entries.filter(c => c.parentId === e.id);
    children.forEach(c => render(c, ind + 1));
  };
  roots.forEach(r => render(r, 0));
  return y;
};
const buildProperties = (entries: Entry[]): string => {
  const map: Record<string, Entry> = {};
  entries.forEach(e => { map[e.id] = e; });
  let p = '';
  const path = (e: Entry): string => {
    const parts: string[] = [];
    let cur: Entry | null = e;
    while (cur) {
      parts.unshift(cur.content.replace(/[.=]/g, '_').replace(/\s+/g, '_'));
      cur = cur.parentId ? map[cur.parentId] : null;
    }
    return parts.join('.');
  };
  entries.forEach(e => {
    p += path(e) + '=' + e.content.replace(/\n/g, '\\n') + '\n';
  });
  return p;
};
const buildExcel = (entries: Entry[]): Uint8Array => {
  // 主词条表
  const mainRows: (string | number | null)[][] = [['id', 'parentId', 'content', 'userId', 'createdAt', 'updatedAt', 'isDeleted', 'deletedAt']];
  entries.forEach(e => {
    mainRows.push([
      e.id,
      e.parentId || '',
      e.content,
      e.userId,
      new Date(e.createdAt).toISOString(),
      new Date(e.updatedAt).toISOString(),
      e.isDeleted ? 'true' : 'false',
      e.deletedAt ? new Date(e.deletedAt).toISOString() : null
    ]);
  });
  // 历史记录表
  const historyRows: (string | number)[][] = [['id', 'entryId', 'content', 'timestamp', 'userId']];
  entries.forEach(e => {
    e.historyRecords.forEach(h => {
      historyRows.push([h.id, e.id, h.content, new Date(h.timestamp).toISOString(), h.userId])
    })
  })
  // 复制记录表
  const copyRows: (string | number)[][] = [['id', 'entryId', 'content', 'timestamp', 'userId']];
  entries.forEach(e => {
    e.copyRecords.forEach(c => {
      copyRows.push([c.id, e.id, c.content, new Date(c.timestamp).toISOString(), c.userId])
    })
  })

  const wsMain = XLSX.utils.aoa_to_sheet(mainRows);
  const wsHistory = XLSX.utils.aoa_to_sheet(historyRows);
  const wsCopy = XLSX.utils.aoa_to_sheet(copyRows);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, wsMain, t('entries'));
  XLSX.utils.book_append_sheet(wb, wsHistory, 'history');
  XLSX.utils.book_append_sheet(wb, wsCopy, 'copyRecords');
  return new Uint8Array(XLSX.write(wb, { bookType: 'xlsx', type: 'array' }));
};

// 监听配置
watch(viewMode, () => saveSettings());
watch(currentTheme, () => setTheme());
watch(currentLang, () => setLang());
watch(showRecycleBin, () => refreshData());

onMounted(async () => {
  loadSettings();
  await loadData();
  refreshData();
});
</script>

<style>
/* ===== 全局变量 & 基础重置 ===== */
:root {
  --bg: #f5f5f7;
  --bg2: #ffffff;
  --bg3: #ebebef;
  --text: #1a1a1a;
  --text2: #5e5e64;
  --border: #d9d9df;
  --accent: #4f7cff;
  --accent-hover: #3b62e0;
  --danger: #e6504c;
  --danger-hover: #c43e3a;
  --success: #2da44e;
  --warning: #d4992a;
  --tag-bg: #eef2ff;
  --tag-text: #4f7cff;
  --shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  --shadow-lg: 0 12px 28px rgba(0, 0, 0, 0.12);
  --radius: 10px;
  --radius-sm: 6px;
  --transition: 0.2s cubic-bezier(0.2, 0, 0, 1);
  --font: 'Inter', 'PingFang SC', 'Microsoft YaHei', 'Segoe UI', system-ui, sans-serif;
}

[data-theme="dark"] {
  --bg: #1a1b1e;
  --bg2: #25262b;
  --bg3: #2d2e33;
  --text: #e0e0e0;
  --text2: #9a9ba0;
  --border: #3a3b40;
  --accent: #6c8cff;
  --accent-hover: #8ba3ff;
  --danger: #f06060;
  --danger-hover: #d94a4a;
  --success: #3fb950;
  --warning: #e2a13b;
  --tag-bg: #2a3150;
  --tag-text: #8ca3ff;
  --shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 12px 28px rgba(0, 0, 0, 0.5);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: var(--font);
  background: var(--bg);
  color: var(--text);
  transition: background var(--transition), color var(--transition);
  min-height: 100vh;
  line-height: 1.5;
}

#app {
  max-width: 1120px;
  margin: 0 auto;
  padding: 0 16px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* ===== 头部 & 导航 ===== */
.header {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  background: var(--bg);
  z-index: 100;
  min-height: 56px;
  transition: background var(--transition);
}

.header .title {
  font-size: 1.3rem;
  font-weight: 700;
  white-space: nowrap;
  margin-right: auto;
  display: flex;
  align-items: center;
  gap: 6px;
}

.header .title span { color: var(--accent); }

/* ===== 通用按钮 (主页面 & 子组件共用) ===== */
.btn {
  padding: 7px 14px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 0.85rem;
  font-family: var(--font);
  background: var(--bg2);
  color: var(--text);
  transition: all var(--transition);
  white-space: nowrap;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  user-select: none;
  font-weight: 500;
}

.btn:hover { background: var(--bg3); border-color: var(--accent); }

.btn.accent { background: var(--accent); color: #fff; border-color: var(--accent); font-weight: 600; }
.btn.accent:hover { background: var(--accent-hover); }

.btn.danger { background: var(--danger); color: #fff; border-color: var(--danger); }
.btn.danger:hover { background: var(--danger-hover); }

.btn.btn-small { padding: 4px 9px; font-size: 0.75rem; border-radius: 4px; }
.btn.icon-only { padding: 4px 8px; min-width: 30px; justify-content: center; }
.btn:disabled { opacity: 0.45; cursor: not-allowed; pointer-events: none; }

select.btn {
  appearance: none;
  padding-right: 26px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6'%3E%3Cpath d='M0 0l5 6 5-6z' fill='%23666'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
}

/* ===== 工具栏 ===== */
.toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  padding: 10px 0;
  align-items: center;
}

.toolbar .sep {
  width: 1px;
  height: 20px;
  background: var(--border);
  margin: 0 5px;
}

.search-input {
  padding: 7px 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  font-family: var(--font);
  background: var(--bg2);
  color: var(--text);
  outline: none;
  width: 190px;
  transition: all var(--transition);
}

.search-input:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(79,124,255,0.12); width: 240px; }

/* ===== 主内容区 & 列表容器 ===== */
.main-content { flex: 1; display: flex; flex-direction: column; gap: 10px; padding-bottom: 24px; }

.entry-list {
  flex: 1;
  background: var(--bg2);
  border-radius: var(--radius);
  border: 1px solid var(--border);
  overflow: auto;
  box-shadow: var(--shadow);
  transition: all var(--transition);
  max-height: calc(100vh - 210px);
  min-height: 320px;
}

.entry-list.recycle { border-left: 4px solid var(--warning); }

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 70px 20px;
  color: var(--text2);
  text-align: center;
  gap: 10px;
  font-size: 0.95rem;
}

.empty-state .icon { font-size: 3rem; opacity: 0.5; }

/* ===== 面包屑导航 ===== */
.breadcrumb {
  display: flex; align-items: center; gap: 5px; flex-wrap: wrap;
  font-size: 0.85rem; padding: 6px 0; color: var(--text2); min-height: 36px;
  background: var(--bg2); border-radius: var(--radius-sm); padding: 8px 12px;
  border: 1px solid var(--border); margin-bottom: 8px;
}

.breadcrumb span { cursor: pointer; color: var(--accent); transition: color var(--transition); }
.breadcrumb span:hover { color: var(--accent-hover); text-decoration: underline; }
.breadcrumb .sep-bc { color: var(--text2); cursor: default; }
.breadcrumb .current-bc { color: var(--text); font-weight: 600; cursor: default; }

/* ===== 模态框 ===== */
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.45); z-index: 200;
  display: flex; align-items: center; justify-content: center;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

.modal {
  background: var(--bg2); border-radius: var(--radius); border: 1px solid var(--border);
  box-shadow: var(--shadow-lg); padding: 24px; max-width: 660px; width: 95%;
  max-height: 85vh; display: flex; flex-direction: column; gap: 16px;
  animation: slideUp 0.25s ease;
}

@keyframes slideUp { from { transform: translateY(30px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

.modal h3 { font-size: 1.15rem; font-weight: 600; margin: 0; }

.modal textarea {
  width: 100%; min-height: 120px; padding: 12px; border: 1px solid var(--border);
  border-radius: var(--radius-sm); font-family: var(--font); font-size: 0.9rem;
  background: var(--bg); color: var(--text); resize: vertical; outline: none; line-height: 1.6;
}

.modal textarea:focus { border-color: var(--accent); box-shadow: 0 0 0 3px rgba(79,124,255,0.15); }
.modal .hint { font-size: 0.8rem; color: var(--text2); margin-top: -8px; }
.modal .modal-actions { display: flex; gap: 10px; justify-content: flex-end; flex-wrap: wrap; }

/* ===== 历史记录列表 ===== */
.history-list { max-height: 280px; overflow-y: auto; border: 1px solid var(--border); border-radius: var(--radius-sm); }

.history-item { display: flex; align-items: center; gap: 10px; padding: 10px 14px; border-bottom: 1px solid var(--border); font-size: 0.85rem; transition: background var(--transition); }
.history-item:hover { background: var(--bg3); }
.history-item .h-content { flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.history-item .h-version { font-weight: 700; }

/* ===== 全局 Toast ===== */
.toast {
  position: fixed; bottom: 28px; right: 28px; background: var(--bg2); border: 1px solid var(--border);
  border-radius: var(--radius); padding: 12px 20px; box-shadow: var(--shadow-lg); z-index: 300;
  font-size: 0.9rem; font-weight: 500; animation: slideIn 0.3s ease; max-width: 380px;
}

@keyframes slideIn { from { transform: translateX(80px); opacity: 0; } to { transform: translateX(0); opacity: 1; } }

/* ===== 响应式 ===== */
@media (max-width: 640px) {
  .header .title { font-size: 1rem; }
  .search-input { width: 130px; }
  /* 注意：原样式中 .entry-row .actions 在移动端强制可见，此处保留 */
  .entry-row .actions { opacity: 1; }
}
</style>
