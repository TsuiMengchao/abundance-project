<template>
  <q-page class="row q-pa-md">
    <div id="app">
      <div class="header">
        <div class="title">📖 <span>{{ t('appTitle') }}</span></div>
        <button class="btn" @click="toggleRecycleBin" :class="{accent: showRecycleBin}">
          🗑️ {{ showRecycleBin ? t('backToHome') : t('recycleBin') }} ({{ deletedCount }})
        </button>
        <button class="btn accent" @click="openAddModal(null)" v-if="!showRecycleBin">＋ {{ t('addRoot') }}</button>
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
                                @update="refreshData">

            </entry-row-renderer>
          </template>
        </div>
        <div class="empty-state" v-else>
          <span class="icon">{{ showRecycleBin ? '🗑️' : '📭' }}</span>
          <span>{{ showRecycleBin ? t('emptyRecycle') : t('emptyHint') }}</span>
          <button class="btn accent" v-if="!showRecycleBin" @click="openAddModal(null)">＋ {{ t('addFirst') }}</button>
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
            <div class="history-item" v-for="h in historyEntry?.history||[]" :key="h.version"
                 :style="{background: h.version===historyEntry?.version ? 'var(--tag-bg)' : 'transparent'}">
              <span class="h-version">v{{ h.version }}</span>
              <span class="h-content">{{ h.content }}</span>
              <span style="font-size:0.7rem;color:var(--text2);">{{ formatTime(h.timestamp) }}</span>
              <span v-if="h.version===historyEntry?.version" class="tag current">● {{ t('current') }}</span>
              <button v-else class="btn btn-small" @click="restoreVersion(historyEntry.id, h.version)">{{ t('restore') }}</button>
            </div>
          </div>
          <div class="modal-actions"><button class="btn" @click="historyModalVisible=false">{{ t('close') }}</button></div>
        </div>
      </div>

      <div class="toast" v-if="toastMsg" @click="toastMsg=''">{{ toastMsg }}</div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'

import { useI18n } from 'vue-i18n'
import * as XLSX from 'xlsx'
import EntryRowRenderer from '@/components/EntryRowRenderer.vue'

// ==================== 常量 & 工具函数 抽离封装 ====================
const STORAGE_KEY = 'entry-reader-data'
const SETTINGS_KEY = 'entry-reader-settings'
const SEARCH_SIMILARITY_THRESHOLD = 0.25

// UUID生成
const uuid = () => 'e_' + Date.now().toString(36) + '_' + Math.random().toString(36).substring(2, 8)

// 编辑距离算法
const levenshteinDistance = (a, b) => {
  const m = a.length, n = b.length
  const dp = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0))
  for (let i = 0; i <= m; i++) dp[i][0] = i
  for (let j = 0; j <= n; j++) dp[0][j] = j
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      dp[i][j] = Math.min(
        dp[i - 1][j] + 1,
        dp[i][j - 1] + 1,
        dp[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1)
      )
    }
  }
  return dp[m][n]
}

// 文本相似度
const similarity = (a, b) => {
  const al = a.toLowerCase(), bl = b.toLowerCase()
  if (al.includes(bl) || bl.includes(al)) {
    return 0.7 + Math.min(al.length, bl.length) / Math.max(al.length, bl.length) * 0.3
  }
  const len = Math.max(al.length, bl.length)
  if (len === 0) return 1
  const d = levenshteinDistance(al, bl)
  return Math.max(0, 1 - d / len)
}

// XML特殊字符转义
const escapeXml = (str) => str
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;')

// ==================== i18n 语言包 ====================
const { t, locale } = useI18n()

// ==================== 响应式状态 ====================
const allEntries = ref([])
const showRecycleBin = ref(false)
const viewMode = ref('tree')
const currentTheme = ref('light')
const currentLang = ref('zh-CN')
const searchQuery = ref('')
const showExportMenu = ref(false)
const historyModalVisible = ref(false)
const historyEntry = ref(null)
const breadcrumbStack = ref([])
const toastMsg = ref('')
const toastTimer = ref(null)
const expandedIds = ref(new Set())
const importFileInput = ref(null)

