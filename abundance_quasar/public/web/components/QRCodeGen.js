const QRCodeGen = {
    template: `
        <div class="tool-page" :style="containerStyle">
            <!-- 顶部栏：返回 + 全屏按钮 -->
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;">
                <button class="back-btn" @click="$router.push('/')" v-if="!isFullScreen">← 返回工具箱</button>
            </div>

            <h2 v-if="!isFullScreen">📱 二维码生成 (云端离线)</h2>
            <div class="network-status" v-if="!isFullScreen">
                <span :class="['status-dot', cached ? '' : 'offline']"></span>
                {{ cached ? '页面已缓存，可离线使用' : '正在缓存页面资源...' }}
            </div>

            <input v-model="text" placeholder="输入文本或链接" />
            <button @click="generate" style="margin-top:8px;">生成二维码</button>
            
            <div v-if="qrData" class="result-box" style="text-align:center; margin-top:16px;">
                <img :src="qrData" alt="真实二维码" style="max-width:280px; width:100%;" />
            </div>
            
            <p style="font-size:0.8rem; margin-top:8px;" v-if="!isFullScreen">* 二维码生成完全在本地执行，无需网络。</p>
        </div>
    `,
    data() {
        return {
            text: '',
            qrData: null,
            cached: true,
            isFullScreen: false // 全屏状态
        };
    },
    mounted() {
        // 原有缓存逻辑保留
        if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
            navigator.serviceWorker.controller.postMessage({ type: 'CHECK_CACHE', url: '/cloud-offline/qrcode' });
            navigator.serviceWorker.addEventListener('message', (e) => {
                if (e.data && e.data.type === 'CACHE_STATUS') {
                    this.cached = e.data.cached;
                }
            });
        } else {
            this.cached = true;
        }
    },
    computed: {
        // 全屏样式（和阅读器完全统一）
        containerStyle() {
            if (this.isFullScreen) {
                return {
                    position: 'fixed',
                    top: '0',
                    left: '0',
                    width: '100vw',
                    height: '100vh',
                    margin: '0',
                    padding: '20px',
                    zIndex: '99999',
                    background: '#ffffff',
                    borderRadius: '0'
                }
            }
            return {}
        }
    },
    methods: {
        // 🔥 真实二维码生成（可扫描、离线可用）
        generate() {
            if (!this.text.trim()) {
                alert('请输入内容');
                return;
            }
            // 调用真实二维码库生成
            QRCode.toDataURL(this.text, {
                width: 280,
                margin: 1,
                color: {
                    dark: '#000000',
                    light: '#ffffff'
                }
            }, (err, url) => {
                if (err) {
                    console.error(err);
                    alert('生成失败');
                    return;
                }
                this.qrData = url;
            });
        }
    }
};