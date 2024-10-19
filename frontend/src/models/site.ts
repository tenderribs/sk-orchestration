export enum Provider {
    UGZ = "UGZ",
    INNET = "INN",
    METEOBLUE = "MET",
    AWEL = "AWE",
}

export type Site = {
    id: number;
    provider: Provider;
    name: string;
    wgs84_lat: number;
    wgs84_lon: number;
    masl: number;
    magl?: number;
}
