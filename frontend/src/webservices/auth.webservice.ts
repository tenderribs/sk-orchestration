import { Webservice } from '../Webservice'
import { type User } from '../models/user'

export class AuthWebservice extends Webservice {
    public static async login(username: string, password: string) {
        return this.request<User>({
            method: Webservice.methods.POST,
            path: '/login',
            post: {
                username,
                password
            }
        })
    }

    public static async logout() {
        return this.request<void>({
            method: Webservice.methods.POST,
            path: '/logout',
        })
    }

    public static async getCurrentUser() {
        return this.request<User>({
            method: Webservice.methods.GET,
            path: '/me',
        })
    }
}
