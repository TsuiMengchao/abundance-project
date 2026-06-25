const Base64Convert = {
    template: `
    <div class="tool-page">
      <button class="back-btn" @click="$router.push('/')">← 返回工具箱</button>
      <h2>🔐 Base64 编码转换</h2>
      
      <input 
        v-model="content" 
        placeholder="请输入要转换的文本或 Base64 字符串"
        style="min-height:80px;white-space:pre-wrap;word-break:break-all"
      />
      
      <div style="display:flex;gap:10px;margin:10px 0">
        <button @click="encode" style="flex:1">编码 → Base64</button>
        <button @click="decode" style="flex:1">Base64 → 解码</button>
      </div>
      
      <button @click="copyResult" v-if="result" style="background:#10b981;width:100%">
        复制结果
      </button>
      
      <div v-if="result" class="result-box" style="margin-top:12px;">
        {{ result }}
      </div>
      <div v-if="error" class="result-box" style="color:#ef4444;margin-top:12px;">
        {{ error }}
      </div>
    </div>
  `,
    data() {
        return {
            content: '',
            result: '',
            error: ''
        };
    },
    methods: {
        // 文本 → Base64 编码
        encode() {
            this.error = '';
            if (!this.content) {
                this.error = '请输入内容';
                this.result = '';
                return;
            }
            try {
                this.result = btoa(unescape(encodeURIComponent(this.content)));
            } catch (e) {
                this.error = '编码失败';
                this.result = '';
            }
        },
        // Base64 → 文本 解码
        decode() {
            this.error = '';
            if (!this.content) {
                this.error = '请输入内容';
                this.result = '';
                return;
            }
            try {
                this.result = decodeURIComponent(escape(atob(this.content)));
            } catch (e) {
                this.error = 'Base64 格式无效，解码失败';
                this.result = '';
            }
        },
        // 一键复制结果
        copyResult() {
            if (!this.result) return;
            navigator.clipboard.writeText(this.result).then(() => {
                alert('复制成功！');
            }).catch(() => {
                alert('复制失败，请手动复制');
            });
        }
    }
};