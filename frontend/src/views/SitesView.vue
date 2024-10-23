<script setup lang="ts">
import L from 'leaflet'
import { useToast } from '@/helpers/useToasts'
import { type Site, Provider } from '@/models/site'
import { SiteWebservice } from '@/webservices/site.webservice'
import { computed, onMounted, ref, type Ref, watch } from 'vue'
import NewSiteModal from '@/components/NewSiteModal.vue'
import ManageSiteModal from '@/components/ManageSiteModal.vue'

type ProviderSelection = {
    provider: Provider
    selected: boolean
}

const sites: Ref<Site[]> = ref([])
const { error } = useToast()

const searchname: Ref<string> = ref('')
const providers: Provider[] = Object.values(Provider)
const newSiteModal: Ref<boolean> = ref(false)
const manageSiteModal: Ref<boolean> = ref(false)

const selectedProviders = ref<ProviderSelection[]>(
    providers.map((provider: Provider) => {
        return { provider, selected: false }
    })
)

const clickedSite: Ref<Site> = ref({} as Site)

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

const sortKey: Ref<keyof Site> = ref('name')
const sortASC: Ref<boolean> = ref(true)

const setSortParams = (key: keyof Site) => {
    sortKey.value = key
    sortASC.value = !sortASC.value // toggle
}

type CompElement = string | number | undefined

const cleanString = (s: string) =>
    s
        .replace('Ä', 'A')
        .replace('ä', 'a')
        .replace('Ü', 'U')
        .replace('ü', 'u')
        .replace('Ö', 'O')
        .replace('ö', 'o')

const compareSites = (a: CompElement, b: CompElement) => {
    // one key is undefined (occurs on optional fields) -> prefer existing field
    if (a && !b) return 1
    if (!a && b) return -1

    if (typeof a === 'string' && typeof b === 'string') {
        a = cleanString(a)
        b = cleanString(b)
    }

    // both are defined -> actually check
    if (a && b) {
        if (a > b) return 1
        if (a < b) return -1
    }
    return 0
}

const sortedSites = computed(() => {
    return [...providerFilter.value].sort((a: Site, b: Site) => {
        if (sortASC.value) return compareSites(a[sortKey.value], b[sortKey.value])
        else return compareSites(b[sortKey.value], a[sortKey.value])
    })
})

const sortIcon = computed(() => {
    if (sortASC.value) {
        return 'bi bi-arrow-down'
    }
    return 'bi bi-arrow-up'
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

    if (providerFilter.value.length === 0) return

    // Create a bounds object to track the geographical bounds of the markers
    let points: L.LatLngBoundsLiteral = []

    // Add markers for each site
    providerFilter.value.forEach((site: Site) => {
        const marker = L.marker([site.wgs84_lat, site.wgs84_lon]).bindPopup(
            `<b>${site.name}</b><br>${site.provider}`
        )
        markersLayer.addLayer(marker)

        points.push([site.wgs84_lat, site.wgs84_lon])
    })

    // Fit the map view to the markers bounds, keeping the current zoom level
    map.fitBounds(new L.LatLngBounds(points))
}

// Watch for changes in providerFilter and update markers accordingly
watch(providerFilter, () => {
    updateMarkers()
})

onMounted(() => {
    getSites()
    initMap()
})
</script>

<template>
    <div>
        <NewSiteModal v-if="newSiteModal" @close-new-site="(newSiteModal = false), getSites()" />
        <ManageSiteModal
            v-if="manageSiteModal"
            :site="clickedSite"
            @close-manage-site="(manageSiteModal = false), getSites()"
        />

        <div class="font-bold text-2xl mb-5">Sites</div>

        <div class="flex lg:flex-row lg:items-start text-[14px]">
            <div class="w-full lg:w-1/2 hd:w-3/5 lg:pr-2">
                <!-- Filters -->
                <div class="flex flex-row items-center justify-between mb-3">
                    <!-- Search -->
                    <div class="flex flex-row items-center w-2/5">
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
                    <div class="flex flex-row justify-end w-2/5">
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
                                <th
                                    class="cursor-pointer select-none"
                                    @click="setSortParams('name')"
                                >
                                    Name <i :class="sortIcon" v-show="sortKey === 'name'" />
                                </th>
                                <th
                                    class="cursor-pointer select-none"
                                    @click="setSortParams('provider')"
                                >
                                    Provider <i :class="sortIcon" v-show="sortKey === 'provider'" />
                                </th>
                                <th
                                    class="cursor-pointer select-none"
                                    @click="setSortParams('wgs84_lat')"
                                >
                                    Lat <i :class="sortIcon" v-show="sortKey === 'wgs84_lat'" />
                                </th>
                                <th
                                    class="cursor-pointer select-none"
                                    @click="setSortParams('wgs84_lon')"
                                >
                                    Lon <i :class="sortIcon" v-show="sortKey === 'wgs84_lon'" />
                                </th>
                                <th
                                    class="cursor-pointer select-none"
                                    @click="setSortParams('masl')"
                                >
                                    MASL <i :class="sortIcon" v-show="sortKey === 'masl'" />
                                </th>
                                <th
                                    class="cursor-pointer select-none"
                                    @click="setSortParams('magl')"
                                >
                                    MAGL <i :class="sortIcon" v-show="sortKey === 'magl'" />
                                </th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr
                                v-for="(site, index) in sortedSites"
                                @click="searchname = site.name"
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
                                <td
                                    class="text-center hover:text-gray-400"
                                    @click.stop="(clickedSite = site), (manageSiteModal = true)"
                                >
                                    <i class="bi bi-pencil-square text-[12px]"></i>
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
