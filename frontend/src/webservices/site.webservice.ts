import { ModelWebservice } from './model.webservice.ts'
import type { Site } from '@/models/site'
import type { Logger } from '@/models/logger.js'
import type { Installation } from '@/models/installation.js'
import type { DeviceModel } from '@/models/deviceModel.js'

export class SiteWebservice extends ModelWebservice<Site>() {
    public static path = '/sites'
}

export class LoggerWebservice extends ModelWebservice<Logger>() {
    public static path = '/loggers'
}

export class InstallationWebservice extends ModelWebservice<Installation>() {
    public static path = '/installations'
}

export class DeviceModelWebservice extends ModelWebservice<DeviceModel>() {
    public static path = '/devicemodels'
}
