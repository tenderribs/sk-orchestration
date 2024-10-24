<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { isLoggedIn } from '@/helpers/useIsLoggedIn'
import { onMounted } from 'vue'

const { BASE_URL } = import.meta.env

onMounted(() => console.log(BASE_URL))
</script>

<template>
    <div class="border-b-[1.5px] border-b-gray-200 py-2.5 mb-6">
        <div class="container flex flex-row justify-between items-center">
            <div class="flex flex-row items-center">
                <router-link :to="{ name: 'home' }">
                    <img class="h-10" :src="BASE_URL + 'logo_stzh_ugz_rgb_blau_digital.svg'" />
                </router-link>
                <!-- <router-link class="pl-4 font-md text-xl" :to="{ name: 'home' }"
                    >Sensors</router-link
                > -->
            </div>
            <div v-if="isLoggedIn">
                <router-link class="pr-8" :to="{ name: 'home' }">Dashboard</router-link>
                <router-link class="pr-8" :to="{ name: 'sites' }">Installations</router-link>
                <router-link class="pr-8" :to="{ name: 'sites' }">Sites</router-link>
                <router-link :to="{ name: 'hardware' }">Hardware</router-link>
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
