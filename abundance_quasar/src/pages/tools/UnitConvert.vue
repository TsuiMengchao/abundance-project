<template>
  <q-page class="row q-pa-md">
    <q-card class="col-12 q-pa-lg">
      <q-btn label="← 返回工具箱" icon="arrow_back" class="mb-4" @click="$router.push('/')" />
      <h2 class="text-center mb-5">📏 单位换算</h2>

      <q-select
        v-model="category"
        label="换算类别"
        :options="categoryOptions"
        class="mb-4"
        filled
      />

      <div class="flex gap-2 items-center mb-4">
        <q-input
          v-model.number="value"
          type="number"
          placeholder="数值"
          class="flex-1"
          label="数值"
          filled
        />

        <q-select
          v-model="fromUnit"
          :options="units.map(u => ({ label: u, value: u }))"
          style="width:100px"
          filled
        />

        <span class="text-lg">→</span>

        <q-select
          v-model="toUnit"
          :options="units.map(u => ({ label: u, value: u }))"
          style="width:100px"
          filled
        />
      </div>

      <q-btn
        label="转换"
        icon="swap_horiz"
        color="primary"
        class="mb-4"
        @click="convert"
      />

      <q-card v-if="result !== null" class="q-pa-4 bg-grey-100">
        {{ result }}
      </q-card>
    </q-card>
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

// 换算类别选项
const categoryOptions = [
  { label: '长度', value: 'length' },
  { label: '重量', value: 'weight' },
  { label: '温度', value: 'temperature' }
];

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
