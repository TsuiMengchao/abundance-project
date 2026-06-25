<template>
  <q-page class="row q-pa-md">
    <q-card class="col-12 q-pa-lg">
      <q-btn label="← 返回工具箱" icon="arrow_back" class="mb-4" @click="$router.push('/')" />
      <h2 class="text-center mb-5">☁️ 天气查询 (云端联网)</h2>

      <q-input
        v-model="city"
        placeholder="输入城市名称 (英文)"
        class="mb-4"
        label="城市名称"
        filled
      />

      <q-btn
        label="查询天气"
        icon="search"
        color="primary"
        class="mb-4"
        @click="fetchWeather"
      />

      <q-card v-if="weather" class="q-pa-4 bg-grey-100">
        {{ weather }}
      </q-card>

      <q-card v-if="error" class="q-pa-4 bg-red-100 text-red-600">
        {{ error }}
      </q-card>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const city = ref<string>('Beijing');
const weather = ref<string>('');
const error = ref<string>('');

const fetchWeather = async () => {
  error.value = '';
  weather.value = '加载中...';
  try {
    const res = await fetch(`https://wttr.in/${city.value}?format=%C+%t+%w`);
    const text = await res.text();
    weather.value = text;
  } catch (e) {
    error.value = '请求失败，请检查网络';
    weather.value = '';
  }
};
</script>