const editModal = ref({
  visible: false,
  mode: 'add',
  parentId: null,
  entryId: null,
  content: ''
})

// ==================== 计算属性 ====================
const entryMap = computed(() => {
  const map = {}
  allEntries.value.forEach(e => map[e.id] = e)
  return map
})

const childrenMap = computed(() => {
  const map = {}
  allEntries.value.forEach(e => {
    const pid = e.parentId || '__root__'
    if (!map[pid]) map[pid] = []
    map[pid].push(e)
  })
  // 统一排序
  Object.keys(map).forEach(key => {
    map[key].sort((a, b) => sortScore(b) - sortScore(a))
  })
  return map
})

const rootEntries = computed(() => (childrenMap.value['__root__'] || []).filter(e => !e.isDeleted))
const deletedRootEntries = computed(() => allEntries.value.filter(e => e.isDeleted).filter(e => {
  if (!e.parentId) return true
  const p = entryMap.value[e.parentId]
  return !p || !p.isDeleted
}))

// 展示列表主逻辑
const displayEntries = computed(() => {
  const entries = allEntries.value
  const cm = childrenMap.value
  const em = entryMap.value

  // 平铺模式
  if (viewMode.value === 'flat') {
    let list = showRecycleBin.value
      ? entries.filter(e => e.isDeleted)
      : entries.filter(e => !e.isDeleted)
    if (searchQuery.value) {
      list = list.filter(e => similarity(e.content, searchQuery.value) > SEARCH_SIMILARITY_THRESHOLD)
    }
    list.sort((a, b) => sortScore(b) - sortScore(a))
    return list
  }

  // 树形模式
  if (viewMode.value === 'tree') {
    let roots = showRecycleBin.value ? deletedRootEntries.value : rootEntries.value
    if (searchQuery.value) {
      const active = entries.filter(e => !e.isDeleted)
      return active.filter(e => similarity(e.content, searchQuery.value) > SEARCH_SIMILARITY_THRESHOLD)
        .sort((a, b) => sortScore(b) - sortScore(a))
    }
    return roots
  }

  // 面包屑层级模式
  if (viewMode.value === 'breadcrumb') {
    let parentId = null
    if (breadcrumbStack.value.length > 0) {
      parentId = breadcrumbStack.value[breadcrumbStack.value.length - 1].id
    }
    let list
    if (showRecycleBin.value) {
      list = parentId ? entries.filter(e => e.parentId === parentId) : deletedRootEntries.value
    } else {
      list = parentId ? getChildren(parentId) : rootEntries.value
    }
    if (searchQuery.value) {
      list = list.filter(e => similarity(e.content, searchQuery.value) > SEARCH_SIMILARITY_THRESHOLD)
    }
    return list.sort((a, b) => sortScore(b) - sortScore(a))
  }
  return []
})

const activeCount = computed(() => allEntries.value.filter(e => !e.isDeleted).length)
const deletedCount = computed(() => allEntries.value.filter(e => e.isDeleted).length)
const filteredCount = computed(() => displayEntries.value.length)

// ==================== 公共方法 ====================
// 词条排序权重
const sortScore = (e) => {
  const now = Date.now()
  const age = (now - (e.updatedAt || e.createdAt || now)) / 3600000
  return (1 / (1 + age * 0.1)) * 10 + (e.copyCount || 0) * 0.5 + (e.modifyCount || 0) * 0.3
}

// 获取未删除子节点
const getChildren = (pid) => (childrenMap.value[pid || '__root__'] || []).filter(e => !e.isDeleted)
// 获取全部子节点（含删除）
const getAllChildren = (pid) => childrenMap.value[pid || '__root__'] || []
// 判断是否顶级删除条目
const isTopDeleted = (entry) => {
  if (!entry.isDeleted) return false
  if (!entry.parentId) return true
  const p = entryMap.value[entry.parentId]
  return !p || !p.isDeleted
}
// 是否存在子节点
const hasAnyChildren = (id) => (childrenMap.value[id] || []).length > 0

