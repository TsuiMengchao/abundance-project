<template>
  <template v-if="forceShow && entry">
    <div class="entry-row" :class="{deleted: entry.isDeleted}" :style="{paddingLeft: (breadcrumbMode ? 10 : 12 + depth*22) + 'px'}">
            <span class="expand-icon" :class="{expanded: isExpanded, 'no-children': !hasAnyChildren}" @click.stop="toggleExpand" v-if="!breadcrumbMode && viewMode==='tree'">
              {{ hasAnyChildren ? '▶' : '·' }}
            </span>
      <span class="content-text" @click="onClickContent" :title="entry.content">
              {{ entry.isDeleted ? '🗑️ ' : '' }}{{ entry.content }}
            </span>
      <span class="meta-tags">
              <span class="tag">v{{ entry.version }}</span>
              <span class="tag" v-if="entry.copyCount>0">📋{{ entry.copyCount }}</span>
              <span class="tag" v-if="entry.modifyCount>0">✏️{{ entry.modifyCount }}</span>
            </span>
      <span class="actions" :class="{'always-visible': isRecycle}">
            <button class="btn btn-small icon-only" @click.stop="copyText" title="复制文本">📋</button>
            <button class="btn btn-small icon-only" @click.stop="addChild" title="新增子词条" v-if="!entry.isDeleted && !isRecycle">➕</button>
            <button class="btn btn-small icon-only" @click.stop="editEntry" title="编辑" v-if="!entry.isDeleted && !isRecycle">✏️</button>
            <button class="btn btn-small icon-only" @click.stop="showHistory" title="历史">📜</button>
            <button class="btn btn-small danger icon-only" @click.stop="deleteEntry" title="删除" v-if="!entry.isDeleted && !isRecycle">🗑️</button>
            <button class="btn btn-small icon-only" @click.stop="restoreEntry" title="恢复" v-if="isRecycle && isTopDeleted">♻️</button>
          </span>
    </div>
    <template v-if="!breadcrumbMode && viewMode==='tree' && isExpanded">
      <entry-row-renderer v-for="child in visibleChildren"
                          :key="child.id"
                          :entry="child"
                          :depth="depth+1"
                          :is-recycle="isRecycle"
                          :force-show="isRecycle ? true : !child.isDeleted" :breadcrumb-mode="false"
                          :expanded-ids="expandedIds"
                          :view-mode="viewMode"
                          :has-any-children-fn="hasAnyChildrenFn"
                          :get-all-children-fn="getAllChildrenFn"
                          :sort-score-fn="sortScoreFn"
                          :is-top-deleted-fn="isTopDeletedFn"
                          @update="$emit('update')">

      </entry-row-renderer>
    </template>
  </template>
</template>

<script setup lang="ts">
import { computed, type ComputedRef } from 'vue'

// 和父页面统一的词条类型
interface EntryHistoryItem {
  version: number
  content: string
  timestamp: number
}
interface Entry {
  id: string
  parentId: string | null
  content: string
  version: number
  history: EntryHistoryItem[]
  isDeleted: boolean
  deletedAt: number | null
  createdAt: number
  updatedAt: number
  copyCount: number
  modifyCount: number
}

// Props 完整类型约束
const props = defineProps<{
  entry: Entry
  depth?: number
  isRecycle?: boolean
  forceShow?: boolean
  breadcrumbMode?: boolean
  expandedIds: Set<string>
  viewMode: 'tree' | 'breadcrumb' | 'flat'
  // 工具函数类型
  hasAnyChildrenFn: (id: string) => boolean
  getAllChildrenFn: (pid: string | null) => Entry[]
  sortScoreFn: (item: Entry) => number
  isTopDeletedFn: (item: Entry) => boolean
}>()

// 事件类型约束
const emit = defineEmits<{
  update: []
  copy: [entryId: string]
  'add-child': [entryId: string]
  edit: [entryId: string]
  history: [entryId: string]
  delete: [entryId: string]
  restore: [entryId: string]
  drill: [entryId: string]
}>()

