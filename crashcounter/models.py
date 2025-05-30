import datetime
import json
from enum import StrEnum

from pydantic import BaseModel, field_validator
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.types import Text

Base = declarative_base()


class Dataset(StrEnum):
    person = "person"
    crash = "crash"
    vehicle = "vehicle"
    all = "all"


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
            "filter_field": "unique_id",
            "primary_key": "unique_id",
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


class CrashOrm(Base):
    __tablename__ = "crash"
    crash_date = Column(DateTime)
    crash_time = Column(String(255))
    borough = Column(String(255))
    zip_code = Column(String(255))
    latitude = Column(String(255))
    longitude = Column(String(255))
    location = Column(String(255))
    on_street_name = Column(String(255))
    cross_street_name = Column(String(255))
    off_street_name = Column(String(255))
    number_of_persons_injured = Column(Integer)
    number_of_persons_killed = Column(Integer)
    number_of_pedestrians_injured = Column(Integer)
    number_of_pedestrians_killed = Column(Integer)
    number_of_cyclist_injured = Column(Integer)
    number_of_cyclist_killed = Column(Integer)
    number_of_motorist_injured = Column(Integer)
    number_of_motorist_killed = Column(Integer)
    contributing_factor_vehicle_1 = Column(String(255))
    contributing_factor_vehicle_2 = Column(String(255))
    contributing_factor_vehicle_3 = Column(String(255))
    contributing_factor_vehicle_4 = Column(String(255))
    contributing_factor_vehicle_5 = Column(String(255))
    collision_id = Column(Integer, primary_key=True)
    vehicle_type_code1 = Column(String(255))
    vehicle_type_code2 = Column(String(255))
    vehicle_type_code_3 = Column(String(255))
    vehicle_type_code_4 = Column(String(255))
    vehicle_type_code_5 = Column(String(255))


class Crash(BaseModel):
    class Config:
        json_schema_extra = {
            "about": "https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Crashes/h9gi-nx95/about_data",
            "endpoint": "https://data.cityofnewyork.us/resource/h9gi-nx95.json",
            "filter_field": "collision_id",
            "primary_key": "collision_id",
        }

    # dict -> json string for postgres insert
    @field_validator("location", mode="before")
    @classmethod
    def parse_location(cls, value: dict | None) -> str:
        return json.dumps(value)

    crash_date: datetime.datetime
    crash_time: str
    borough: str | None = None
    zip_code: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    location: str | None = None
    on_street_name: str | None = None
    cross_street_name: str | None = None
    off_street_name: str | None = None
    number_of_persons_injured: int
    number_of_persons_killed: int
    number_of_pedestrians_injured: int
    number_of_pedestrians_killed: int
    number_of_cyclist_injured: int
    number_of_cyclist_killed: int
    number_of_motorist_injured: int
    number_of_motorist_killed: int
    contributing_factor_vehicle_1: str | None = None
    contributing_factor_vehicle_2: str | None = None
    contributing_factor_vehicle_3: str | None = None
    contributing_factor_vehicle_4: str | None = None
    contributing_factor_vehicle_5: str | None = None
    collision_id: int
    vehicle_type_code1: str | None = None
    vehicle_type_code2: str | None = None
    vehicle_type_code_3: str | None = None
    vehicle_type_code_4: str | None = None
    vehicle_type_code_5: str | None = None


class VehicleOrm(Base):
    __tablename__ = "vehicle"
    unique_id = Column(Integer, primary_key=True)
    collision_id = Column(Integer)
    crash_date = Column(DateTime)
    crash_time = Column(String(255))
    vehicle_id = Column(String(255))
    state_registration = Column(String(255))
    vehicle_type = Column(String(255))
    vehicle_make = Column(String(255))
    vehicle_model = Column(String(255))
    vehicle_year = Column(Integer)
    travel_direction = Column(String(255))
    vehicle_occupants = Column(Integer)
    driver_sex = Column(String(255))
    driver_license_status = Column(String(255))
    driver_license_jurisdiction = Column(String(255))
    pre_crash = Column(String(255))
    point_of_impact = Column(String(255))
    vehicle_damage = Column(String(255))
    vehicle_damage_1 = Column(String(255))
    vehicle_damage_2 = Column(String(255))
    vehicle_damage_3 = Column(String(255))
    public_property_damage = Column(String(255))
    public_property_damage_type = Column(Text)
    contributing_factor_1 = Column(String(255))
    contributing_factor_2 = Column(String(255))


class Vehicle(BaseModel):
    class Config:
        json_schema_extra = {
            "about": "https://data.cityofnewyork.us/Public-Safety/Motor-Vehicle-Collisions-Vehicles/bm4k-52h4/about_data",
            "endpoint": "https://data.cityofnewyork.us/resource/bm4k-52h4.json",
            "filter_field": "unique_id",
            "primary_key": "unique_id",
        }

    unique_id: int
    collision_id: int
    crash_date: datetime.datetime
    crash_time: str
    vehicle_id: str
    state_registration: str | None = None
    vehicle_type: str | None = None
    vehicle_make: str | None = None
    vehicle_model: str | None = None
    vehicle_year: int | None = None
    travel_direction: str | None = None
    vehicle_occupants: int | None = None
    driver_sex: str | None = None
    driver_license_status: str | None = None
    driver_license_jurisdiction: str | None = None
    pre_crash: str | None = None
    point_of_impact: str | None = None
    vehicle_damage: str | None = None
    vehicle_damage_1: str | None = None
    vehicle_damage_2: str | None = None
    vehicle_damage_3: str | None = None
    public_property_damage: str | None = None
    public_property_damage_type: str | None = None
    contributing_factor_1: str | None = None
    contributing_factor_2: str | None = None


refresh_map = {
    Dataset.person: (Person, PersonOrm),
    Dataset.crash: (Crash, CrashOrm),
    Dataset.vehicle: (Vehicle, VehicleOrm),
}
