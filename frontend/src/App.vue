<script setup lang="ts">
import { RouterView } from 'vue-router'
import SkNavbar from './components/SkNavbar.vue'
</script>

<template>
  <sk-navbar />
  <div class="container">
    <RouterView />
  </div>
</template>

<style scoped></style>
