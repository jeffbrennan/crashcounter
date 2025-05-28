from typing import Type

import requests
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.engine.mock import MockConnection
from sqlalchemy.orm import sessionmaker
from typer import Typer

from crashcounter.models import Base, Crash, Person, Vehicle, VehicleOrm

app = Typer()


@app.command("get")
def get_data(
    model: Type[BaseModel], offset: int
) -> list[Person] | list[Crash] | list[Vehicle]:
    endpoint = model.model_json_schema().get("endpoint")
    assert endpoint is not None, "Endpoint not found in model schema"
    params = {
        "$limit": 1000,
        "$offset": offset,
    }

    response = requests.get(endpoint, params=params)
    if response.status_code != 200:
        raise Exception(
            f"Error fetching data: {response.status_code} - {response.text}"
        )

    data = response.json()
    result = [model(**item) for item in data]
    return result  # pyright: ignore


def get_engine() -> MockConnection:
    url = URL.create(
        drivername="postgresql",
        username="postgres",
        host="/tmp",
        database="crashcounter",
    )

    engine = create_engine(url)
    return engine


def load_data(data: list[Person] | list[Crash] | list[Vehicle], target: Type[Base]):  # type: ignore
    engine = get_engine()
    Base.metadata.create_all(engine)  # type: ignore
    with sessionmaker(bind=engine)() as session:
        for item in data:
            converted = target(**item.model_dump())
            session.add(converted)

        session.commit()
        print(f"Loaded {len(data)} records into {target.__tablename__}.")


@app.command("load")
def main() -> None:
    # result = get_data(Person, 0)
    # load_data(result, PersonOrm)

    # result = get_data(Crash, 0)
    # load_data(result, CrashOrm)

    result = get_data(Vehicle, 0)
    load_data(result, VehicleOrm)


if __name__ == "__main__":
    main()
