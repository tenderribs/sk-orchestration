import type { Site } from '@/models/site'
import { Webservice } from '../Webservice'

export class SiteWebservice extends Webservice {
    private static path = '/sites'

    public static async get() {
        return this.request<Site[]>({
            method: Webservice.methods.GET,
            path: this.path,
        })
    }

    public static async add(site: Site) {
        return this.request<Site>({
            method: Webservice.methods.POST,
            path: this.path,
            post: site
        })
    }

    public static async update(site: Site) {
        return this.request<Site>({
            method: Webservice.methods.PUT,
            path: this.path + '/' + site.id,
            post: site
        })
    }

    public static async delete(site_id: number) {
        return this.request<Site>({
            method: Webservice.methods.DELETE,
            path: this.path + '/' + site_id,
        })
    }
}
