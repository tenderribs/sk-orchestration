<script setup lang="ts">
import { onMounted } from 'vue'
import { AuthWebservice } from '@/webservices/auth.webservice'
import { useAppStore } from '@/stores/app.store'
import { useRouter } from 'vue-router'

const router = useRouter()

const logout = async () => {
    try {
        await AuthWebservice.logout()
        useAppStore().unsetCurrentUser()
    } catch (e) {
        console.log(e)
    }
    router.push({ name: 'home' })
}

onMounted(() => {
    logout()
})
</script>

<template>
    <div></div>
</template>

<style scoped></style>
