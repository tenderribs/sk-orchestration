<script setup lang="ts">
import { ref, type Ref } from 'vue'
import { AuthWebservice } from '@/webservices/auth.webservice'
import { useAppStore } from '@/stores/app.store'
import type { User } from '@/models/user'

const username: Ref<string> = ref('')
const password: Ref<string> = ref('')

const submit = async () => {
    try {
        const user: User = await AuthWebservice.login(username.value, password.value)
        useAppStore().setCurrentUser(user)
    } catch (e) {
        useAppStore().unsetCurrentUser()
    }
}
</script>

<template>
    <div class="flex flex-row justify-center items-center pt-[10vh]">
        <form class="w-full max-w-sm">
            <div class="md:flex md:items-center mb-6">
                <div class="md:w-1/3">
                    <label
                        class="block font-bold md:text-right mb-1 md:mb-0 pr-4"
                        for="inline-full-name"
                    >
                        Full Name
                    </label>
                </div>
                <div class="md:w-2/3">
                    <input
                        class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                        id="inline-full-name"
                        type="text"
                        v-model="username"
                    />
                </div>
            </div>
            <div class="md:flex md:items-center mb-6">
                <div class="md:w-1/3">
                    <label
                        class="block font-bold md:text-right mb-1 md:mb-0 pr-4"
                        for="inline-password"
                    >
                        Password
                    </label>
                </div>
                <div class="md:w-2/3">
                    <input
                        class="bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500"
                        id="inline-password"
                        type="password"
                        placeholder="******************"
                        v-model="password"
                    />
                </div>
            </div>
            <div class="md:flex md:items-center">
                <div class="md:w-1/3"></div>
                <div class="md:w-2/3">
                    <button
                        class="shadow bg-purple-500 hover:bg-purple-400 focus:shadow-outline focus:outline-none text-white font-bold py-2 px-4 rounded"
                        type="button"
                        @click="submit"
                    >
                        Log in
                    </button>
                </div>
            </div>
        </form>
    </div>
</template>

<style scoped></style>
