<script setup lang="ts">
import { onMounted } from 'vue'
import { AuthWebservice } from '@/webservices/auth.webservice'
import { useAppStore } from '@/stores/app.store'
import { useRouter } from 'vue-router'
import { useToast } from '@/helpers/useToasts'

const router = useRouter()
const { success, error } = useToast()

const logout = async () => {
    try {
        await AuthWebservice.logout()
        success('Logged out')
        useAppStore().unsetCurrentUser()
    } catch (e: any) {
        error(e?.detail)
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
