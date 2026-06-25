const IpLookup = {
    template: `
        <div class="tool-page">
          <button class="back-btn" @click="$router.push('/')">← 返回工具箱</button>
          <h2>🌐 IP 查询</h2>
          <div class="network-status">
            <span :class="['status-dot', online ? '' : 'offline']"></span>
            {{ online ? '网络连接正常' : '离线状态，无法查询' }}
          </div>
          <input v-model="ip" placeholder="输入IP地址 (留空查询本机)" />
          <button @click="queryIP" :disabled="!online">查询</button>
          <div v-if="result" class="result-box">{{ result }}</div>
          <div v-if="error" class="result-box" style="color:#ef4444;">{{ error }}</div>
        </div>
    `,
    data() {
        return { ip: '', result: '', error: '', online: navigator.onLine };
    },
    mounted() {
        window.addEventListener('online', () => this.online = true);
        window.addEventListener('offline', () => this.online = false);
    },
    methods: {
        async queryIP() {
            this.error = '';
            this.result = '查询中...';
            try {
                const res = await fetch(`https://ipapi.co/${this.ip || ''}/json/`);
                const data = await res.json();
                this.result = JSON.stringify(data, null, 2);
            } catch (e) {
                this.error = '请求失败，请检查网络';
                this.result = '';
            }
        }
    }
};