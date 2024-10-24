export enum Organization {
    UGZ = "UGZ",
    INNET = "INN",
    METEOBLUE = "MET",
    AWEL = "AWE",
}

export type Site = {
    id: number;
    organization: Organization;
    name: string;
    wgs84_lat: number;
    wgs84_lon: number;
    masl: number;
    magl?: number;
}
