<script setup lang="ts">
import { onMounted, ref, type Ref } from 'vue'

import { SiteWebservice } from '@/webservices/site.webservice'
import { Provider, type Site } from '@/models/site'
import { useToast } from '@/helpers/useToasts'

import SkModal from '@/components/SkModal.vue'
import SkDropdown from '@/components/SkDropdown.vue'
import ConfirmDeleteModal from './ConfirmDeleteModal.vue'

const props = defineProps<{
    site: Site
}>()
const emit = defineEmits(['close-manage-site'])

const { error, success } = useToast()

const confirmDelete: Ref<boolean> = ref(false)

const localSite: Ref<Site> = ref({} as Site)
const providers: string[] = Object.values<string>(Provider)

const updateSite = async () => {
    try {
        await SiteWebservice.update(localSite.value)
        success('Updated Site')
        emit('close-manage-site')
    } catch (e: any) {
        if (e.code && e.code == 400) error('Check input fields')
        else error(e?.detail)
    }
}

const deleteSite = async () => {
    try {
        await SiteWebservice.delete(localSite.value.id)

        success('Deleted Site')
        emit('close-manage-site')
    } catch (e: any) {
        error(e?.detail)
    }
}

onMounted(() => {
    // deep copy the site props and mutate a local copy
    localSite.value = JSON.parse(JSON.stringify(props.site))

    if (!localSite.value.id) emit('close-manage-site')
})
</script>

<template>
    <div>
        <ConfirmDeleteModal
            v-if="confirmDelete"
            :challenge="'DELETE SITE'"
            @close-confirm-delete="confirmDelete = false"
            @confirm-delete="deleteSite"
            class="z-50"
        />
        <sk-modal v-else @close-modal="emit('close-manage-site')">
            <!-- Title -->
            <template #title>Update Site</template>

            <!-- Content -->
            <template #content>
                <div class="w-full">
                    <div class="flex flex-row mb-3">
                        <input
                            class="px-3 py-1 w-4/5 mr-3"
                            maxlength="64"
                            type="text"
                            v-model="localSite.name"
                            placeholder="Name"
                        />
                        <SkDropdown
                            class="w-1/5"
                            :options="providers"
                            v-model="localSite.provider"
                        />
                    </div>
                    <div class="flex flex-row mb-3">
                        <input
                            class="px-3 py-1 w-1/2 mr-3"
                            type="text"
                            maxlength="7"
                            v-model="localSite.wgs84_lat"
                            placeholder="Latitude"
                        />
                        <input
                            class="px-3 py-1 w-1/2"
                            type="text"
                            maxlength="7"
                            v-model="localSite.wgs84_lon"
                            placeholder="Longitude"
                        />
                    </div>
                    <div class="flex flex-row">
                        <input
                            class="px-3 py-1 w-full mr-3"
                            type="text"
                            maxlength="5"
                            v-model="localSite.masl"
                            placeholder="MASL"
                        />
                        <input
                            class="px-3 py-1 w-full"
                            type="text"
                            maxlength="5"
                            v-model="localSite.magl"
                            placeholder="MAGL (optional)"
                        />
                    </div>
                </div>
            </template>

            <!-- Actions -->
            <template #actions>
                <div class="flex flex-row justify-between">
                    <div>
                        <button
                            class="w-24 mr-5 bg-primary hover:bg-primary/80 text-white"
                            @click="updateSite"
                        >
                            Save
                        </button>

                        <button class="w-24 hover:bg-gray-100" @click="emit('close-manage-site')">
                            Cancel
                        </button>
                    </div>

                    <button
                        class="w-24 bg-red-500 hover:bg-red-500/80 text-white"
                        @click="(confirmDelete = true), console.log('confirm')"
                    >
                        Delete
                    </button>
                </div>
            </template>
        </sk-modal>
    </div>
</template>

<style scoped></style>
