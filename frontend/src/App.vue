<script setup lang="ts">
import { RouterView } from 'vue-router'
import SkNavbar from '@/components/SkNavbar.vue'
import SkToasts from '@/components/SkToasts.vue'
</script>

<template>
    <sk-navbar />
    <sk-toasts />
    <div class="container">
        <RouterView />
    </div>
</template>

<style scoped></style>
