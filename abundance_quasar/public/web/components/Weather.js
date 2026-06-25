const Weather = {
    template: `
        <div class="tool-page">
          <button class="back-btn" @click="$router.push('/')">← 返回工具箱</button>
          <h2>☁️ 天气查询 (云端联网)</h2>
          <input v-model="city" placeholder="输入城市名称 (英文)" />
          <button @click="fetchWeather">查询天气</button>
          <div v-if="weather" class="result-box">{{ weather }}</div>
          <div v-if="error" class="result-box" style="color:#ef4444;">{{ error }}</div>
        </div>
      `,
    data() {
        return { city: 'Beijing', weather: '', error: '' };
    },
    methods: {
        async fetchWeather() {
            this.error = '';
            this.weather = '加载中...';
            try {
                // 使用免费的wttr.in API
                const res = await fetch(`https://wttr.in/${this.city}?format=%C+%t+%w`);
                const text = await res.text();
                this.weather = text;
            } catch (e) {
                this.error = '请求失败，请检查网络';
                this.weather = '';
            }
        }
    }
};
