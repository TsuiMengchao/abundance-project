const WoodenFish = {
    template: `
    <div class="tool-page">
      <button class="back-btn" @click="$router.push('/')">← 返回工具箱</button>
      <h2>🪷 电子木鱼</h2>
      
      <div style="text-align:center; margin:20px 0">
        <div style="font-size:24px; font-weight:bold; margin-bottom:20px">
          功德：{{ count }}
        </div>
        
        <div 
          @click="knock"
          style="font-size:100px; cursor:pointer; transition:0.2s; user-select:none"
          :style="{ transform: isKnock ? 'scale(0.9)' : 'scale(1)' }"
        >
          🪔
        </div>
        
        <button @click="reset" style="margin-top:20px; background:#ef4444;">
          重置功德
        </button>
      </div>
    </div>
  `,
    data() {
        return {
            // 从本地缓存读取功德数，没有则默认为 0
            count: parseInt(localStorage.getItem('fish_count')) || 0,
            isKnock: false,
            audio: new Audio('data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmImBze5u+wVRwASe7UAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=')
        };
    },
    methods: {
        knock() {
            this.audio.currentTime = 0;
            this.audio.play().catch(() => {});

            // 功德+1
            this.count++;
            // 写入本地缓存（永久保存）
            localStorage.setItem('fish_count', this.count);

            this.isKnock = true;
            setTimeout(() => {
                this.isKnock = false;
            }, 150);
        },
        reset() {
            // 重置功德
            this.count = 0;
            // 清空本地缓存
            localStorage.setItem('fish_count', 0);
        }
    }
};