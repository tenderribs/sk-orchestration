import type { Site } from '@/models/site'
import { Webservice } from '../Webservice'
import { type User } from '../models/user'

export class SiteWebservice extends Webservice {
    public static async get() {
        return this.request<Site[]>({
            method: Webservice.methods.GET,
            path: '/sites',
        })
    }

    public static async add(site: Site) {
        return this.request<Site>({
            method: Webservice.methods.POST,
            path: '/sites',
            post: site
        })
    }

    public static async getCurrentUser() {
        return this.request<User>({
            method: Webservice.methods.GET,
            path: '/me',
        })
    }
}
