import { useAppStore } from "@/stores/app.store"
import { storeToRefs } from "pinia"
import { computed } from "vue"

export const isLoggedIn = computed(() => {
    const appStore = useAppStore()
    const { user } = storeToRefs(appStore)

    return user.value && user.value.id && user.value.id > 0
})