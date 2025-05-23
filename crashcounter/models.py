import datetime

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class PersonOrm(Base):
    __tablename__ = "person"
    unique_id = Column(Integer, primary_key=True)
    collision_id = Column(Integer)
    crash_date = Column(DateTime)
    crash_time = Column(String(255))
    person_id = Column(String(255))
    person_type = Column(String(255))
    person_injury = Column(String(255))
    vehicle_id = Column(Integer)
    person_age = Column(Integer)
    ejection = Column(String(255))
    emotional_status = Column(String(255))
    bodily_injury = Column(String(255))
    position_in_vehicle = Column(String(255))
    safety_equipment = Column(String(255))
    ped_location = Column(String(255))
    ped_action = Column(String(255))
    complaint = Column(String(255))
    ped_role = Column(String(255))
    contributing_factor_1 = Column(String(255))
    contributing_factor_2 = Column(String(255))
    person_sex = Column(String(255))


class Person(BaseModel):
    class Config:
        json_schema_extra = {
            "about": "https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Person/f55k-p6yu/about_data",
            "endpoint": "https://data.cityofnewyork.us/resource/f55k-p6yu.json",
        }

    unique_id: int
    collision_id: int
    crash_date: datetime.datetime
    crash_time: str
    person_id: str
    person_type: str
    person_injury: str
    vehicle_id: int | None = None
    person_age: int | None = None
    ejection: str | None = None
    emotional_status: str | None = None
    bodily_injury: str | None = None
    position_in_vehicle: str | None = None
    safety_equipment: str | None = None
    ped_location: str | None = None
    ped_action: str | None = None
    complaint: str | None = None
    ped_role: str | None = None
    contributing_factor_1: str | None = None
    contributing_factor_2: str | None = None
    person_sex: str | None = None


class Crash(BaseModel):
    crash_date: datetime.datetime
    crash_time: str
    borough: str
    zip_code: str
    latitude: float
    longitude: float
    location: tuple[float, float]
    on_street_name: str
    cross_street_name: str
    off_street_name: str
    number_of_persons_injured: int
    number_of_persons_killed: int
    number_of_pedestrians_injured: int
    number_of_pedestrians_killed: int
    number_of_cyclist_injured: int
    number_of_cyclist_killed: int
    number_of_motorist_injured: int
    number_of_motorist_killed: int
    contributing_factor_vehicle_1: str
    contributing_factor_vehicle_2: str
    contributing_factor_vehicle_3: str
    contributing_factor_vehicle_4: str
    contributing_factor_vehicle_5: str
    collision_id: int
    vehicle_type_code1: str
    vehicle_type_code2: str
    vehicle_type_code_3: str
    vehicle_type_code_4: str
    vehicle_type_code_5: str


class Vehicle(BaseModel):
    unique_id: int
    collision_id: int
    crash_date: datetime.datetime
    crash_time: str
    vehicle_id: str
    state_registration: str
    vehicle_type: str
    vehicle_make: str
    vehicle_model: str
    vehicle_year: int
    travel_direction: str
    vehicle_occupants: int
    driver_sex: str
    driver_license_status: str
    driver_license_jurisdiction: str
    pre_crash: str
    point_of_impact: str
    vehicle_damage: str
    vehicle_damage_1: str
    vehicle_damage_2: str
    vehicle_damage_3: str
    public_property_damage: str
    public_property_damage_type: str
    contributing_factor_1: str
    contributing_factor_2: str
