<script setup lang="ts">
import { ref, type Ref } from 'vue'

import { SiteWebservice } from '@/webservices/site.webservice'
import { useToast } from '@/helpers/useToasts'
import { Organization, type Site } from '@/models/site'

import SkDropdown from '@/components/SkDropdown.vue'
import SkModal from '@/components/SkModal.vue'

const emit = defineEmits(['close-new-site'])
const { error, success } = useToast()

const organizations: string[] = Object.values<string>(Organization)

const newSite: Ref<Site> = ref({} as Site)

const saveNewSite = async () => {
    try {
        await SiteWebservice.add(newSite.value)

        success('Created new Site')
        newSite.value = {} as Site

        emit('close-new-site')
    } catch (e: any) {
        if (e.code && e.code == 400) error('Check input fields')
        else error(e?.detail)
    }
}
</script>

<template>
    <sk-modal @close-modal="emit('close-new-site')">
        <!-- Title -->
        <template #title>New Site</template>

        <!-- Content -->
        <template #content>
            <div class="w-full">
                <div class="flex flex-row mb-3">
                    <input
                        class="px-3 py-1 w-4/5 mr-3"
                        maxlength="64"
                        type="text"
                        v-model="newSite.name"
                        placeholder="Name"
                    />
                    <SkDropdown
                        class="w-1/5"
                        :options="organizations"
                        v-model="newSite.organization"
                    />
                </div>

                <div class="flex flex-row mb-3">
                    <input
                        class="px-3 py-1 w-1/2 mr-3"
                        type="text"
                        maxlength="7"
                        v-model="newSite.wgs84_lat"
                        placeholder="Latitude"
                    />
                    <input
                        class="px-3 py-1 w-1/2"
                        type="text"
                        maxlength="7"
                        v-model="newSite.wgs84_lon"
                        placeholder="Longitude"
                    />
                </div>
                <div class="flex flex-row">
                    <input
                        class="px-3 py-1 w-full mr-3"
                        type="text"
                        maxlength="5"
                        v-model="newSite.masl"
                        placeholder="MASL"
                    />

                    <input
                        class="px-3 py-1 w-full"
                        type="text"
                        maxlength="5"
                        v-model="newSite.magl"
                        placeholder="MAGL (optional)"
                    />
                </div>
            </div>
        </template>

        <!-- Actions -->
        <template #actions>
            <button
                class="w-24 mr-5 bg-primary hover:bg-primary/80 text-white"
                @click="saveNewSite"
            >
                Save
            </button>
            <button class="w-24 hover:bg-gray-100" @click="emit('close-new-site')">Cancel</button>
        </template>
    </sk-modal>
</template>

<style scoped></style>