// 时间格式化
const formatTime = (ts) => {
  if (!ts) return ''
  return new Date(ts).toLocaleString(currentLang.value === 'en' ? 'en-US' : 'zh-CN', {
    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
  })
}

// Toast提示
const showToast = (msg) => {
  toastMsg.value = msg
  if (toastTimer.value) clearTimeout(toastTimer.value)
  toastTimer.value = setTimeout(() => toastMsg.value = '', 2500)
}

// 刷新响应式列表
const refreshData = () => {
  allEntries.value = [...allEntries.value]
}

// 本地存储读写
const saveData = () => {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(allEntries.value))
  } catch (err) {
    showToast('数据保存失败：' + err.message)
  }
}
const loadData = () => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) allEntries.value = JSON.parse(raw)
  } catch (err) {
    allEntries.value = []
    showToast('数据加载异常，已重置')
  }
  if (!Array.isArray(allEntries.value)) allEntries.value = []
}
const saveSettings = () => {
  try {
    localStorage.setItem(SETTINGS_KEY, JSON.stringify({
      theme: currentTheme.value,
      lang: currentLang.value,
      viewMode: viewMode.value
    }))
  } catch (e) {}
}
const loadSettings = () => {
  try {
    const raw = localStorage.getItem(SETTINGS_KEY)
    if (raw) {
      const s = JSON.parse(raw)
      if (s.theme) currentTheme.value = s.theme
      if (s.lang) {
        currentLang.value = s.lang
        locale.value = currentLang.value
      }
      if (s.viewMode) viewMode.value = s.viewMode
    }
  } catch (e) {}
  setTheme()
}

// 主题切换
const setTheme = () => {
  document.documentElement.setAttribute('data-theme', currentTheme.value)
  saveSettings()
}
// 语言切换
const setLang = () => {
  locale.value = currentLang.value
  saveSettings()
}

// 复制文本
const copyEntryText = (entryId) => {
  const entry = entryMap.value[entryId]
  if (!entry) return
  navigator.clipboard.writeText(entry.content)
    .then(() => {
      entry.copyCount = (entry.copyCount || 0) + 1
      saveData()
      showToast('📋 ' + t('copied'))
    })
    .catch(() => {
      const ta = document.createElement('textarea')
      ta.value = entry.content
      document.body.appendChild(ta)
      ta.select()
      document.execCommand('copy')
      document.body.removeChild(ta)
      entry.copyCount = (entry.copyCount || 0) + 1
      saveData()
      showToast('📋 ' + t('copied'))
    })
}

// 弹窗操作
const openAddModal = (parentId) => {
  editModal.value = {
    visible: true,
    mode: 'add',
    parentId: parentId || null,
    entryId: null,
    content: ''
  }
}
const openEditModal = (entryId) => {
  const e = entryMap.value[entryId]
  if (!e) return
  editModal.value = {
    visible: true,
    mode: 'edit',
    parentId: null,
    entryId,
    content: e.content
  }
}
const cancelEditModal = () => {
  editModal.value.visible = false
}

// 提交新增/编辑
const submitEditModal = () => {
  const { mode, parentId, entryId, content } = editModal.value
  const trimContent = content.trim()
  if (!trimContent) {
    showToast('内容不能为空')
    return
  }
  const now = Date.now()
  if (mode === 'add') {
    const lines = content.split('\n\n').filter(l => l.trim())
    if (lines.length === 0) return
    const newEntries = lines.map(line => ({
      id: uuid(),
      parentId: parentId || null,
      content: line.trim(),
      version: 1,
      history: [{ version: 1, content: line.trim(), timestamp: now }],
      isDeleted: false,
      deletedAt: null,
      createdAt: now,
      updatedAt: now,
      copyCount: 0,
      modifyCount: 0
    }))
    allEntries.value.push(...newEntries)
    saveData()
    showToast(`${t('saved')} (${newEntries.length})`)
  } else {
    const entry = entryMap.value[entryId]
    if (!entry) return
    if (trimContent === entry.content) {
      showToast(t('contentUnchanged'))
      editModal.value.visible = false
      return
    }
    entry.content = trimContent
    entry.version = (entry.version || 0) + 1
    entry.modifyCount = (entry.modifyCount || 0) + 1
    entry.updatedAt = now
    if (!entry.history) entry.history = []
    entry.history.push({ version: entry.version, content: trimContent, timestamp: now })
    saveData()
    showToast(`${t('saved')} v${entry.version}`)
  }
  editModal.value.visible = false
  refreshData()
}

