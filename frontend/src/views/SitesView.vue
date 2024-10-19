<script setup lang="ts">
import { useToast } from '@/helpers/useToasts'
import { type Site, Provider } from '@/models/site'
import { SiteWebservice } from '@/webservices/site.webservice'
import { computed, onMounted, ref, type Ref } from 'vue'

type ProviderSelection = {
    provider: Provider
    selected: boolean
}

const sites: Ref<Site[]> = ref([])
const { error } = useToast()

const searchname: Ref<string> = ref('')
const providers: Provider[] = Object.values(Provider)

const selectedProviders = ref<ProviderSelection[]>(
    providers.map((provider: Provider) => {
        return { provider, selected: true }
    })
)

const getSites = async () => {
    try {
        sites.value = await SiteWebservice.get()
    } catch (e: any) {
        error(e?.detail)
    }
}

// first filter
const searchFilter = computed(() => {
    // search for search string within site name or provider name
    if (searchname.value.length) {
        return sites.value.filter((site: Site) => {
            return (
                site.name.toLowerCase().includes(searchname.value.toLowerCase()) ||
                site.provider.toLowerCase().includes(searchname.value.toLowerCase())
            )
        })
    }
    return sites.value
})

const providerFilter = computed(() => {
    // get the selected providers
    const selection: Provider[] = selectedProviders.value
        .filter((provSel: ProviderSelection) => {
            return provSel.selected
        })
        .map((provSel: ProviderSelection) => provSel.provider)

    // and filter the sites by site.provider included in providers from search filter
    return searchFilter.value.filter((site: Site) => {
        return selection.includes(site.provider)
    })
})

const filteredSites = computed(() => {
    return providerFilter.value
})

onMounted(() => {
    getSites()
})
</script>

<template>
    <div>
        <div class="font-bold text-2xl mb-5">Sites</div>

        <div class="flex flex-row items-start text-[14px]">
            <div class="pr-10 w-1/2">
                <!-- Filters -->
                <div class="flex flex-row items-center mb-3">
                    <!-- Search -->
                    <div class="flex flex-row items-center w-1/2">
                        <i class="bi bi-search mr-3 text-gray-500 select-none"></i>
                        <input
                            id="inline-full-name "
                            class="p-1 mr-3 w-full"
                            type="text"
                            v-model="searchname"
                        />
                        <i
                            v-if="searchname.length"
                            @click="searchname = ''"
                            class="bi bi-x-square text-red-500 select-none cursor-pointer"
                        ></i>
                    </div>

                    <!-- Selectors -->
                    <div class="flex flex-row justify-end w-1/2">
                        <div
                            class="cursor-pointer select-none border-gray-200 border-[1px] px-2 py-1 ml-3 rounded"
                            :class="provSelect.selected ? 'bg-slate-200' : ''"
                            v-for="provSelect in selectedProviders"
                            :key="provSelect.provider"
                            @click="provSelect.selected = !provSelect.selected"
                        >
                            {{ provSelect.provider }}
                        </div>
                    </div>
                </div>

                <!-- List -->
                <div class="overflow-y-auto overflow-x-hidden max-h-[80vh]">
                    <table class="table-auto w-full">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Name</th>
                                <th>Provider</th>
                                <th>Lat</th>
                                <th>Lon</th>
                                <th>MASL</th>
                                <th>MAGL</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(site, index) in filteredSites" v-bind:key="site.id">
                                <td class="text-center">{{ index + 1 }}</td>
                                <td>
                                    {{
                                        site.name.length > 36
                                            ? site.name.substring(0, 36) + '...'
                                            : site.name
                                    }}
                                </td>
                                <td class="text-center">{{ site.provider }}</td>
                                <td class="text-center">
                                    {{ Math.round(site.wgs84_lat * 100) / 100 }} N
                                </td>
                                <td class="text-center">
                                    {{ Math.round(site.wgs84_lon * 100) / 100 }} E
                                </td>
                                <td class="text-center">{{ Math.round(site.masl) }} m</td>
                                <td class="text-center">
                                    {{ site.magl ? site.magl + ' m' : 'N/A' }}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Map -->
            <div></div>
        </div>
    </div>
</template>

<style scoped>
th,
td {
    border: 1px solid #ddd;
    padding: 8px;
}
</style>
