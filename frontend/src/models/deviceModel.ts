import type { Logger } from "./logger";

export type DeviceModel = {
    name: string;
    description: string;
    manufacturer_url: string;
    datasheet: string;
    user_manual: string;
    attachment: string;
    image: string;

    loggers: Logger[];

    created_at: Date;
    updated_at: Date;
}
