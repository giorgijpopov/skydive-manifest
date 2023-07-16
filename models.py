from sqlalchemy import Column, Integer, Date, Time, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Flight(Base):
    __tablename__ = 'flights'

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    time = Column(Time)
    flight_number = Column(String)
    aircraft_model = Column(String)
    parachutists = Column(String)

    def __repr__(self):
        return f"<Flight(id={self.id}, date={self.date}, time={self.time}, flight_number={self.flight_number}, " \
               f"aircraft_model={self.aircraft_model}, parachutists={self.parachutists})>"
