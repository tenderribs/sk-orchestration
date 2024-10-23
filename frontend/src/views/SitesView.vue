<script setup lang="ts">
import L from 'leaflet'
import { useToast } from '@/helpers/useToasts'
import { type Site, Provider } from '@/models/site'
import { SiteWebservice } from '@/webservices/site.webservice'
import { computed, onMounted, ref, type Ref, watch } from 'vue'
import NewSiteModal from '@/components/NewSiteModal.vue'

type ProviderSelection = {
    provider: Provider
    selected: boolean
}

const sites: Ref<Site[]> = ref([])
const { error } = useToast()

const searchname: Ref<string> = ref('')
const providers: Provider[] = Object.values(Provider)
const newSiteModal: Ref<boolean> = ref(false)

const selectedProviders = ref<ProviderSelection[]>(
    providers.map((provider: Provider) => {
        return { provider, selected: false }
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
    const selection: Provider[] = selectedProviders.value
        .filter((provSel: ProviderSelection) => {
            return provSel.selected
        })
        .map((provSel: ProviderSelection) => provSel.provider)

    if (selection.length == 0) return searchFilter.value

    return searchFilter.value.filter((site: Site) => {
        return selection.includes(site.provider)
    })
})

const filteredSites = computed(() => {
    return providerFilter.value
})

let map: L.Map
let markersLayer: L.LayerGroup

// Function to initialize the Leaflet map
const initMap = () => {
    map = L.map('map').setView([47.4, 8.5], 12) // Initial center of the map (world view)

    // Add the OSM tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
    }).addTo(map)

    // Initialize an empty layer for markers
    markersLayer = L.layerGroup().addTo(map)
}

// Function to update markers on the map
const updateMarkers = () => {
    // Clear the existing markers
    markersLayer.clearLayers()

    if (filteredSites.value.length === 0) return

    // Create a bounds object to track the geographical bounds of the markers
    let points: L.LatLngBoundsLiteral = []

    // Add markers for each site
    filteredSites.value.forEach((site: Site) => {
        const marker = L.marker([site.wgs84_lat, site.wgs84_lon]).bindPopup(
            `<b>${site.name}</b><br>${site.provider}`
        )
        markersLayer.addLayer(marker)

        points.push([site.wgs84_lat, site.wgs84_lon])
    })

    // Fit the map view to the markers bounds, keeping the current zoom level
    map.fitBounds(new L.LatLngBounds(points))
}

// Watch for changes in filteredSites and update markers accordingly
watch(filteredSites, () => {
    updateMarkers()
})

onMounted(() => {
    getSites()
    initMap()
})
</script>

<template>
    <div>
        <new-site-modal v-if="newSiteModal" @close-new-site="newSiteModal = false" />
        <div class="font-bold text-2xl mb-5">Sites</div>

        <div class="flex lg:flex-row lg:items-start text-[14px]">
            <div class="w-full lg:w-1/2 hd:w-3/5 lg:pr-2">
                <!-- Filters -->
                <div class="flex flex-row items-center justify-between mb-3">
                    <!-- Search -->
                    <div class="flex flex-row items-center w-1/2">
                        <i class="bi bi-search mr-3 text-gray-500 select-none"></i>
                        <input class="p-1 px-2 mr-3 w-full" type="text" v-model="searchname" />
                        <i
                            v-if="searchname.length"
                            @click="searchname = ''"
                            class="bi bi-x-square text-red-500 select-none cursor-pointer"
                        ></i>
                    </div>

                    <button
                        class="hover:bg-primary/80 hover:text-white"
                        @click="newSiteModal = !newSiteModal"
                    >
                        <i class="bi bi-plus"></i> New
                    </button>

                    <!-- Selectors -->
                    <div class="flex flex-row justify-end">
                        <button
                            class="ml-3"
                            :class="
                                provSelect.selected
                                    ? 'bg-primary text-white hover:bg-primary/80'
                                    : 'hover:bg-slate-50 '
                            "
                            v-for="provSelect in selectedProviders"
                            :key="provSelect.provider"
                            @click="provSelect.selected = !provSelect.selected"
                        >
                            {{ provSelect.provider }}
                        </button>
                    </div>
                </div>

                <!-- List -->
                <div class="overflow-y-auto overflow-x-auto max-h-[80vh]">
                    <table class="table-auto w-full">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Name</th>
                                <th>Provider</th>
                                <!-- <th>Lat</th>
                                <th>Lon</th> -->
                                <th>MASL</th>
                                <th>MAGL</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="(site, index) in filteredSites"
                                @click.prevent="searchname = site.name"
                                class="hover:bg-gray-100 cursor-pointer"
                                v-bind:key="site.id"
                            >
                                <td class="text-center">{{ index + 1 }}</td>
                                <td>
                                    {{
                                        site.name.length > 36
                                            ? site.name.substring(0, 36) + '...'
                                            : site.name
                                    }}
                                </td>
                                <td class="text-center">{{ site.provider }}</td>
                                <!-- <td class="text-center">
                                    {{ Math.round(site.wgs84_lat * 100) / 100 }} N
                                </td>
                                <td class="text-center">
                                    {{ Math.round(site.wgs84_lon * 100) / 100 }} E
                                </td> -->
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
            <div class="hidden lg:block lg:w-1/2 hd:w-3/5 lg:pl-2 z-0">
                <div id="map" style="width: 100%; height: 85vh"></div>
            </div>
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
