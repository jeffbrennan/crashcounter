import json
from typing import Annotated, Type

import psycopg2
import requests
import sqlalchemy
import typer
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from typer import Typer

from crashcounter.common import get_engine, get_model_metadata, timeit
from crashcounter.models import (
    Base,
    Dataset,
    refresh_map,
)

app = Typer(pretty_exceptions_enable=False)


@timeit
def request_data(
    endpoint: str, offset: int, filter_field: str, direction: str
) -> requests.Response:
    params = {
        "$limit": 1000,
        "$offset": offset,
        "$order": f"{filter_field} {direction}",
    }
    response = requests.get(endpoint, params=params)
    if response.status_code != 200:
        raise Exception(
            f"Error fetching data: {response.status_code} - {response.text}"
        )
    return response


@timeit
def get_data(
    model: Type[BaseModel], offset: int, filter_field: str, direction: str
) -> list[BaseModel]:
    endpoint = get_model_metadata(model, "endpoint")
    response = request_data(endpoint, offset, filter_field, direction)
    if response.status_code != 200:
        raise Exception(
            f"Error fetching data: {response.status_code} - {response.text}"
        )

    result = [model(**item) for item in response.json()]
    return result


@timeit
def load_data(
    data: list[BaseModel],
    target: Type[Base],  # pyright: ignore
    load_type: str,
) -> None:
    engine = get_engine()
    print(
        f"starting {load_type} of n={len(data)} records into {target.__tablename__}..."
    )

    with sessionmaker(bind=engine)() as session:
        for item in data:
            converted = target(**item.model_dump())

            if load_type == "insert":
                session.add(converted)
            elif load_type == "merge":
                session.merge(converted)
            else:
                raise ValueError(f"Unknown load type: {load_type}")

        try:
            session.commit()
        except sqlalchemy.exc.DataError as e:  # type: ignore
            if not isinstance(e.orig, psycopg2.errors.StringDataRightTruncation):
                raise e

            print(
                f"Error committing data to {target.__tablename__}. "
                "Some records may have been truncated due to string length limits."
            )

            col_lengths = {}
            for item in data:
                for field, value in item.model_dump().items():
                    if isinstance(value, str) and len(value) > col_lengths.get(
                        field, 0
                    ):
                        col_lengths[field] = len(value)

            print(json.dumps(col_lengths, indent=4))
            raise e


@timeit
def refresh_data(model: Type[BaseModel], target: Type[Base]):  # pyright: ignore
    engine = get_engine()
    Base.metadata.create_all(engine)  # type: ignore

    # while loop that queries until latest record is in queried batch
    filter_field = get_model_metadata(model, "filter_field")
    primary_key = get_model_metadata(model, "primary_key")

    with sessionmaker(bind=engine)() as session:
        result = (
            session.query(target).order_by(getattr(target, filter_field).desc()).first()  # pyright: ignore
        )
        latest_record = getattr(result, primary_key) if result else None

    max_attempts = 100
    attempts = 0
    while attempts < max_attempts:
        print(f"loading records {attempts * 1000} to {attempts * 1000 + 999}")
        data = get_data(model, attempts * 1000, filter_field, "desc")

        pks = [data.model_dump()[primary_key] for data in data]
        if latest_record is not None and latest_record in pks:
            print("latest record found in current batch, ending loop")
            load_data(data, target, "merge")
            break

        load_data(data, target, "insert")
        attempts += 1


def refresh_all() -> None:
    for model, orm in refresh_map.values():
        refresh_data(model, orm)


@app.command("load")
def main(
    dataset: Annotated[Dataset, typer.Option("--dataset", "-d")] = Dataset.all,
) -> None:
    if dataset == Dataset.all:
        refresh_all()
    else:
        refresh_data(*refresh_map[dataset])


if __name__ == "__main__":
    app()
