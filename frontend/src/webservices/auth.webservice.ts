import { Webservice } from '../Webservice'
import { type User } from '../models/user'

export class AuthWebservice extends Webservice {
    public static async login(email: string, password: string) {
        return this.request<User>({
            method: Webservice.methods.POST,
            path: '/login',
            post: {
                email,
                password
            }
        })
    }

    public static async getCurrentUser() {
        return this.request<User>({
            method: Webservice.methods.GET,
            path: '/me',
        })
    }
}
