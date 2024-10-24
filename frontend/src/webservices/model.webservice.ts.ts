import { Webservice, type WebserviceRequestPost } from '../Webservice';

export function ModelWebservice<T>() {
    abstract class ModelWebservice {
        public static path = '/';

        public static async get(): Promise<T[]> {
            return Webservice.request<T[]>({
                method: Webservice.methods.GET,
                path: this.path,
            });
        }

        public static async add(model: T): Promise<T> {
            return Webservice.request<T>({
                method: Webservice.methods.POST,
                path: this.path,
                post: model as WebserviceRequestPost,
            });
        }

        public static async update(model: T & { id: number }): Promise<T> {
            return Webservice.request<T>({
                method: Webservice.methods.PUT,
                path: `${this.path}/${model.id}`,
                post: model,
            });
        }

        public static async delete(id: number): Promise<void> {
            return Webservice.request<void>({
                method: Webservice.methods.DELETE,
                path: `${this.path}/${id}`,
            });
        }
    }
    return ModelWebservice;
}
