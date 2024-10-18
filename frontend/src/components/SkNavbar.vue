<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
    <div class="border-b-[1.5px] border-b-gray-200 py-2.5 mb-2.5">
        <div class="container flex flex-row justify-between">
            <router-link :to="{ name: 'home' }">Home</router-link>
            <router-link :to="{ name: 'login' }">Login</router-link>
        </div>
    </div>
</template>

<style scoped></style>
