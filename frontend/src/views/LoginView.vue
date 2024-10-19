<script setup lang="ts">
import { ref, type Ref } from 'vue'
import { AuthWebservice } from '@/webservices/auth.webservice'
import { useAppStore } from '@/stores/app.store'
import type { User } from '@/models/user'
import { useRouter } from 'vue-router'

const router = useRouter()
const username: Ref<string> = ref('')
const password: Ref<string> = ref('')

const submit = async () => {
    try {
        const user: User = await AuthWebservice.login(username.value, password.value)

        await useAppStore().setCurrentUser(user)
        router.push({ name: 'home' })
    } catch (e) {
        await useAppStore().unsetCurrentUser()
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
                        Username
                    </label>
                </div>
                <div class="md:w-2/3">
                    <input
                        id="inline-full-name"
                        autocomplete="username"
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
                        id="inline-password"
                        autocomplete="current-password"
                        type="password"
                        v-model="password"
                        @keypress.enter="submit"
                    />
                </div>
            </div>
            <div class="md:flex md:items-center">
                <div class="md:w-1/3"></div>
                <div class="md:w-2/3">
                    <button
                        class="bg-primary hover:bg-primary/80 text-white py-2 px-4 rounded-md"
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
