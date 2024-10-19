<script setup lang="ts">
const emit = defineEmits(['close-modal'])

const close = () => {
    emit('close-modal')
}
</script>

<template>
    <div class="fixed w-full left-0 top-0 h-full bg-black/70 z-30">
        <div
            class="relative inset-x-1/2 -translate-x-1/2 inset-y-1/2 -translate-y-1/2 rounded w-[90vw] sm:w-2/3 lg:w-1/3 bg-white p-6 flex flex-col justify-between"
        >
            <div class="mb-4 text-3xl font-bold">New Site</div>
            <i
                class="absolute right-5 top-5 bi bi-x text-2xl hover:text-gray-700 select-none cursor-pointer"
                @click="close"
            ></i>
            <div>
                <slot name="content"></slot>
            </div>
            <div class="mt-6">
                <slot name="actions"></slot>
            </div>
        </div>
    </div>
</template>

<style lang="css" scoped></style>
