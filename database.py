from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

DATABASE_URI = 'postgresql+psycopg2://postgres:prasanth@localhost/weather_monitoring_db'

engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class WeatherData(Base):
    __tablename__ = 'weather_data'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)      # New column for humidity
    wind_speed = Column(Float)    # New column for wind speed
    condition = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class ForecastData(Base):
    __tablename__ = 'forecast_data'
    id = Column(Integer, primary_key=True)
    city = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    condition = Column(String)
    timestamp = Column(DateTime)
    
Base.metadata.create_all(engine)
