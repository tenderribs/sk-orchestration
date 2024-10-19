<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { isLoggedIn } from '@/helpers/useIsLoggedIn'
</script>

<template>
    <div class="border-b-[1.5px] border-b-gray-200 py-2.5 mb-6">
        <div class="container flex flex-row justify-between">
            <div>
                <router-link class="font-bold" :to="{ name: 'home' }">UGZ Sensors</router-link>
                <router-link class="pl-6" v-if="isLoggedIn" :to="{ name: 'sites' }"
                    >Sites</router-link
                >
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
