export enum Action {
    CAL = "Calibration",
    PER = "Periodic Maintenance",
    FWU = "Firmware Update",
    SRP = "Sensor Replacement",
    BRP = "Battery Replacement",
    DEX = "Data Extraction",
    FRS = "Factory Reset",
    INS = "Inspection",
    ENV = "Environmental Adjustment",
    CLN = "Cleaning",
    MOV = "Moved",
}


export type Logger = {
    sensor_id: string;
    sensor_serial?: string;

    created_at: Date;
    updated_at: Date;
}


export type LoggerAction = {
    action: Action;

    created_at: Date;
    updated_date: Date;
}