const HomePage = {
    template: `
        <style>
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
        <div>
          <h1 style="font-size:1.8rem; margin-bottom:4px;">🧰 万能工具箱</h1>
          <p style="color:#64748b; margin-bottom:20px;">全端适配 · 离线/联网智能分类</p>

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
                       class="tool-card" @click="$router.push('/tool/' + tool.id)">
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
    `,
    data() {
        return {
            activeTab: '',
            foldMap: {},
            // 云端数据存储
            cloudCategories: [],
            cloudTools: []
        };
    },
    async created() {
        // 初始化默认激活标签
        const isApp = isMobileApp();
        if (isApp) {
            this.activeTab = 'local-offline';
            // 应用端拉取云端接口
            await this.loadCloudData();
        } else {
            this.activeTab = 'offline';
        }
    },
    computed: {
        currentTabs() {
            return isMobileApp() ? tabsApplication : tabsWeb;
        },
        filteredTools() {
            const tabKey = this.activeTab;
            const isApp = isMobileApp();
            let list = [];
            if (isApp) {
                // 应用端区分本地/云端tab
                if (tabKey === 'local-offline' || tabKey === 'local-online') {
                    // 本地工具匹配
                    const localTabMap = {
                        'local-offline': 'offline',
                        'local-online': 'online'
                    };
                    list = tools.filter(t => t.tab === localTabMap[tabKey]);
                } else if (tabKey === 'cloud-offline' || tabKey === 'cloud-online') {
                    // 云端工具匹配
                    const cloudTabMap = {
                        'cloud-offline': 'offline',
                        'cloud-online': 'online'
                    };
                    list = this.cloudTools.filter(t => t.tab === cloudTabMap[tabKey]);
                }
            } else {
                // 网页端只走本地tools
                list = tools.filter(t => t.tab === tabKey);
            }
            return list;
        },
        subCategoryList() {
            const toolList = this.filteredTools;
            const existCatIds = [...new Set(toolList.map(item => item.category).filter(Boolean))];
            let sourceCats = [];
            const isApp = isMobileApp();
            // 云端tab优先用云端分类，否则用本地全局categories
            if (isApp && (this.activeTab === 'cloud-offline' || this.activeTab === 'cloud-online') && this.cloudCategories.length) {
                sourceCats = [...this.cloudCategories];
            } else {
                sourceCats = [...categories];
            }
            // 只保留当前有工具的分类
            sourceCats = sourceCats.filter(c => existCatIds.includes(c.id));
            // rank从小到大排序
            return sourceCats.sort((a, b) => {
                const ra = a.rank ?? 9999;
                const rb = b.rank ?? 9999;
                return ra - rb;
            });
        }
    },
    methods: {
        // 应用端加载云端json数据
        async loadCloudData() {
            try {
                const res = await fetch('/public/tools.json');
                if (!res.ok) throw new Error('接口请求失败');
                const json = await res.json();
                this.cloudCategories = json.categories || [];
                this.cloudTools = (json.tool || []).map(item => ({
                    ...item,
                    component: 'NativeIFrame'
                }));
            } catch (err) {
                console.warn('云端工具配置加载失败', err);
                this.cloudCategories = [];
                this.cloudTools = [];
            }
        },
        getToolCount(tabKey) {
            const isApp = isMobileApp();
            if (isApp) {
                if (tabKey === 'local-offline') return tools.filter(t => t.tab === 'offline').length;
                if (tabKey === 'local-online') return tools.filter(t => t.tab === 'online').length;
                if (tabKey === 'cloud-offline') {
                    return this.cloudTools.filter(t => t.tab === 'offline').length;
                }
                if (tabKey === 'cloud-online') {
                    return this.cloudTools.filter(t => t.tab === 'online').length;
                }
            } else {
                if (tabKey === 'offline') return tools.filter(t => t.tab === 'offline').length;
                if (tabKey === 'online') return tools.filter(t => t.tab === 'online').length;
            }
            return 0;
        },
        toggleFold(cateId) {
            this.foldMap[cateId] = !this.foldMap[cateId];
        },
        resetAllFold() {
            Object.keys(this.foldMap).forEach(k => {
                this.foldMap[k] = false;
            });
        },
        getToolsByCate(cateId) {
            return this.filteredTools.filter(item => item.category === cateId);
        },
        getCateToolNum(cateId) {
            return this.getToolsByCate(cateId).length;
        }
    },
    watch: {
        activeTab(val) {}
    }
};