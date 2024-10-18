import axios from 'axios'
import { getXsrfCookie } from './helpers/getCookie'
import { useAppStore } from './stores/app.store'


export type WebserviceRequestMethods = 'get' | 'post' | 'put' | 'delete';
export type WebserviceRequestHeaders = Record<string, string | number | boolean>;

export type WebserviceRequestPost = WebserviceRequestParams | FormData | string;


export type WebserviceRequestParams = {
    [key: string]: string | number | boolean | object
} | object;


export type WebserviceRequest = {
    method: WebserviceRequestMethods,
    path: string,
    params?: WebserviceRequestParams,
    post?: WebserviceRequestPost,
    headers?: WebserviceRequestHeaders,
    passthroughResponse?: boolean,
    isCSRFCall?: boolean,
}

export class Webservice {
    public static methods: {
        [key: string]: WebserviceRequestMethods
    } = {
        GET: 'get',
        POST: 'post',
        PUT: 'put',
        DELETE: 'delete',
    }

    protected static async prepare(options: WebserviceRequest): Promise<string> {
        const { VITE_APP_API_URL } = import.meta.env

        const url = !options.path.includes(VITE_APP_API_URL) ? VITE_APP_API_URL + options.path : options.path

        // Try to set CSRF token
        if(!options.isCSRFCall && getXsrfCookie() === '') {
            try {
                await this.csrf()
            } catch(e) {
                useAppStore().unsetCurrentUser()
            }
        }

        axios.defaults.withCredentials = true
        axios.defaults.withXSRFToken = true
        axios.defaults.xsrfHeaderName = "X-CSRFToken"
        axios.defaults.xsrfCookieName = 'csrftoken'

        axios.defaults.headers.common = {
                'accept': 'application/json',
        }

        return url
    }

    public static csrf() {
        const { VITE_APP_API_URL } = import.meta.env

        return this.request({
            method: this.methods.GET,
            path: VITE_APP_API_URL + '/csrf',
            passthroughResponse: true,
            isCSRFCall: true,
        })
    }

    public static async request<T>(options: WebserviceRequest): Promise<T> {
        const url: string = await this.prepare(options)

        try {
            const response = await axios.request<T>({
                method: options.method,
                url,
                data: options.post ?? null,
                params: options.params ?? {},
                headers: options.headers ?? {},
            })

            if (options.passthroughResponse) return response as T

            JSON.parse(response.request.response) // Throws if not JSON

            // @ts-ignore
            return Promise.resolve<T>( response.data.success ? response.data.data : {})
        } catch (err: any) {
            const _e = err.response.data

            return Promise.reject(_e)
        }
    }
}