enum MeasurementType {
    WIND_SPEED_MS = "ws_ms",
    WIND_SPEED_MAX_MS = "ws_max_ms",
    EAST_WIND_SPEED_MS = "e_ws_ms",
    NORTH_WIND_SPEED_MS = "n_ws_ms",
    REL_HUMIDITY_PCT = "rel_h_pct",
    IRRADIATION_WM2 = "irr_wm2",
    WIND_DIRECTION_DEG = "w_dir_deg",
    ATM_PRESSURE_HPA = "atm_p_hpa",
    AIR_TEMPERATURE_C = "air_t_c",
    BATTERY_VOLTAGE_V = "bat_v",
    PRECIPITATION_MM = "precip_mm",
    DEWPOINT_C = "dewpoint_t_c",
    GLOBAL_RADIATION_WM2 = "global_rad_wm2",
}

export type Measurement = {
    meas_type: MeasurementType;
    value: number;
    timestamp: Date;

    created_at: Date;
    updated_at: Date;
}
