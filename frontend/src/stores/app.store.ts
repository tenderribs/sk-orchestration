import { defineStore } from 'pinia'
import { type User } from '../models/user'


type AppStore = {
    user:  User | undefined
}

export const useAppStore = defineStore('app', {
    state: (): AppStore => {
        return {
            user: undefined,
        }
    },
    actions: {
        async setCurrentUser(user: User) {
            this.user = user
        },
        async unsetCurrentUser() {
            this.user = undefined
        },
    }
})
