from db.models import Site, Logger


def upsert_sites(session, sites: dict):
    # if we don't hear from the logger, assume it is inactive
    session.query(Site).update({Site.active: False})

    for s in sites:
        site = Site(
            id=s["site_id"],
            name=s["name"],
            provider_id="innet",
            WGS84_lat=s["latitude"],
            WGS84_lon=s["longitude"],
            active=s["state"] == "ACTIVE",
        )

        instance: Site = session.query(Site).filter_by(id=s["site_id"], provider_id="innet").first()

        # insert, or update if exists
        if not instance:
            session.add(site)
        else:
            instance = site
        session.commit()


def upsert_loggers(session, loggers: dict) -> None:
    # if we don't hear from the logger, assume it is inactive
    session.query(Logger).update({Logger.active: False})

    for _logger in loggers:
        logger = Logger(
            id=_logger["logger_id"],
            site_id=_logger["site_id"],
            interval_s=_logger["interval_s"],
            active=_logger["state"] == "ACTIVE",
        )

        instance: Logger = session.query(Logger).filter_by(id=logger.id).first()

        # update logger if exists, insert otherwise
        if not instance:
            session.add(logger)
        else:
            instance = logger
        session.commit()
