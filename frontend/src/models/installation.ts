import type { Technician } from "./technician";

export type Installation = {
    interval_s: number;
    notes: string;
    start: Date;
    end: Date;
    image: string;
    magl?: number;

    technician: Technician;

    created_at: Date;
    updated_at: Date;
}
