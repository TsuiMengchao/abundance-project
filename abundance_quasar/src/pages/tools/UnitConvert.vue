<template>
  <q-page class="row q-pa-md">
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
  </q-page>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

type Category = 'length' | 'weight' | 'temperature';

const category = ref<Category>('length');
const value = ref<number>(0);
const fromUnit = ref<string>('米');
const toUnit = ref<string>('千米');
const result = ref<string | null>(null);
const units = ref<string[]>(['米', '千米', '厘米', '毫米', '英里', '英尺']);

// 监听类别变化更新单位列表
watch(category, (val) => {
  if (val === 'length') {
    units.value = ['米', '千米', '厘米', '毫米', '英里', '英尺'];
  } else if (val === 'weight') {
    units.value = ['千克', '克', '毫克', '吨', '磅', '盎司'];
  } else if (val === 'temperature') {
    units.value = ['摄氏度', '华氏度', '开尔文'];
  }
  fromUnit.value = units.value[0];
  toUnit.value = units.value[1];
});

// 单位换算逻辑
const convert = () => {
  const v = value.value;

  if (category.value === 'length') {
    const toMeter: Record<string, number> = {
      '米': 1, '千米': 1000, '厘米': 0.01, '毫米': 0.001, '英里': 1609.34, '英尺': 0.3048
    };
    const meter = v * toMeter[fromUnit.value];
    result.value = `${(meter / toMeter[toUnit.value]).toFixed(4)} ${toUnit.value}`;
  } else if (category.value === 'weight') {
    const toKg: Record<string, number> = {
      '千克': 1, '克': 0.001, '毫克': 1e-6, '吨': 1000, '磅': 0.453592, '盎司': 0.0283495
    };
    const kg = v * toKg[fromUnit.value];
    result.value = `${(kg / toKg[toUnit.value]).toFixed(6)} ${toUnit.value}`;
  } else if (category.value === 'temperature') {
    let celsius = v;
    if (fromUnit.value === '华氏度') celsius = (v - 32) * 5/9;
    else if (fromUnit.value === '开尔文') celsius = v - 273.15;

    let out = 0;
    if (toUnit.value === '摄氏度') out = celsius;
    else if (toUnit.value === '华氏度') out = celsius * 9/5 + 32;
    else out = celsius + 273.15;

    result.value = `${out.toFixed(2)} ${toUnit.value}`;
  }
};
</script>

<style scoped>
/* 工具页面容器 */
.tool-page {
  background: white;
  border-radius: 24px;
  padding: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  margin-top: 12px;
  flex: 1;
}

.back-btn {
  background: none;
  border: none;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  gap: 6px;
  color: #3b82f6;
  cursor: pointer;
  margin-bottom: 18px;
  padding: 6px 12px;
  border-radius: 30px;
  transition: 0.2s;
}

.back-btn:hover {
  background: #eff6ff;
}

input,
select,
textarea {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  font-size: 1rem;
  margin: 8px 0;
  background: #f8fafc;
}

button {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 12px 20px;
  border-radius: 30px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
  font-size: 0.95rem;
}

button:hover {
  background: #2563eb;
}

.result-box {
  background: #f1f5f9;
  padding: 14px;
  border-radius: 14px;
  margin-top: 12px;
  word-break: break-all;
  font-family: monospace;
}
</style>