// 删除/恢复词条
const deleteEntry = (id) => {
  const e = entryMap.value[id]
  if (!e) return
  if (!confirm(`${t('confirmDelete')}\n\n${e.content.substring(0, 60)}`)) return
  e.isDeleted = true
  e.deletedAt = Date.now()
  e.updatedAt = Date.now()
  saveData()
  showToast('🗑️ ' + t('deleted'))
  refreshData()
}
const restoreEntry = (id) => {
  const e = entryMap.value[id]
  if (!e || !e.isDeleted) return
  e.isDeleted = false
  e.deletedAt = null
  e.updatedAt = Date.now()
  saveData()
  showToast('♻️ ' + t('restored'))
  refreshData()
}

// 历史版本
const showHistory = (id) => {
  historyEntry.value = entryMap.value[id]
  historyModalVisible.value = true
}
const restoreVersion = (entryId, version) => {
  const e = entryMap.value[entryId]
  if (!e) return
  const hist = e.history?.find(h => h.version === version)
  if (!hist) return
  const now = Date.now()
  e.content = hist.content
  e.version = (e.version || 0) + 1
  e.modifyCount = (e.modifyCount || 0) + 1
  e.updatedAt = now
  e.history.push({ version: e.version, content: hist.content, timestamp: now })
  saveData()
  showToast(`${t('versionRestored')} → v${e.version}`)
  historyModalVisible.value = false
  refreshData()
}

// 面包屑导航
const drillDownList = (entryId) => {
  const entry = entryMap.value[entryId]
  if (!entry) return
  breadcrumbStack.value.push({ id: entry.id, content: entry.content })
  refreshData()
}
const navBreadcrumb = (idx) => {
  if (idx < 0) {
    breadcrumbStack.value = []
    refreshData()
    return
  }
  breadcrumbStack.value = breadcrumbStack.value.slice(0, idx + 1)
  refreshData()
}

// 视图切换
const onViewModeChange = () => {
  breadcrumbStack.value = []
  expandedIds.value.clear()
  refreshData()
}
// 回收站切换
const toggleRecycleBin = () => {
  showRecycleBin.value = !showRecycleBin.value
  breadcrumbStack.value = []
  expandedIds.value.clear()
  searchQuery.value = ''
  refreshData()
}
// 搜索输入
const onSearch = () => {
  expandedIds.value.clear()
  if (searchQuery.value && viewMode.value === 'tree' && !showRecycleBin.value) {
    const active = allEntries.value.filter(e => !e.isDeleted)
    active.forEach(e => {
      if (similarity(e.content, searchQuery.value) > SEARCH_SIMILARITY_THRESHOLD) {
        let cur = e.parentId ? entryMap.value[e.parentId] : null
        while (cur) {
          expandedIds.value.add(cur.id)
          cur = cur.parentId ? entryMap.value[cur.parentId] : null
        }
      }
    })
  }
  refreshData()
}
// ==================== 导入逻辑 ====================
const triggerImport = () => {
  importFileInput.value = ''
  importFileInput.value.click()
}
const handleImportFile = (e) => {
  const file = e.target.files[0]
  if (!file) return
  const ext = file.name.split('.').pop().toLowerCase()
  const reader = new FileReader()
  reader.onload = (ev) => {
    const text = ev.target.result
    try {
      let entries = []
      if (ext === 'json') entries = parseJSON(text)
      else if (ext === 'xml') entries = parseXML(text)
      else if (ext === 'txt') entries = parseTXT(text)
      else if (ext === 'yml' || ext === 'yaml') entries = parseYML(text)
      else if (ext === 'properties') entries = parseProperties(text)
      else if (ext === 'xlsx' || ext === 'xls') {
        handleExcelImport(file)
        return
      } else if (ext === 'csv') entries = parseCSV(text)
      else {
        showToast('不支持该文件格式')
        return
      }
      if (entries.length === 0) {
        showToast('未解析到词条')
        return
      }
      mergeImportedEntries(entries)
    } catch (err) {
      showToast('导入失败：' + err.message)
    }
  }
  reader.readAsText(file)
}

