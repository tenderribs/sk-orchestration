<script setup lang="ts">
import { ref, type Ref } from 'vue'

const props = defineProps<{
    options: string[]
}>()

defineEmits(['update:value'])

const value: Ref<string> = ref('')
</script>

<template>
    <select
        v-model="value"
        class="origin-top-right px-2 rounded-md bg-white focus:outline-none"
        role="menu"
        aria-orientation="vertical"
        aria-labelledby="menu-button"
        tabindex="-1"
    >
        <option v-for="option in props.options" :key="option" :value="option">
            {{ option }}
        </option>
    </select>
</template>
