<script setup lang="ts">
import SkModal from '@/components/SkModal.vue'
import { ref } from 'vue'

const emit = defineEmits(['close-confirm-delete', 'confirm-delete'])

const props = defineProps<{
    challenge: string
}>()

const input = ref('')
</script>

<template>
    <sk-modal @close-modal="emit('close-confirm-delete')">
        <!-- Title -->
        <template #title>Sure? </template>

        <!-- Content -->
        <template #content>
            <div class="w-full">
                <p class="mb-3">
                    Deletion will possibly remove linked entries in database. Confirm by retyping
                    the following:
                </p>
                <input
                    class="px-3 py-1 w-full"
                    maxlength="64"
                    type="text"
                    v-model="input"
                    :placeholder="props.challenge"
                />
            </div>
        </template>

        <!-- Actions -->
        <template #actions>
            <button
                :disabled="input !== props.challenge"
                :class="{
                    'bg-red-500 hover:bg-red-500/80 text-white': input === props.challenge
                }"
                class="w-24 mr-3 text-gray-200"
                @click="emit('confirm-delete'), emit('close-confirm-delete')"
            >
                Delete
            </button>

            <button
                class="w-24 hover:bg-gray-100"
                @click="
                    () => {
                        emit('confirm-delete')
                        emit('close-confirm-delete')
                    }
                "
            >
                Cancel
            </button>
        </template>
    </sk-modal>
</template>

<style scoped></style>
