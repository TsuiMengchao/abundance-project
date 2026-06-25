const UnitConvert = {
    template: `
        <div class="tool-page">
          <button class="back-btn" @click="$router.push('/')">← 返回工具箱</button>
          <h2>📏 单位换算</h2>
          <select v-model="category">
            <option value="length">长度</option>
            <option value="weight">重量</option>
            <option value="temperature">温度</option>
          </select>
          <div style="display:flex; gap:8px; align-items:center;">
            <input v-model.number="value" type="number" placeholder="数值" style="flex:1;" />
            <select v-model="fromUnit" style="width:100px;">
              <option v-for="u in units" :value="u">{{ u }}</option>
            </select>
            <span>→</span>
            <select v-model="toUnit" style="width:100px;">
              <option v-for="u in units" :value="u">{{ u }}</option>
            </select>
          </div>
          <button @click="convert">转换</button>
          <div v-if="result !== null" class="result-box">{{ result }}</div>
        </div>
      `,
    data() {
        return {
            category: 'length',
            value: 0,
            fromUnit: '米',
            toUnit: '千米',
            result: null,
            units: ['米', '千米', '厘米', '毫米', '英里', '英尺']
        };
    },
    watch: {
        category(val) {
            if (val === 'length') this.units = ['米','千米','厘米','毫米','英里','英尺'];
            else if (val === 'weight') this.units = ['千克','克','毫克','吨','磅','盎司'];
            else if (val === 'temperature') this.units = ['摄氏度','华氏度','开尔文'];
            this.fromUnit = this.units[0];
            this.toUnit = this.units[1];
        }
    },
    methods: {
        convert() {
            const v = this.value;
            if (this.category === 'length') {
                const toMeter = { '米':1, '千米':1000, '厘米':0.01, '毫米':0.001, '英里':1609.34, '英尺':0.3048 };
                const meter = v * toMeter[this.fromUnit];
                this.result = meter / toMeter[this.toUnit] + ' ' + this.toUnit;
            } else if (this.category === 'weight') {
                const toKg = { '千克':1, '克':0.001, '毫克':1e-6, '吨':1000, '磅':0.453592, '盎司':0.0283495 };
                const kg = v * toKg[this.fromUnit];
                this.result = kg / toKg[this.toUnit] + ' ' + this.toUnit;
            } else if (this.category === 'temperature') {
                let celsius = v;
                if (this.fromUnit === '华氏度') celsius = (v - 32) * 5/9;
                else if (this.fromUnit === '开尔文') celsius = v - 273.15;
                let out;
                if (this.toUnit === '摄氏度') out = celsius;
                else if (this.toUnit === '华氏度') out = celsius * 9/5 + 32;
                else out = celsius + 273.15;
                this.result = out.toFixed(2) + ' ' + this.toUnit;
            }
        }
    }
};
