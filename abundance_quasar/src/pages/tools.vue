<template>
  <q-layout view="hHh lpR fFf">
    <!-- 顶部导航栏 -->
    <q-header elevated>
      <q-toolbar>
        <q-toolbar-title>万能工具箱</q-toolbar-title>
      </q-toolbar>
    </q-header>

    <!-- 页面容器出口 -->
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
// 无需代码，仅布局容器
</script>
