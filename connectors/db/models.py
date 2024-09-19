from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Provider(Base):
    __tablename__ = "provider"

    def __init__(self, _id):
        self.id = _id

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)

    sites = relationship("Site", back_populates="provider")

    def __repr__(self) -> str:
        return f"Provider(id={self.id!r}"


class Site(Base):
    __tablename__ = "site"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)
    provider_id = Column(String, ForeignKey("provider.id"))
    WGS84_lat = Column(Float, nullable=False)
    WGS84_lon = Column(Float, nullable=False)
    active = Column(Boolean, default=False, nullable=False)

    provider = relationship("Provider", back_populates="sites")
    loggers = relationship("Logger", back_populates="site")

    def __repr__(self) -> str:
        return f"Site(id={self.id!r}"


class Logger(Base):
    __tablename__ = "logger"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=True)
    active = Column(Boolean, nullable=False, default=False)
    site_id = Column(String, ForeignKey("site.id"))
    interval_s = Column(Integer, nullable=False)

    site = relationship("Site", back_populates="loggers")
    data = relationship("LoggerData", back_populates="logger")

    def __repr__(self) -> str:
        return f"Logger(id={self.id!r}"


class LoggerData(Base):
    __tablename__ = "logger_data"

    id = Column(Integer, primary_key=True, index=True)
    logger_id = Column(String, ForeignKey("logger.id"))
    timestamp = Column(DateTime, nullable=False)

    logger = relationship("Logger", back_populates="data")


# here are the 12 key metrics for stadtklima


class TemperatureLoggerData(LoggerData):
    __tablename__ = "temperature_logger_data"

    id = Column(Integer, ForeignKey("logger_data.id"), primary_key=True)
    temperature = Column(Float, nullable=False)


class PressureLoggerData(LoggerData):
    __tablename__ = "pressure_logger_data"

    id = Column(Integer, ForeignKey("logger_data.id"), primary_key=True)
    pressure = Column(Float, nullable=False)
