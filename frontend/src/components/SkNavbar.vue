<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { isLoggedIn } from '@/helpers/useIsLoggedIn'
</script>

<template>
    <div class="border-b-[1.5px] border-b-gray-200 py-2.5 mb-2.5">
        <div class="container flex flex-row justify-between">
            <router-link :to="{ name: 'home' }">UGZ Sensors</router-link>
            <router-link v-if="!isLoggedIn" :to="{ name: 'login' }">Login</router-link>
            <router-link class="cursor-pointer select-none" :to="{ name: 'logout' }" v-else
                >Log out</router-link
            >
        </div>
    </div>
</template>

<style scoped></style>