// 简写绑定
const viewMode = props.viewMode
const expandedIds = props.expandedIds

// 计算：当前条目是否存在子项
const hasAnyChildren: ComputedRef<boolean> = computed(() => {
  return props.hasAnyChildrenFn(props.entry.id)
})
const sortScore = props.sortScoreFn
// 计算：是否为顶层删除条目
const isTopDeleted: ComputedRef<boolean> = computed(() => {
  return props.isTopDeletedFn(props.entry)
})
const isExpanded = computed(() => expandedIds.has(props.entry.id))
// 计算：当前展示的子条目列表
const visibleChildren = computed(() => {
  const all = props.getAllChildrenFn(props.entry.id) || []
  const filtered = props.isRecycle ? all : all.filter(c => !c.isDeleted)
  return filtered.sort((a, b) => props.sortScoreFn(b) - props.sortScoreFn(a))
})

// 展开/折叠
const toggleExpand = () => {
  if (!props.hasAnyChildrenFn(props.entry.id) && !props.isRecycle) return
  if (expandedIds.has(props.entry.id)) {
    expandedIds.delete(props.entry.id)
  } else {
    expandedIds.add(props.entry.id)
  }
  emit('update')
}

// 点击条目内容
const onClickContent = () => {
  if (props.breadcrumbMode) {
    emit('drill', props.entry.id)
  } else if (viewMode === 'tree') {
    toggleExpand()
  }
}

// 操作事件转发
const copyText = () => emit('copy', props.entry.id)
const addChild = () => emit('add-child', props.entry.id)
const editEntry = () => emit('edit', props.entry.id)
const showHistory = () => emit('history', props.entry.id)
const deleteEntry = () => emit('delete', props.entry.id)
const restoreEntry = () => emit('restore', props.entry.id)
</script>

<style scoped>
/* ===== 条目行容器 ===== */
.entry-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  transition: background var(--transition);
  min-height: 42px;
  font-size: 0.9rem;
}

.entry-row:hover { background: var(--bg3); }

.entry-row.deleted { opacity: 0.7; background: rgba(212,153,42,0.06); }

/* ===== 缩进占位（当前模板未使用 .indent-spacer 类，实际缩进通过 :style 实现，可移除） ===== */
.entry-row .indent-spacer { flex-shrink: 0; }

/* ===== 展开/折叠图标 ===== */
.entry-row .expand-icon {
  flex-shrink: 0;
  width: 20px;
  text-align: center;
  cursor: pointer;
  font-size: 0.75rem;
  color: var(--text2);
  transition: transform var(--transition);
  user-select: none;
}

.entry-row .expand-icon.expanded { transform: rotate(90deg); }
.entry-row .expand-icon.no-children { opacity: 0.3; cursor: default; }

/* ===== 内容文本 ===== */
.entry-row .content-text {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  min-width: 0;
  font-weight: 500;
}

/* ===== 元数据标签 ===== */
.entry-row .meta-tags {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
  font-size: 0.7rem;
}

.entry-row .tag {
  padding: 2px 8px;
  border-radius: 12px;
  background: var(--tag-bg);
  color: var(--tag-text);
  font-size: 0.7rem;
  white-space: nowrap;
  font-weight: 600;
}

.entry-row .tag.current {
  background: var(--success);
  color: #fff;
}

/* ===== 操作按钮组 ===== */
.entry-row .actions {
  display: flex;
  gap: 3px;
  flex-shrink: 0;
  opacity: 0;
  transition: opacity var(--transition);
}

.entry-row:hover .actions { opacity: 1; }

.entry-row .actions.always-visible { opacity: 1; }

/* ===== 响应式 ===== */
@media (max-width: 640px) {
  .header .title { font-size: 1rem; }
  .search-input { width: 130px; }
  /* 注意：原样式中 .entry-row .actions 在移动端强制可见，此处保留 */
  .entry-row .actions { opacity: 1; }
}
</style>
