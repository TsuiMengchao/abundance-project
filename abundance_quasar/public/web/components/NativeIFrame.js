// components/NativeIFrame.js
const NativeIFrame = {
    template: `
        <div class="tool-page" :style="containerStyle">
            <!-- 顶部栏：统一样式，全屏隐藏返回按钮 -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;">
                <button class="back-btn" @click="$router.push('/')" v-if="!isFullScreen">← 返回工具箱</button>
                <button class="back-btn" @click="toggleFullScreen">
                    {{ isFullScreen ? '退出全屏' : '全屏' }}
                </button>
                <button class="back-btn" @click="openInNewTab">
                    在新标签页中打开
                </button>
            </div>

            <!-- 非全屏显示标题，全屏隐藏 -->
            <h2 v-if="!isFullScreen" class="tool-title">{{tool.icon}} {{tool.name}}</h2>
            
            <!-- iframe 核心：绑定配置的src路径 -->
            <iframe 
                :src="tool.src" 
                style="width:100%; border:none; border-radius:12px; transition: all 0.2s;"
                :style="iframeStyle">
            </iframe>
        </div>
    `,
    data() {
        return {
            isFullScreen: false
        }
    },
    props: {
        // 接收配置中的src路径（核心！）
        tool: {
            type: Object,
            required: true, // 强制必须传，避免空白iframe
            default: 'about:blank'
        }
    },
    computed: {
        // 全屏容器样式
        containerStyle() {
            return this.isFullScreen ? {
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
            } : {}
        },
        // 自适应iframe高度（核心优化）
        iframeStyle() {
            return this.isFullScreen ? {
                height: 'calc(100vh - 60px)',
                borderRadius: '0'
            } : {
                height: 'calc(100vh - 200px)'
            }
        }
    },
    methods: {
        toggleFullScreen() {
            this.isFullScreen = !this.isFullScreen;
        },
        openInNewTab() {
            const originUrl = window.location.origin;
            const targetUrl = originUrl + '/' + this.tool.src;
            window.open(targetUrl);
        }
    }
};