// Excel导入（增加XLSX存在判断）
const handleExcelImport = async (file) => {
  if (!XLSX) {
    showToast('未引入SheetJS(XLSX)库，无法导入Excel')
    return
  }
  const reader = new FileReader()
  reader.onload = (ev) => {
    try {
      const data = new Uint8Array(ev.target.result)
      const wb = XLSX.read(data, { type: 'array' })
      const sheet1 = wb.Sheets[wb.SheetNames[0]]
      if (!sheet1) {
        showToast('Excel缺少工作表')
        return
      }
      const rows1 = XLSX.utils.sheet_to_json(sheet1, { header: 1 })
      if (rows1.length < 2) {
        showToast('表格无数据')
        return
      }
      let historyMap = {}
      if (wb.SheetNames.length > 1) {
        const sheet2 = wb.Sheets[wb.SheetNames[1]]
        const rows2 = XLSX.utils.sheet_to_json(sheet2, { header: 1 })
        if (rows2.length > 1) {
          const headers2 = rows2[0].map(h => String(h).toLowerCase().trim())
          const eidIdx = headers2.indexOf('entryid')
          const verIdx = headers2.indexOf('version')
          const contIdx = headers2.indexOf('content')
          const timeIdx = headers2.indexOf('timestamp')
          for (let i = 1; i < rows2.length; i++) {
            const row = rows2[i]
            if (!row) continue
            const eid = row[eidIdx]?.toString() || ''
            const ver = parseInt(row[verIdx]) || 1
            const cont = row[contIdx]?.toString() || ''
            const ts = new Date(row[timeIdx]).getTime() || Date.now()
            if (!eid) continue
            if (!historyMap[eid]) historyMap[eid] = []
            historyMap[eid].push({ version: ver, content: cont, timestamp: ts })
          }
        }
      }
      const headers1 = rows1[0].map(h => String(h).toLowerCase().trim())
      const idCol = headers1.indexOf('id')
      const pidCol = headers1.indexOf('parentid')
      const contentCol = headers1.indexOf('content')
      const versionCol = headers1.indexOf('version')
      const copyCountCol = headers1.indexOf('copycount')
      const modifyCountCol = headers1.indexOf('modifycount')
      const createdAtCol = headers1.indexOf('createdat')
      const updatedAtCol = headers1.indexOf('updatedat')
      const isDeletedCol = headers1.indexOf('isdeleted')
      const deletedAtCol = headers1.indexOf('deletedat')
      if (contentCol < 0) {
        showToast('表格缺少content列')
        return
      }
      const oldIdMap = {}
      const newEntries = []
      const now = Date.now()
      for (let i = 1; i < rows1.length; i++) {
        const row = rows1[i]
        if (!row || !row[contentCol]) continue
        const oldId = (idCol >= 0 && row[idCol]) ? String(row[idCol]) : uuid()
        const newId = uuid()
        oldIdMap[oldId] = newId
        const entry = {
          id: newId,
          parentId: (pidCol >= 0 && row[pidCol]) ? String(row[pidCol]) : null,
          content: String(row[contentCol]).trim(),
          version: (versionCol >= 0 && row[versionCol]) ? parseInt(row[versionCol]) || 1 : 1,
          copyCount: (copyCountCol >= 0) ? (parseInt(row[copyCountCol]) || 0) : 0,
          modifyCount: (modifyCountCol >= 0) ? (parseInt(row[modifyCountCol]) || 0) : 0,
          createdAt: (createdAtCol >= 0) ? (new Date(row[createdAtCol]).getTime() || now) : now,
          updatedAt: (updatedAtCol >= 0) ? (new Date(row[updatedAtCol]).getTime() || now) : now,
          isDeleted: (isDeletedCol >= 0) ? (String(row[isDeletedCol]).toLowerCase() === 'true') : false,
          deletedAt: (deletedAtCol >= 0) ? (new Date(row[deletedAtCol]).getTime() || null) : null,
          history: []
        }
        newEntries.push(entry)
      }
      for (const entry of newEntries) {
        if (entry.parentId && oldIdMap[entry.parentId]) {
          entry.parentId = oldIdMap[entry.parentId]
        }
        let oldIdForEntry = null
        for (const [old, nid] of Object.entries(oldIdMap)) {
          if (nid === entry.id) { oldIdForEntry = old; break }
        }
        if (oldIdForEntry && historyMap[oldIdForEntry]) {
          entry.history = historyMap[oldIdForEntry].sort((a, b) => a.version - b.version)
          if (entry.history.length > 0) {
            const maxVer = Math.max(...entry.history.map(h => h.version))
            entry.version = maxVer
          }
        } else {
          entry.history = [{ version: entry.version || 1, content: entry.content, timestamp: entry.createdAt }]
        }
      }
      allEntries.value.push(...newEntries)
      saveData()
      showToast(`${t('imported')} (${newEntries.length} 条词条)`)
      refreshData()
    } catch (err) {
      console.error(err)
      showToast('Excel导入错误：' + err.message)
    }
  }
  reader.readAsArrayBuffer(file)
}

