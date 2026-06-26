<template>
  <q-layout view="hHh lpR fFf">
    <!-- 页面容器出口 -->
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";

// 获取路由参数
const $route = useRoute();
</script>
