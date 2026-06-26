
  const { createApp, ref, computed, watch, onMounted } = Vue;

  // ===================== 1. 国际化配置（不变） =====================
  const i18n = {
  'zh-CN': { appTitle: '词条阅读器', recycleBin: '回收站', backToHome: '返回主页', addRoot: '新增根词条', treeView: '树形', breadcrumbView: '层级导航', flatView: '平铺', lightTheme: '浅色', darkTheme: '深色', import: '导入', export: '导出', exportAs: '导出格式', cancel: '取消', close: '关闭', searchPlaceholder: '搜索词条...', results: '条结果', totalEntries: '总词条', activeEntries: '活跃', root: '根', emptyRecycle: '回收站为空', emptyHint: '暂无词条', addFirst: '新增第一个词条', noChildren: '暂无子词条', addHere: '在此新增', historyFor: '历史版本', current: '当前', restore: '恢复', noHistory: '暂无历史记录', edit: '编辑', delete: '删除', copy: '复制', confirmDelete: '确定删除此词条？', restored: '已恢复', copied: '已复制', saved: '已保存', imported: '导入成功', exported: '导出成功', versionRestored: '版本已恢复', contentUnchanged: '内容未变化', multiAddHint: '每隔一个空行一个词条（可批量创建）', editEntry: '编辑词条', addEntry: '新增词条', save: '保存', add: '新增', entries: '词条', historyEntries: '历史词条' },
  'zh-TW': { appTitle: '詞條閱讀器', recycleBin: '回收桶', backToHome: '返回主頁', addRoot: '新增根詞條', treeView: '樹形', breadcrumbView: '層級導航', flatView: '平鋪', lightTheme: '淺色', darkTheme: '深色', import: '匯入', export: '匯出', exportAs: '匯出格式', cancel: '取消', close: '關閉', searchPlaceholder: '搜尋詞條...', results: '條結果', totalEntries: '總詞條', activeEntries: '活躍', root: '根', emptyRecycle: '回收桶為空', emptyHint: '暫無詞條', addFirst: '新增第一個詞條', noChildren: '暫無子詞條', addHere: '在此新增', historyFor: '歷史版本', current: '當前', restore: '恢復', noHistory: '暫無歷史記錄', edit: '編輯', delete: '刪除', copy: '複製', confirmDelete: '確定刪除此詞條？', restored: '已恢復', copied: '已複製', saved: '已儲存', imported: '匯入成功', exported: '匯出成功', versionRestored: '版本已恢復', contentUnchanged: '內容未變化', multiAddHint: '每隔一個空行一個詞條（可批量建立）', editEntry: '編輯詞條', addEntry: '新增詞條', save: '儲存', add: '新增', entries: '詞條', historyEntries: '歷史詞條' },
  'en': { appTitle: 'Entry Reader', recycleBin: 'Recycle Bin', backToHome: 'Back to Home', addRoot: 'Add Root', treeView: 'Tree', breadcrumbView: 'Breadcrumb', flatView: 'Flat', lightTheme: 'Light', darkTheme: 'Dark', import: 'Import', export: 'Export', exportAs: 'Export As', cancel: 'Cancel', close: 'Close', searchPlaceholder: 'Search...', results: 'results', totalEntries: 'Total', activeEntries: 'Active', root: 'Root', emptyRecycle: 'Recycle bin empty', emptyHint: 'No entries', addFirst: 'Add first', noChildren: 'No children', addHere: 'Add here', historyFor: 'History for', current: 'Current', restore: 'Restore', noHistory: 'No history', edit: 'Edit', delete: 'Delete', copy: 'Copy', confirmDelete: 'Delete this entry?', restored: 'Restored', copied: 'Copied', saved: 'Saved', imported: 'Imported', exported: 'Exported', versionRestored: 'Version restored', contentUnchanged: 'Content unchanged', multiAddHint: 'One entry every other blank line', editEntry: 'Edit Entry', addEntry: 'Add Entry', save: 'Save', add: 'Add', entries: 'Entry', historyEntries: 'History Entry' }
};

  // ===================== 2. 工具函数（不变） =====================
  function uuid() { return 'e_' + Date.now().toString(36) + '_' + Math.random().toString(36).substring(2,8); }
  function similarity(a,b){ const al=a.toLowerCase(); const bl=b.toLowerCase(); if(al.includes(bl)||bl.includes(al)) return 0.7+Math.min(al.length,bl.length)/Math.max(al.length,bl.length)*0.3; const len=Math.max(al.length,bl.length); if(len===0) return 1; const d=levenshteinDistance(al,bl); return Math.max(0,1-d/len); }
  function levenshteinDistance(a,b){ const m=a.length,n=b.length; const dp=Array.from({length:m+1},()=>Array(n+1).fill(0)); for(let i=0;i<=m;i++)dp[i][0]=i; for(let j=0;j<=n;j++)dp[0][j]=j; for(let i=1;i<=m;i++) for(let j=1;j<=n;j++) dp[i][j]=Math.min(dp[i-1][j]+1,dp[i][j-1]+1,dp[i-1][j-1]+(a[i-1]===b[j-1]?0:1)); return dp[m][n]; }

  // ===================== 3. IndexedDB 封装（核心新增） =====================
  /**
  * 浏览器数据库：两张表
  * 1. entries：词条主数据（扁平化存储，树形通过parentId关联）
  * 2. history：修改历史（关联entryId）
  */
  class EntryDB {
  constructor() {
  this.dbName = 'entryReaderDB';
  this.version = 1;
  this.db = null;
}

  // 初始化数据库&创建表
  init() {
  return new Promise((resolve, reject) => {
  const request = indexedDB.open(this.dbName, this.version);

  // 版本更新/首次创建：建表
  request.onupgradeneeded = (e) => {
  this.db = e.target.result;

  // 词条表：主键id，索引parentId/isDeleted
  if (!this.db.objectStoreNames.contains('entries')) {
  const entriesStore = this.db.createObjectStore('entries', { keyPath: 'id' });
  entriesStore.createIndex('parentId', 'parentId', { unique: false });
  entriesStore.createIndex('isDeleted', 'isDeleted', { unique: false });
}

  // 历史表：自增主键，索引entryId+version（唯一）
  if (!this.db.objectStoreNames.contains('history')) {
  const historyStore = this.db.createObjectStore('history', { autoIncrement: true });
  historyStore.createIndex('entryId', 'entryId', { unique: false });
  historyStore.createIndex('entryId_version', ['entryId', 'version'], { unique: true });
}
};

  request.onsuccess = (e) => {
  this.db = e.target.result;
  resolve();
};
  request.onerror = (e) => reject(e.target.error);
});
}

  // 保存数据：拆分主数据+历史，分别存储
  async saveEntries(entries) {
  return new Promise((resolve, reject) => {
  const tx = this.transaction(['entries', 'history'], 'readwrite');
  const entriesStore = tx.objectStore('entries');
  const historyStore = tx.objectStore('history');

  // 清空旧数据
  entriesStore.clear();
  historyStore.clear();

  // 批量写入
  entries.forEach(entry => {
  // 拆分：主数据（不含history）
  const { history, ...entryData } = entry;
  entriesStore.put(entryData);

  // 拆分：历史数据（关联entryId）
  if (Array.isArray(history) && history.length) {
  history.forEach(h => historyStore.put({ entryId: entry.id, ...h }));
}
});

  tx.oncomplete = () => resolve();
  tx.onerror = (e) => reject(e.target.error);
});
}

  // 加载数据：关联主数据+历史，还原原有结构
  async loadEntries() {
  return new Promise((resolve, reject) => {
  const tx = this.transaction(['entries', 'history'], 'readonly');
  const entriesStore = tx.objectStore('entries');
  const historyStore = tx.objectStore('history');

  let entries = [], historyList = [];
  entriesStore.getAll().onsuccess = e => entries = e.target.result;
  historyStore.getAll().onsuccess = e => historyList = e.target.result;

  tx.oncomplete = () => {
  // 按entryId分组历史
  const historyMap = {};
  historyList.forEach(h => {
  if (!historyMap[h.entryId]) historyMap[h.entryId] = [];
  historyMap[h.entryId].push(h);
});
  // 合并历史到词条，还原原有结构
  const result = entries.map(entry => ({
  ...entry,
  history: historyMap[entry.id] || []
}));
  resolve(result);
};
  tx.onerror = (e) => reject(e.target.error);
});
}

  // 创建事务
  transaction(storeNames, mode = 'readonly') {
  return this.db.transaction(storeNames, mode);
}
}

  // 全局数据库实例
  const entryDB = new EntryDB();

  // 配置项存储key（保留localStorage）
  const SETTINGS_KEY = 'entry-reader-settings';

  // ===================== 4. Vue 应用（仅修改存储相关方法） =====================
  const app = createApp({
  data() {
  return {
  allEntries: [],
  showRecycleBin: false,
  viewMode: 'tree',
  currentTheme: 'light',
  currentLang: 'zh-CN',
  searchQuery: '',
  showExportMenu: false,
  historyModalVisible: false,
  historyEntry: null,
  breadcrumbStack: [],
  toastMsg: '',
  toastTimer: null,
  expandedIds: new Set(),
  editModal: { visible: false, mode: 'add', parentId: null, entryId: null, content: '' },
};
},
  computed: {
  entryMap() { const map={}; this.allEntries.forEach(e=>{ map[e.id]=e; }); return map; },
  childrenMap() {
  const map={};
  this.allEntries.forEach(e=>{ const pid=e.parentId||'__root__'; if(!map[pid]) map[pid]=[]; map[pid].push(e); });
  for(const key in map) map[key].sort((a,b)=>this.sortScore(b)-this.sortScore(a));
  return map;
},
  rootEntries() { return (this.childrenMap['__root__']||[]).filter(e=>!e.isDeleted); },
  deletedRootEntries() {
  return this.allEntries.filter(e=>e.isDeleted).filter(e=>{
  if(!e.parentId) return true;
  const p=this.entryMap[e.parentId]; return !p||!p.isDeleted;
});
},
  displayEntries() {
  if(this.viewMode==='flat'){
  let list = this.showRecycleBin ? this.allEntries.filter(e=>e.isDeleted) : this.allEntries.filter(e=>!e.isDeleted);
  if(this.searchQuery) list = list.filter(e=>similarity(e.content,this.searchQuery)>0.25);
  list.sort((a,b)=>this.sortScore(b)-this.sortScore(a));
  return list;
}
  if(this.viewMode==='tree'){
  if(this.showRecycleBin){
  let roots = this.deletedRootEntries;
  if(this.searchQuery) roots = roots.filter(e=>similarity(e.content,this.searchQuery)>0.25);
  return roots;
}
  let roots = this.rootEntries;
  if(this.searchQuery){
  const allActive = this.allEntries.filter(e=>!e.isDeleted);
  return allActive.filter(e=>similarity(e.content,this.searchQuery)>0.25).sort((a,b)=>this.sortScore(b)-this.sortScore(a));
}
  return roots;
}
  if(this.viewMode==='breadcrumb'){
  let parentId = null;
  if(this.breadcrumbStack.length>0) parentId = this.breadcrumbStack[this.breadcrumbStack.length-1].id;
  let list;
  if(this.showRecycleBin){
  list = parentId ? this.allEntries.filter(e=>e.parentId===parentId) : this.deletedRootEntries;
} else {
  list = parentId ? this.getChildren(parentId) : this.rootEntries;
}
  if(this.searchQuery) list = list.filter(e=>similarity(e.content,this.searchQuery)>0.25);
  return list.sort((a,b)=>this.sortScore(b)-this.sortScore(a));
}
  return [];
},
  activeCount() { return this.allEntries.filter(e=>!e.isDeleted).length; },
  deletedCount() { return this.allEntries.filter(e=>e.isDeleted).length; },
  filteredCount() { return this.displayEntries.length; },
},
  methods: {
  t(key) { return (i18n[this.currentLang]||i18n['zh-CN'])[key]||key; },
  formatTime(ts) { if(!ts) return ''; return new Date(ts).toLocaleString(this.currentLang==='en'?'en-US':'zh-CN',{month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'}); },
  sortScore(e){
  const now=Date.now(); const age=(now-(e.updatedAt||e.createdAt||now))/3600000;
  return (1/(1+age*0.1))*10 + (e.copyCount||0)*0.5 + (e.modifyCount||0)*0.3;
},
  getChildren(pid) { return (this.childrenMap[pid||'__root__']||[]).filter(e=>!e.isDeleted); },
  getAllChildren(pid) { return this.childrenMap[pid||'__root__']||[]; },
  isTopDeleted(entry) {
  if(!entry.isDeleted) return false;
  if(!entry.parentId) return true;
  const p=this.entryMap[entry.parentId]; return !p||!p.isDeleted;
},
  hasAnyChildren(id) { return (this.childrenMap[id]||[]).length>0; },

  // ===================== 存储方法：替换为 IndexedDB =====================
  async saveData() {
  try { await entryDB.saveEntries(this.allEntries); }
  catch (e) { console.error('保存失败', e); this.showToast('保存失败'); }
},
  async loadData() {
  try { this.allEntries = await entryDB.loadEntries(); }
  catch (e) { console.error('加载失败', e); this.allEntries = []; }
  if (!Array.isArray(this.allEntries)) this.allEntries = [];
},
  // ================================================================

  // 其余所有业务方法（完全不变）
  copyEntryText(entryId) {
  const entry = this.entryMap[entryId];
  if(!entry) return;
  navigator.clipboard.writeText(entry.content).then(()=>{
  entry.copyCount = (entry.copyCount||0)+1;
  this.saveData();
  this.showToast('📋 '+this.t('copied'));
}).catch(()=>{
  const ta=document.createElement('textarea'); ta.value=entry.content; document.body.appendChild(ta); ta.select(); document.execCommand('copy'); document.body.removeChild(ta);
  entry.copyCount = (entry.copyCount||0)+1; this.saveData(); this.showToast('📋 '+this.t('copied'));
});
},
  openAddModal(parentId) { this.editModal = { visible:true, mode:'add', parentId:parentId||null, entryId:null, content:'' }; },
  openEditModal(entryId) { const e=this.entryMap[entryId]; if(!e) return; this.editModal = { visible:true, mode:'edit', parentId:null, entryId, content:e.content }; },
  cancelEditModal() { this.editModal.visible=false; },
  async submitEditModal() {
  const {mode,parentId,entryId,content}=this.editModal;
  if(!content.trim()){ this.showToast('内容不能为空'); return; }
  if(mode==='add'){
  const lines=content.split('\n\n').filter(l=>l.trim());
  if(lines.length===0) return;
  const now=Date.now();
  const newEntries=lines.map(line=>({id:uuid(),parentId:parentId||null,content:line.trim(),version:1,history:[{version:1,content:line.trim(),timestamp:now}],isDeleted:false,deletedAt:null,createdAt:now,updatedAt:now,copyCount:0,modifyCount:0}));
  this.allEntries.push(...newEntries); await this.saveData(); this.showToast(this.t('saved')+` (${newEntries.length})`);
} else {
  const entry=this.entryMap[entryId]; if(!entry) return;
  const newContent=content.trim();
  if(newContent===entry.content){ this.showToast(this.t('contentUnchanged')); this.editModal.visible=false; return; }
  const now=Date.now(); entry.content=newContent; entry.version=(entry.version||0)+1; entry.modifyCount=(entry.modifyCount||0)+1; entry.updatedAt=now;
  if(!entry.history) entry.history=[]; entry.history.push({version:entry.version,content:newContent,timestamp:now});
  await this.saveData(); this.showToast(this.t('saved')+' v'+entry.version);
}
  this.editModal.visible=false; this.refreshData();
},
  async deleteEntry(id) {
  const e=this.entryMap[id]; if(!e) return;
  if(!confirm(this.t('confirmDelete')+'\n\n'+e.content.substring(0,60))) return;
  e.isDeleted=true; e.deletedAt=Date.now(); e.updatedAt=Date.now();
  await this.saveData(); this.showToast('🗑️ '+this.t('deleted')); this.refreshData();
},
  async restoreEntry(id) {
  const e=this.entryMap[id]; if(!e||!e.isDeleted) return;
  e.isDeleted=false; e.deletedAt=null; e.updatedAt=Date.now();
  await this.saveData(); this.showToast('♻️ '+this.t('restored')); this.refreshData();
},
  showHistory(id) { this.historyEntry=this.entryMap[id]; this.historyModalVisible=true; },
  async restoreVersion(entryId,version){
  const e=this.entryMap[entryId]; if(!e) return;
  const hist=e.history?.find(h=>h.version===version); if(!hist) return;
  const now=Date.now(); e.content=hist.content; e.version=(e.version||0)+1; e.modifyCount=(e.modifyCount||0)+1; e.updatedAt=now;
  e.history.push({version:e.version,content:hist.content,timestamp:now});
  await this.saveData(); this.showToast(this.t('versionRestored')+' → v'+e.version);
  this.historyModalVisible=false; this.refreshData();
},
  drillDownList(entryId) {
  const entry=this.entryMap[entryId]; if(!entry) return;
  this.breadcrumbStack.push({id:entry.id, content:entry.content});
  this.refreshData();
},
  navBreadcrumb(idx) {
  if(idx<0){ this.breadcrumbStack=[]; this.refreshData(); return; }
  this.breadcrumbStack = this.breadcrumbStack.slice(0, idx+1);
  this.refreshData();
},
  onViewModeChange() {
  this.breadcrumbStack=[]; this.expandedIds.clear(); this.refreshData();
},
  toggleRecycleBin() {
  this.showRecycleBin=!this.showRecycleBin; this.breadcrumbStack=[]; this.expandedIds.clear();
  this.searchQuery=''; this.refreshData();
},
  onSearch() {
  this.expandedIds.clear();
  if(this.searchQuery && this.viewMode==='tree' && !this.showRecycleBin){
  const allActive=this.allEntries.filter(e=>!e.isDeleted);
  allActive.forEach(e=>{ if(similarity(e.content,this.searchQuery)>0.25){ let cur=e.parentId?this.entryMap[e.parentId]:null; while(cur){ this.expandedIds.add(cur.id); cur=cur.parentId?this.entryMap[cur.parentId]:null; } } });
}
  this.refreshData();
},
  loadSettings() {
  const raw=localStorage.getItem(SETTINGS_KEY); if(raw){ try{ const s=JSON.parse(raw); if(s.theme) this.currentTheme=s.theme; if(s.lang) this.currentLang=s.lang; if(s.viewMode) this.viewMode=s.viewMode; }catch(e){} }
  this.setTheme();
},
  saveSettings() { localStorage.setItem(SETTINGS_KEY, JSON.stringify({theme:this.currentTheme,lang:this.currentLang,viewMode:this.viewMode})); },
  setTheme() { document.documentElement.setAttribute('data-theme', this.currentTheme); this.saveSettings(); },
  setLang() { this.saveSettings(); },
  refreshData() { this.allEntries=[...this.allEntries]; },
  showToast(msg) { this.toastMsg=msg; if(this.toastTimer) clearTimeout(this.toastTimer); this.toastTimer=setTimeout(()=>{ this.toastMsg=''; },2500); },
  triggerImport() { this.$refs.importFileInput.value=''; this.$refs.importFileInput.click(); },
  handleImportFile(e) {
  const file=e.target.files[0]; if(!file) return;
  const ext=file.name.split('.').pop().toLowerCase();
  const reader=new FileReader();
  reader.onload=(ev)=>{
  const text=ev.target.result;
  try{
  let entries=[];
  if(ext==='json') entries=this.parseJSON(text);
  else if(ext==='xml') entries=this.parseXML(text);
  else if(ext==='txt') entries=this.parseTXT(text);
  else if(ext==='yml'||ext==='yaml') entries=this.parseYML(text);
  else if(ext==='properties') entries=this.parseProperties(text);
  else if(ext==='xlsx'||ext==='xls'){ this.handleExcelImport(file); return; }
  else if(ext==='csv') entries=this.parseCSV(text);
  else { this.showToast('Unsupported format'); return; }
  if(entries.length===0){ this.showToast('No entries'); return; }
  this.mergeImportedEntries(entries);
}catch(err){ this.showToast('Import error: '+err.message); }
};
  reader.readAsText(file);
},
  handleExcelImport(file) {
  const reader=new FileReader();
  reader.onload=(ev)=>{
  try{
  const data=new Uint8Array(ev.target.result);
  const wb=XLSX.read(data,{type:'array'});
  const sheet1 = wb.Sheets[wb.SheetNames[0]];
  if(!sheet1) { this.showToast('Excel 缺少第一个工作表'); return; }
  const rows1 = XLSX.utils.sheet_to_json(sheet1, { header:1 });
  if(rows1.length < 2) { this.showToast('主表为空'); return; }
  let historyMap = {};
  if(wb.SheetNames.length > 1) {
  const sheet2 = wb.Sheets[wb.SheetNames[1]];
  const rows2 = XLSX.utils.sheet_to_json(sheet2, { header:1 });
  if(rows2.length > 1) {
  const headers2 = rows2[0].map(h=>String(h).toLowerCase().trim());
  const eidIdx = headers2.indexOf('entryid');
  const verIdx = headers2.indexOf('version');
  const contIdx = headers2.indexOf('content');
  const timeIdx = headers2.indexOf('timestamp');
  for(let i=1; i<rows2.length; i++) {
  const row = rows2[i];
  if(!row) continue;
  const eid = row[eidIdx]?.toString() || '';
  const ver = parseInt(row[verIdx]) || 1;
  const cont = row[contIdx]?.toString() || '';
  const ts = new Date(row[timeIdx]).getTime() || Date.now();
  if(!eid) continue;
  if(!historyMap[eid]) historyMap[eid] = [];
  historyMap[eid].push({ version: ver, content: cont, timestamp: ts });
}
}
}
  const headers1 = rows1[0].map(h=>String(h).toLowerCase().trim());
  const idCol = headers1.indexOf('id');
  const pidCol = headers1.indexOf('parentid');
  const contentCol = headers1.indexOf('content');
  const versionCol = headers1.indexOf('version');
  const copyCountCol = headers1.indexOf('copycount');
  const modifyCountCol = headers1.indexOf('modifycount');
  const createdAtCol = headers1.indexOf('createdat');
  const updatedAtCol = headers1.indexOf('updatedat');
  const isDeletedCol = headers1.indexOf('isdeleted');
  const deletedAtCol = headers1.indexOf('deletedat');
  if(contentCol < 0) { this.showToast('主表缺少 content 列'); return; }
  const oldIdMap = {};
  const newEntries = [];
  const now = Date.now();
  for(let i=1; i<rows1.length; i++) {
  const row = rows1[i];
  if(!row || !row[contentCol]) continue;
  const oldId = (idCol>=0 && row[idCol]) ? String(row[idCol]) : uuid();
  const newId = uuid();
  oldIdMap[oldId] = newId;
  const entry = {
  id: newId, parentId: (pidCol>=0 && row[pidCol]) ? String(row[pidCol]) : null, content: String(row[contentCol]).trim(),
  version: (versionCol>=0 && row[versionCol]) ? parseInt(row[versionCol])||1 : 1,
  copyCount: (copyCountCol>=0) ? (parseInt(row[copyCountCol])||0) : 0,
  modifyCount: (modifyCountCol>=0) ? (parseInt(row[modifyCountCol])||0) : 0,
  createdAt: (createdAtCol>=0) ? (new Date(row[createdAtCol]).getTime()||now) : now,
  updatedAt: (updatedAtCol>=0) ? (new Date(row[updatedAtCol]).getTime()||now) : now,
  isDeleted: (isDeletedCol>=0) ? (String(row[isDeletedCol]).toLowerCase()==='true') : false,
  deletedAt: (deletedAtCol>=0) ? (new Date(row[deletedAtCol]).getTime()||null) : null, history: []
};
  newEntries.push(entry);
}
  for(const entry of newEntries) {
  if(entry.parentId && oldIdMap[entry.parentId]) { entry.parentId = oldIdMap[entry.parentId]; }
  let oldIdForEntry = null;
  for(const [old, nid] of Object.entries(oldIdMap)) { if(nid === entry.id) { oldIdForEntry = old; break; } }
  if(oldIdForEntry && historyMap[oldIdForEntry]) {
  entry.history = historyMap[oldIdForEntry].sort((a,b)=>a.version-b.version);
  if(entry.history.length > 0) { const maxVer = Math.max(...entry.history.map(h=>h.version)); entry.version = maxVer; }
} else {
  entry.history = [{ version: entry.version || 1, content: entry.content, timestamp: entry.createdAt }];
}
}
  this.allEntries.push(...newEntries); this.saveData(); this.showToast(this.t('imported') + ` (${newEntries.length} 条词条)`); this.refreshData();
}catch(err){ console.error(err); this.showToast('Excel 导入错误: '+err.message); }
};
  reader.readAsArrayBuffer(file);
},
  async mergeImportedEntries(newEntries) {
  const idMap={}; newEntries.forEach(e=>{ const old=e.id; const nid=uuid(); idMap[old]=nid; e.id=nid; });
  newEntries.forEach(e=>{ if(e.parentId&&idMap[e.parentId]) e.parentId=idMap[e.parentId]; });
  this.allEntries.push(...newEntries); await this.saveData(); this.showToast(this.t('imported')+` (${newEntries.length})`); this.refreshData();
},
  parseJSON(text){ const data=JSON.parse(text); if(Array.isArray(data)) return data.map(e=>({...e,id:e.id||uuid(),version:e.version||1,history:e.history||[{version:1,content:e.content,timestamp:Date.now()}],isDeleted:e.isDeleted||false,copyCount:e.copyCount||0,modifyCount:e.modifyCount||0,createdAt:e.createdAt||Date.now(),updatedAt:e.updatedAt||Date.now()})); const flat=[]; const flatten=(nodes,pid)=>{ if(!Array.isArray(nodes)) return; nodes.forEach(n=>{ const now=Date.now(); const entry={id:n.id||uuid(),parentId:pid||null,content:n.content||n.text||'',version:n.version||1,history:n.history||[{version:1,content:n.content||n.text||'',timestamp:now}],isDeleted:n.isDeleted||false,copyCount:n.copyCount||0,modifyCount:n.modifyCount||0,createdAt:n.createdAt||now,updatedAt:n.updatedAt||now}; flat.push(entry); if(n.children) flatten(n.children,entry.id); }); }; if(data.entries) flatten(data.entries,null); else if(data.children) flatten(data.children,null); else flatten([data],null); return flat; },
  parseXML(text){ const p=new DOMParser(); const doc=p.parseFromString(text,'text/xml'); const flat=[]; const parseNode=(node,pid)=>{ for(const child of node.children){ if(child.tagName==='entry'||child.tagName==='item'){ const now=Date.now(); const c=child.getAttribute('content')||child.textContent?.trim()||''; flat.push({id:child.getAttribute('id')||uuid(),parentId:pid||null,content:c,version:parseInt(child.getAttribute('version'))||1,history:[{version:1,content:c,timestamp:now}],isDeleted:child.getAttribute('isDeleted')==='true',copyCount:parseInt(child.getAttribute('copyCount'))||0,modifyCount:parseInt(child.getAttribute('modifyCount'))||0,createdAt:now,updatedAt:now}); parseNode(child,flat[flat.length-1].id); } } }; parseNode(doc.documentElement,null); return flat; },
  parseTXT(text){ const lines=text.split('\n').filter(l=>l.trim()); const now=Date.now(); return lines.map(l=>({id:uuid(),parentId:null,content:l.trim(),version:1,history:[{version:1,content:l.trim(),timestamp:now}],isDeleted:false,deletedAt:null,createdAt:now,updatedAt:now,copyCount:0,modifyCount:0})); },
  parseYML(text){ const flat=[]; const now=Date.now(); const lines=text.split('\n'); const stack=[{indent:-1,id:null}]; for(let line of lines){ if(!line.trim()||line.trim().startsWith('#')) continue; const indent=line.search(/\S/); const content=line.trim().replace(/^-\s*/,'').trim(); if(!content) continue; while(stack.length>0&&stack[stack.length-1].indent>=indent) stack.pop(); const pid=stack.length>0?stack[stack.length-1].id:null; const entry={id:uuid(),parentId:pid,content,version:1,history:[{version:1,content,timestamp:now}],isDeleted:false,deletedAt:null,createdAt:now,updatedAt:now,copyCount:0,modifyCount:0}; flat.push(entry); stack.push({indent,id:entry.id}); } return flat; },
  parseProperties(text){ const flat=[]; const now=Date.now(); const lines=text.split('\n'); const pathMap={}; for(let line of lines){ line=line.trim(); if(!line||line.startsWith('#')||line.startsWith('!')) continue; const eq=line.indexOf('='); if(eq<0) continue; const key=line.substring(0,eq).trim(); const val=line.substring(eq+1).trim(); if(!key||!val) continue; const parts=key.split('.'); let pid=null; for(let i=0;i<parts.length-1;i++){ const pk=parts.slice(0,i+1).join('.'); if(pathMap[pk]) pid=pathMap[pk]; } const entry={id:uuid(),parentId:pid,content:val,version:1,history:[{version:1,content:val,timestamp:now}],isDeleted:false,deletedAt:null,createdAt:now,updatedAt:now,copyCount:0,modifyCount:0}; flat.push(entry); pathMap[key]=entry.id; } return flat; },
  parseCSV(text){ const lines=text.split('\n').filter(l=>l.trim()); if(lines.length<2) return []; const headers=lines[0].split(',').map(h=>h.trim().toLowerCase()); const idCol=headers.findIndex(h=>h==='id'); const pidCol=headers.findIndex(h=>h==='parentid'||h==='parent_id'||h==='parent'); const contentCol=headers.findIndex(h=>h==='content'||h==='text'||h==='entry'); if(contentCol<0) return []; const entries=[]; const now=Date.now(); for(let i=1;i<lines.length;i++){ const cols=lines[i].split(',').map(c=>c.trim()); if(!cols[contentCol]) continue; entries.push({id:(idCol>=0&&cols[idCol])?cols[idCol]:uuid(),parentId:(pidCol>=0&&cols[pidCol])?cols[pidCol]:null,content:cols[contentCol],version:1,history:[{version:1,content:cols[contentCol],timestamp:now}],isDeleted:false,deletedAt:null,createdAt:now,updatedAt:now,copyCount:0,modifyCount:0}); } return entries; },
  doExport(format) {
  this.showExportMenu = false;
  const active = this.allEntries;
  let blob, fn;
  const nowStr = new Date().toISOString().slice(0,10);
  try {
  switch(format) {
  case 'json': blob = new Blob([JSON.stringify(this.buildTreeForExport(active), null, 2)], {type:'application/json'}); fn=`entries_${nowStr}.json`; break;
  case 'xml': blob = new Blob([this.buildXML(active)], {type:'application/xml'}); fn=`entries_${nowStr}.xml`; break;
  case 'txt': blob = new Blob([active.filter(e=>!e.parentId).map(e=>e.content).join('\n')], {type:'text/plain'}); fn=`entries_${nowStr}.txt`; break;
  case 'yml': blob = new Blob([this.buildYML(active)], {type:'text/yaml'}); fn=`entries_${nowStr}.yml`; break;
  case 'properties': blob = new Blob([this.buildProperties(active)], {type:'text/plain'}); fn=`entries_${nowStr}.properties`; break;
  case 'excel': blob = new Blob([this.buildExcel(active)], {type:'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}); fn=`entries_${nowStr}.xlsx`; break;
}
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a'); a.href = url; a.download = fn;
  document.body.appendChild(a); a.click(); document.body.removeChild(a);
  URL.revokeObjectURL(url);
  this.showToast(this.t('exported')+': '+fn);
} catch(err) { this.showToast('Export error: '+err.message); }
},
  buildTreeForExport(entries){ const map={}; entries.forEach(e=>{ map[e.id]={...e,children:[]}; }); const roots=[]; entries.forEach(e=>{ if(e.parentId&&map[e.parentId]) map[e.parentId].children.push(map[e.id]); else roots.push(map[e.id]); }); const clean=n=>{ const {id,parentId,content,version,history,copyCount,modifyCount,createdAt,updatedAt,children}=n; if(children.length===0) return {id,parentId,content,version,history,copyCount,modifyCount,createdAt,updatedAt}; return {id,parentId,content,version,history,copyCount,modifyCount,createdAt,updatedAt,children:children.map(clean)}; }; return {entries:roots.map(clean)}; },
  buildXML(entries){ const map={}; entries.forEach(e=>{ map[e.id]=e; }); const roots=entries.filter(e=>!e.parentId||!map[e.parentId]); let xml='<?xml version="1.0" encoding="UTF-8"?>\n<entries>\n'; const render=(e,ind)=>{ const s='  '.repeat(ind); const esc=e.content.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); xml+=`${s}<entry id="${e.id}" parentId="${e.parentId||''}" content="${esc}" version="${e.version}" copyCount="${e.copyCount||0}" modifyCount="${e.modifyCount||0}" isDeleted="false">\n`; const children=entries.filter(c=>c.parentId===e.id); children.forEach(c=>render(c,ind+1)); xml+=`${s}</entry>\n`; }; roots.forEach(r=>render(r,1)); xml+='</entries>'; return xml; },
  buildYML(entries){ const map={}; entries.forEach(e=>{ map[e.id]=e; }); const roots=entries.filter(e=>!e.parentId||!map[e.parentId]); let y=''; const render=(e,ind)=>{ const p='  '.repeat(ind)+'- '; y+=p+e.content.replace(/\n/g,'\\n')+'\n'; const children=entries.filter(c=>c.parentId===e.id); children.forEach(c=>render(c,ind+1)); }; roots.forEach(r=>render(r,0)); return y; },
  buildProperties(entries){ const map={}; entries.forEach(e=>{ map[e.id]=e; }); let p=''; const path=(e)=>{ const parts=[]; let cur=e; while(cur){ parts.unshift(cur.content.replace(/[.=]/g,'_').replace(/\s+/g,'_')); cur=cur.parentId?map[cur.parentId]:null; } return parts.join('.'); }; entries.forEach(e=>{ p+=path(e)+'='+e.content.replace(/\n/g,'\\n')+'\n'; }); return p; },
  buildExcel(entries) {
  const mainRows = [['id', 'parentId', 'content', 'version', 'copyCount', 'modifyCount', 'createdAt', 'updatedAt', 'isDeleted', 'deletedAt']];
  entries.forEach(e => {
  mainRows.push([e.id, e.parentId || '', e.content, e.version || 1, e.copyCount || 0, e.modifyCount || 0, new Date(e.createdAt).toISOString(), new Date(e.updatedAt || e.createdAt).toISOString(), e.isDeleted ? 'true' : 'false', e.deletedAt?new Date(e.deletedAt).toISOString():null]);
});
  const historyRows = [['entryId', 'version', 'content', 'timestamp']];
  entries.forEach(e => {
  if (e.history && Array.isArray(e.history)) {
  e.history.forEach(h => {
  historyRows.push([e.id, h.version, h.content, new Date(h.timestamp).toISOString()]);
});
}
});
  const wsMain = XLSX.utils.aoa_to_sheet(mainRows);
  const wsHistory = XLSX.utils.aoa_to_sheet(historyRows);
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, wsMain, this.t('entries'));
  XLSX.utils.book_append_sheet(wb, wsHistory, this.t('historyEntries'));
  return new Uint8Array(XLSX.write(wb, { bookType: 'xlsx', type: 'array' }));
},
},
  watch: {
  viewMode(){ this.saveSettings(); },
  currentTheme(){ this.setTheme(); },
  currentLang(){ this.setLang(); },
  showRecycleBin(){ this.refreshData(); },
},
  // 初始化：先启动数据库，再加载数据
  mounted() {
  entryDB.init().then(async () => {
  this.loadSettings();
  await this.loadData();
  this.refreshData();
}).catch(err => {
  console.error('数据库初始化失败', err);
  this.showToast('数据库初始化失败');
});
},
});

  // 子组件（完全不变）
  app.component('entry-row-renderer', {
  props: { entry: Object, depth: { type:Number, default:0 }, isRecycle: Boolean, forceShow: Boolean, breadcrumbMode: { type:Boolean, default: false } },
  emits: ['update'],
  template: `
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
          <button class="btn sm icon-only" @click.stop="copyText" title="复制文本">📋</button>
          <button class="btn sm icon-only" @click.stop="addChild" title="新增子词条" v-if="!entry.isDeleted && !isRecycle">➕</button>
          <button class="btn sm icon-only" @click.stop="editEntry" title="编辑" v-if="!entry.isDeleted && !isRecycle">✏️</button>
          <button class="btn sm icon-only" @click.stop="showHistory" title="历史">📜</button>
          <button class="btn sm danger icon-only" @click.stop="deleteEntry" title="删除" v-if="!entry.isDeleted && !isRecycle">🗑️</button>
          <button class="btn sm icon-only" @click.stop="restoreEntry" title="恢复" v-if="isRecycle && isTopDeleted">♻️</button>
        </span>
      </div>
      <template v-if="!breadcrumbMode && viewMode==='tree' && isExpanded">
        <entry-row-renderer v-for="child in visibleChildren" :key="child.id" :entry="child" :depth="depth+1" :is-recycle="isRecycle" :force-show="isRecycle ? true : !child.isDeleted" :breadcrumb-mode="false" @update="$emit('update')"></entry-row-renderer>
      </template>
    </template>
  `,
  computed: {
  viewMode() { return this.$root?.viewMode || 'tree'; },
  expandedIds() { return this.$root?.expandedIds || new Set(); },
  isExpanded() { return this.expandedIds.has(this.entry.id); },
  hasAnyChildren() { return this.$root?.hasAnyChildren(this.entry.id); },
  visibleChildren() {
  const all = this.$root?.getAllChildren(this.entry.id) || [];
  const filtered = this.isRecycle ? all : all.filter(c => !c.isDeleted);
  return filtered.sort((a,b) => (this.$root?.sortScore(b)||0) - (this.$root?.sortScore(a)||0));
},
  isTopDeleted() { return this.$root?.isTopDeleted(this.entry); },
},
  methods: {
  toggleExpand() { if (!this.hasAnyChildren && !this.isRecycle) return; const set = this.$root?.expandedIds; if(set){ if(set.has(this.entry.id)) set.delete(this.entry.id); else set.add(this.entry.id); this.$root?.refreshData(); } },
  onClickContent() { if(this.breadcrumbMode) { this.$root?.drillDownList(this.entry.id); } else if(this.viewMode==='tree') { this.toggleExpand(); } },
  copyText() { this.$root?.copyEntryText(this.entry.id); },
  addChild() { this.$root?.openAddModal(this.entry.id); },
  editEntry() { this.$root?.openEditModal(this.entry.id); },
  showHistory() { this.$root?.showHistory(this.entry.id); },
  deleteEntry() { this.$root?.deleteEntry(this.entry.id); },
  restoreEntry() { this.$root?.restoreEntry(this.entry.id); },
},
});

  app.mount('#app');