// 导入合并ID映射
const mergeImportedEntries = (newEntries) => {
  const idMap = {}
  newEntries.forEach(e => {
    const old = e.id
    const nid = uuid()
    idMap[old] = nid
    e.id = nid
  })
  newEntries.forEach(e => {
    if (e.parentId && idMap[e.parentId]) e.parentId = idMap[e.parentId]
  })
  allEntries.value.push(...newEntries)
  saveData()
  showToast(`${t('imported')} (${newEntries.length})`)
  refreshData()
}

// 各类文件解析器
const parseJSON = (text) => {
  const data = JSON.parse(text)
  const flat = []
  const now = Date.now()
  const flatten = (nodes, pid) => {
    if (!Array.isArray(nodes)) return
    nodes.forEach(n => {
      const entry = {
        id: n.id || uuid(),
        parentId: pid || null,
        content: n.content || n.text || '',
        version: n.version || 1,
        history: n.history || [{ version: 1, content: n.content || n.text || '', timestamp: now }],
        isDeleted: n.isDeleted || false,
        copyCount: n.copyCount || 0,
        modifyCount: n.modifyCount || 0,
        createdAt: n.createdAt || now,
        updatedAt: n.updatedAt || now
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
const parseXML = (text) => {
  const p = new DOMParser()
  const doc = p.parseFromString(text, 'text/xml')
  const flat = []
  const now = Date.now()
  const parseNode = (node, pid) => {
    for (const child of node.children) {
      if (child.tagName === 'entry' || child.tagName === 'item') {
        const c = child.getAttribute('content') || child.textContent?.trim() || ''
        flat.push({
          id: child.getAttribute('id') || uuid(),
          parentId: pid || null,
          content: c,
          version: parseInt(child.getAttribute('version')) || 1,
          history: [{ version: 1, content: c, timestamp: now }],
          isDeleted: child.getAttribute('isDeleted') === 'true',
          copyCount: parseInt(child.getAttribute('copyCount')) || 0,
          modifyCount: parseInt(child.getAttribute('modifyCount')) || 0,
          createdAt: now,
          updatedAt: now
        })
        parseNode(child, flat[flat.length - 1].id)
      }
    }
  }
  parseNode(doc.documentElement, null)
  return flat
}
const parseTXT = (text) => {
  const lines = text.split('\n').filter(l => l.trim())
  const now = Date.now()
  return lines.map(l => ({
    id: uuid(), parentId: null, content: l.trim(), version: 1,
    history: [{ version: 1, content: l.trim(), timestamp: now }],
    isDeleted: false, deletedAt: null, createdAt: now, updatedAt: now, copyCount: 0, modifyCount: 0
  }))
}
const parseYML = (text) => {
  const flat = []
  const now = Date.now()
  const lines = text.split('\n')
  const stack = [{ indent: -1, id: null }]
  for (const line of lines) {
    if (!line.trim() || line.trim().startsWith('#')) continue
    const indent = line.search(/\S/)
    const content = line.trim().replace(/^-\s*/, '').trim()
    if (!content) continue
    while (stack.length > 0 && stack[stack.length - 1].indent >= indent) stack.pop()
    const pid = stack.length > 0 ? stack[stack.length - 1].id : null
    const entry = {
      id: uuid(), parentId: pid, content, version: 1,
      history: [{ version: 1, content, timestamp: now }],
      isDeleted: false, deletedAt: null, createdAt: now, updatedAt: now, copyCount: 0, modifyCount: 0
    }
    flat.push(entry)
    stack.push({ indent, id: entry.id })
  }
  return flat
}
const parseProperties = (text) => {
  const flat = []
  const now = Date.now()
  const lines = text.split('\n')
  const pathMap = {}
  for (let line of lines) {
    line = line.trim()
    if (!line || line.startsWith('#') || line.startsWith('!')) continue
    const eq = line.indexOf('=')
    if (eq < 0) continue
    const key = line.substring(0, eq).trim()
    const val = line.substring(eq + 1).trim()
    if (!key || !val) continue
    const parts = key.split('.')
    let pid = null
    for (let i = 0; i < parts.length - 1; i++) {
      const pk = parts.slice(0, i + 1).join('.')
      if (pathMap[pk]) pid = pathMap[pk]
    }
    const entry = {
      id: uuid(), parentId: pid, content: val, version: 1,
      history: [{ version: 1, content: val, timestamp: now }],
      isDeleted: false, deletedAt: null, createdAt: now, updatedAt: now, copyCount: 0, modifyCount: 0
    }
    flat.push(entry)
    pathMap[key] = entry.id
  }
  return flat
}
const parseCSV = (text) => {
  const lines = text.split('\n').filter(l => l.trim())
  if (lines.length < 2) return []
  const headers = lines[0].split(',').map(h => h.trim().toLowerCase())
  const idCol = headers.findIndex(h => h === 'id')
  const pidCol = headers.findIndex(h => h === 'parentid' || h === 'parent_id' || h === 'parent')
  const contentCol = headers.findIndex(h => h === 'content' || h === 'text' || h === 'entry')
  if (contentCol < 0) return []
  const entries = []
  const now = Date.now()
  for (let i = 1; i < lines.length; i++) {
    const cols = lines[i].split(',').map(c => c.trim())
    if (!cols[contentCol]) continue
    entries.push({
      id: (idCol >= 0 && cols[idCol]) ? cols[idCol] : uuid(),
      parentId: (pidCol >= 0 && cols[pidCol]) ? cols[pidCol] : null,
      content: cols[contentCol],
      version: 1,
      history: [{ version: 1, content: cols[contentCol], timestamp: now }],
      isDeleted: false, deletedAt: null, createdAt: now, updatedAt: now, copyCount: 0, modifyCount: 0
    })
  }
  return entries
}

// ==================== 导出逻辑 ====================
const doExport = (format) => {
  showExportMenu.value = false
  const all = allEntries.value
  const nowStr = new Date().toISOString().slice(0, 10)
  try {
    let blob, fn
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
    }
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = fn
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
    showToast(`${t('exported')}: ${fn}`)
  } catch (err) {
    showToast('导出失败：' + err.message)
  }
}
const buildTreeForExport = (entries) => {
  const map = {}
  entries.forEach(e => map[e.id] = { ...e, children: [] })
  const roots = []
  entries.forEach(e => {
    if (e.parentId && map[e.parentId]) map[e.parentId].children.push(map[e.id])
    else roots.push(map[e.id])
  })
  const clean = (n) => {
    const { id, parentId, content, version, history, copyCount, modifyCount, createdAt, updatedAt, children } = n
    if (children.length === 0) return { id, parentId, content, version, history, copyCount, modifyCount, createdAt, updatedAt }
    return { id, parentId, content, version, history, copyCount, modifyCount, createdAt, updatedAt, children: children.map(clean) }
  }
  return { entries: roots.map(clean) }
}
const buildXML = (entries) => {
  const map = {}
  entries.forEach(e => map[e.id] = e)
  const roots = entries.filter(e => !e.parentId || !map[e.parentId])
  let xml = '<?xml version="1.0" encoding="UTF-8"?>\n<entries>\n'
  const render = (e, ind) => {
    const s = '  '.repeat(ind)
    const esc = escapeXml(e.content)
    xml += `${s}<entry id="${e.id}" parentId="${e.parentId || ''}" content="${esc}" version="${e.version}" copyCount="${e.copyCount || 0}" modifyCount="${e.modifyCount || 0}" isDeleted="${e.isDeleted}">\n`
    const children = entries.filter(c => c.parentId === e.id)
    children.forEach(c => render(c, ind + 1))
    xml += `${s}</entry>\n`
  }
  roots.forEach(r => render(r, 1))
  xml += '</entries>'
  return xml
}
const buildYML = (entries) => {
  const map = {}
  entries.forEach(e => { map[e.id] = e; });
  const roots = entries.filter(e => !e.parentId || !map[e.parentId]);
  let y = '';
  const render = (e, ind) => {
    const p = '  '.repeat(ind) + '- ';
    y += p + e.content.replace(/\n/g, '\\n') + '\n';
    const children = entries.filter(c => c.parentId === e.id);
    children.forEach(c => render(c, ind + 1));
  };
  roots.forEach(r => render(r, 0));
  return y;
};
const buildProperties = (entries) => {
  const map = {};
  entries.forEach(e => { map[e.id] = e; });
  let p = '';
  const path = (e) => {
    const parts = [];
    let cur = e;
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
const buildExcel = (entries) => {
  // 主表数据
  const mainRows = [['id', 'parentId', 'content', 'version', 'copyCount', 'modifyCount', 'createdAt', 'updatedAt', 'isDeleted', 'deletedAt']];
  entries.forEach(e => {
    mainRows.push([
      e.id,
      e.parentId || '',
      e.content,
      e.version || 1,
      e.copyCount || 0,
      e.modifyCount || 0,
      new Date(e.createdAt).toISOString(),
      new Date(e.updatedAt || e.createdAt).toISOString(),
      e.isDeleted ? 'true' : 'false',
      e.deletedAt ? new Date(e.deletedAt).toISOString() : null
    ]);
  });

  // 历史表数据
  const historyRows = [['entryId', 'version', 'content', 'timestamp']];
  entries.forEach(e => {
    if (e.history && Array.isArray(e.history)) {
      e.history.forEach(h => {
        historyRows.push([
          e.id,
          h.version,
          h.content,
          new Date(h.timestamp).toISOString()
        ]);
      });
    }
  });

  const wsMain = XLSX.utils.aoa_to_sheet(mainRows);
  const wsHistory = XLSX.utils.aoa_to_sheet(historyRows);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, wsMain, t('entries'));
  XLSX.utils.book_append_sheet(wb, wsHistory, t('historyEntries'));
  return new Uint8Array(XLSX.write(wb, { bookType: 'xlsx', type: 'array' }));
};

// 监听配置
watch(viewMode, () => saveSettings());
watch(currentTheme, () => setTheme());
watch(currentLang, () => setLang());
watch(showRecycleBin, () => refreshData());

// 页面挂载初始化
onMounted(() => {
  loadSettings();
  loadData();
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
