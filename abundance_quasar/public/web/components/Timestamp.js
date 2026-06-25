const Timestamp = {
    template: `
        <div class="tool-page">
          <button class="back-btn" @click="$router.push('/')">← 返回工具箱</button>
          <h2>🕒 时间戳转换</h2>
          <input v-model="timestamp" placeholder="输入Unix时间戳 (秒)" type="number" />
          <button @click="convert">转换</button>
          <div v-if="result" class="result-box">
            <p>本地时间：{{ result.local }}</p>
            <p>UTC时间：{{ result.utc }}</p>
            <p>ISO格式：{{ result.iso }}</p>
          </div>
          <div style="margin-top:16px;">
            <button @click="nowTimestamp">获取当前时间戳</button>
            <span v-if="currentTs" style="margin-left:12px;">当前：{{ currentTs }}</span>
          </div>
        </div>
      `,
    data() {
        return { timestamp: '', result: null, currentTs: null };
    },
    methods: {
        convert() {
            const ts = parseInt(this.timestamp);
            if (isNaN(ts)) return;
            const date = new Date(ts * 1000);
            this.result = {
                local: date.toLocaleString(),
                utc: date.toUTCString(),
                iso: date.toISOString()
            };
        },
        nowTimestamp() {
            this.currentTs = Math.floor(Date.now() / 1000);
            this.timestamp = this.currentTs;
        }
    }
};
