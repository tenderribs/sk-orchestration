<script setup lang="ts">
import { useToast } from '../helpers/useToasts'

const { toasts } = useToast()
</script>
<template>
    <div
        class="fixed top-20 left-1/2 -translate-x-1/2 justify-center items-center flex flex-col z-50"
    >
        <TransitionGroup name="list">
            <div v-for="toast in toasts" :key="toast.id">
                <div
                    id="toast-simple"
                    class="flex items-center w-full max-w-xs p-3 space-x-4 rtl:space-x-reverse text-white divide-x rtl:divide-x-reverse divide-gray-200 rounded-lg shadow"
                    :class="toast.classes"
                    role="alert"
                >
                    <i :class="toast.icon" />
                    <div class="ps-4 text-sm font-normal">{{ toast.text }}</div>
                </div>
            </div>
        </TransitionGroup>
    </div>
</template>
<style scoped>
.list-enter-active,
.list-leave-active {
    transition: all 0.5s ease;
}

.list-enter-from {
    opacity: 0;
    transform: translateY(30px);
}

.list-leave-to {
    opacity: 0;
    transform: translateY(-30px);
}
</style>
