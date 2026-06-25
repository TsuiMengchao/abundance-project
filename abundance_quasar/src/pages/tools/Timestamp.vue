<template>
  <q-page class="row q-pa-md">
    <q-card class="col-12 q-pa-lg">
      <q-btn label="← 返回工具箱" icon="arrow_back" class="mb-4" @click="$router.push('/')" />
      <h2 class="text-center mb-5">🕒 时间戳转换</h2>

      <q-input
        v-model="timestamp"
        placeholder="输入Unix时间戳 (秒)"
        type="number"
        class="mb-4"
        label="Unix时间戳"
        filled
      />

      <q-btn
        label="转换"
        icon="timer"
        color="primary"
        class="mb-4"
        @click="convert"
      />

      <q-card v-if="result" class="q-pa-4 bg-grey-100 mb-4">
        <p class="mb-1">本地时间：{{ result.local }}</p>
        <p class="mb-1">UTC时间：{{ result.utc }}</p>
        <p>ISO格式：{{ result.iso }}</p>
      </q-card>

      <div class="flex items-center gap-4">
        <q-btn
          label="获取当前时间戳"
          icon="access_time"
          color="secondary"
          @click="nowTimestamp"
        />
        <span v-if="currentTs" class="text-body1">当前：{{ currentTs }}</span>
      </div>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface TimeResult {
  local: string;
  utc: string;
  iso: string;
}

const timestamp = ref<string>('');
const result = ref<TimeResult | null>(null);
const currentTs = ref<number | null>(null);

// 转换时间戳
const convert = () => {
  const ts = parseInt(timestamp.value);
  if (isNaN(ts)) return;

  const date = new Date(ts * 1000);
  result.value = {
    local: date.toLocaleString(),
    utc: date.toUTCString(),
    iso: date.toISOString()
  };
};

// 获取当前时间戳
const nowTimestamp = () => {
  currentTs.value = Math.floor(Date.now() / 1000);
  timestamp.value = currentTs.value.toString();
};
</script>
