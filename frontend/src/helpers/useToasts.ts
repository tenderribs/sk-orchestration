import { ref } from 'vue'

type Toast = {
    id?: string;
    text: string;
    classes: string;
    icon?: string;
}

const toasts = ref<Toast[]>([])
export const toastDuration = 2 * 1000

export const useToast = () => {
    const create = (toast: Toast) => {
        toast.id = (Math.random() * 99999).toString()
        toasts.value.push(toast)

        setTimeout(() => {
            toasts.value = toasts.value.filter(x => x.id !== toast.id)
        }, toastDuration)

        return toast.id
    }

    const success = (text?: string) => {
        if (text && text.length > 0) {
            return create({
                text: text ?? 'Saved',
                icon: 'bi bi-check',
                classes: 'bg-lime-600 text-white',
            })
        }
    }

    const error = (text?: string) => {
        if (text && text.length > 0) {
            return create({
                text: text ?? 'Error',
                icon: 'bi bi-exclamation-square',
                classes: 'bg-red-600 text-white',
            })
        }
    }


    return {
        toasts,
        success,
        error,
    }
}
