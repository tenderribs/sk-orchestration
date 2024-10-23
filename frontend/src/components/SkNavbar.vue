<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { isLoggedIn } from '@/helpers/useIsLoggedIn'
</script>

<template>
    <div class="border-b-[1.5px] border-b-gray-200 py-2.5 mb-6">
        <div class="container flex flex-row justify-between">
            <div>
                <router-link class="font-bold" :to="{ name: 'home' }">UGZ Sensors</router-link>
            </div>
            <div v-if="isLoggedIn">
                <router-link class="pr-8" :to="{ name: 'sites' }">Dashboard</router-link>
                <router-link class="pr-8" :to="{ name: 'sites' }">Sites</router-link>
                <router-link class="pr-8" :to="{ name: 'sites' }">Installations</router-link>
                <router-link :to="{ name: 'sites' }">Loggers</router-link>
            </div>
            <div>
                <router-link v-if="!isLoggedIn" :to="{ name: 'login' }">Login</router-link>
                <router-link :to="{ name: 'logout' }" v-else> Log out</router-link>
            </div>
        </div>
    </div>
</template>

<style scoped>
router-link,
span {
    cursor: pointer;
    user-select: none;
}
</style>
