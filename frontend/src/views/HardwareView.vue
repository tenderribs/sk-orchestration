<script setup lang="ts">
import { useToast } from '@/helpers/useToasts'
import { DeviceModelWebservice } from '@/webservices/site.webservice'
import { computed, onMounted, ref, type Ref } from 'vue'
import type { DeviceModel } from '@/models/deviceModel'
import { redirectToLoginIfUnauthenticated } from '@/helpers/redirectToLoginIfUnauthenticated'
import type { Logger } from '@/models/logger'

const { error } = useToast()

const deviceModels: Ref<DeviceModel[]> = ref([])

const selectedModel: Ref<DeviceModel | undefined> = ref(undefined)
const loggerSearchName: Ref<string> = ref('')

const compare = (a: string | number, b: string | number) => {
    if (typeof a == 'string') a = a.toLocaleLowerCase()
    if (typeof b == 'string') b = b.toLocaleLowerCase()

    if (a > b) return 1
    if (a == b) return 0
    return -1
}

const getDeviceModels = async () => {
    try {
        deviceModels.value = await DeviceModelWebservice.get()

        if (deviceModels.value.length) selectedModel.value = deviceModels.value[0]
    } catch (e: any) {
        error(e?.detail)
    }
}

const loggers = computed(() => {
    if (!selectedModel.value) return []

    return (
        [...selectedModel.value.loggers]
            // filter by search term
            .filter((logger: Logger) => {
                if (!loggerSearchName.value) return true
                return (
                    logger.sensor_id.toLowerCase().includes(loggerSearchName.value.toLowerCase()) ||
                    logger.sensor_serial
                        .toLowerCase()
                        .includes(loggerSearchName.value.toLowerCase())
                )
            })
            // sort alphabetically
            .sort((a: Logger, b: Logger) => {
                return compare(a.sensor_id, b.sensor_id)
            })
    )
})

const deviceModelsComputed = computed(() => {
    return [...deviceModels.value].sort((a: DeviceModel, b: DeviceModel) => {
        return compare(b.loggers.length, a.loggers.length)
    })
})

onMounted(() => {
    redirectToLoginIfUnauthenticated()

    getDeviceModels()
})
</script>

<template>
    <div>
        <div class="font-bold text-2xl mb-5">Hardware</div>

        <!-- Device Models List -->
        <div class="flex flex-row">
            <div class="w-1/6">
                <div class="pb-4 text-lg font-semibold">Device Models</div>

                <div class="overflow-y-auto overflow-x-auto max-h-[80vh] text-[14px]">
                    <div
                        v-for="deviceModel in deviceModelsComputed"
                        @click="selectedModel = deviceModel"
                        :key="deviceModel.name"
                        class="p-2 mb-4 pr-3 hover:pr-2 hover:bg-gray-100 border-solid border-[1px] border-gray-600 rounded-sm"
                        :class="{ 'bg-black/5': selectedModel === deviceModel }"
                    >
                        <div class="flex flex-row items-center justify-between">
                            <div>
                                <p>
                                    {{ deviceModel.name }}
                                </p>
                                <a
                                    v-show="deviceModel.datasheet"
                                    :href="deviceModel.datasheet"
                                    target="_blank"
                                >
                                    <i class="bi bi-file-earmark-pdf" />
                                    Datasheet
                                </a>
                            </div>
                            <i class="bi bi-chevron-double-right" />
                        </div>
                    </div>
                </div>
            </div>

            <!-- Loggers List -->
            <div class="ml-8 w-[50%]" v-if="selectedModel">
                <div class="pb-4 text-lg font-semibold">{{ selectedModel.name }} Loggers</div>

                <div class="flex flex-row items-center w-full pb-4">
                    <i class="bi bi-search mr-3 text-gray-500 select-none"></i>
                    <input class="p-1 px-2 w-full" type="text" v-model="loggerSearchName" />
                    <i
                        v-if="loggerSearchName.length"
                        @click="loggerSearchName = ''"
                        class="bi bi-x-square text-red-500 select-none cursor-pointer"
                    ></i>
                </div>

                <div class="rounded-sm overflow-y-auto overflow-x-auto max-h-[75vh] text-[14px]">
                    <table class="table-auto w-full text-center">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>ID</th>
                                <th>Serial NR</th>
                                <th>Device Model</th>
                                <th>Measurements</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="(logger, index) in loggers" v-bind:key="logger.sensor_id">
                                <td>{{ index + 1 }}</td>
                                <td>{{ logger.sensor_id }}</td>
                                <td>{{ logger.sensor_serial }}</td>
                                <td>{{ selectedModel.name }}</td>
                                <td>{{ Math.floor(Math.random() * 10000) }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Device Model Details -->
            <div class="ml-8 w-[50%]" v-if="selectedModel">
                <div class="pb-4 text-lg font-semibold">
                    {{ selectedModel.name }} Device Configuration
                </div>
                <div>
                    {{ selectedModel.datasheet }}
                </div>
                <form class="w-full max-w-sm">
                    <div class="mb-6">
                        <label class="block font-bold mb-1" for="device-name"> Model Name </label>
                        <input class="w-full py-2 px-2" id="device-name" type="text" />
                    </div>
                    <div class="">
                        <label class="block font-bold mb-1" for="device-datasheet">
                            Datasheet
                        </label>

                        <input class="w-full py-2 px-2" id="device-datasheet" type="password" />
                    </div>
                    <div class="md:w-2/3">
                        <button
                            class="bg-primary hover:bg-primary/80 text-white py-2 px-4 rounded-md"
                            type="button"
                        >
                            Update
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
