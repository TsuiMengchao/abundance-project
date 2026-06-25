const Calculator = {
    template: `
        <div class="tool-page">
          <button class="back-btn" @click="$router.push('/')">← 返回工具箱</button>
          <h2>🧮 科学计算器</h2>
          <input v-model="expression" @keyup.enter="calculate" placeholder="输入表达式，如 sin(pi/2)+2^3" />
          <button @click="calculate">计算</button>
          <div v-if="result !== null" class="result-box">{{ result }}</div>
          <div style="margin-top:12px; font-size:0.8rem; color:#64748b;">
            支持: + - * / % ^ sin cos tan sqrt log abs PI E
          </div>
        </div>
      `,
    data() {
        return { expression: '', result: null };
    },
    methods: {
        calculate() {
            try {
                let expr = this.expression
                    .replace(/\^/g, '**')
                    .replace(/sin/g, 'Math.sin')
                    .replace(/cos/g, 'Math.cos')
                    .replace(/tan/g, 'Math.tan')
                    .replace(/sqrt/g, 'Math.sqrt')
                    .replace(/log/g, 'Math.log10')
                    .replace(/ln/g, 'Math.log')
                    .replace(/abs/g, 'Math.abs')
                    .replace(/PI/g, 'Math.PI')
                    .replace(/E/g, 'Math.E');
                this.result = eval(expr);
            } catch (e) {
                this.result = '表达式错误';
            }
        }
    }
};
