import datetime
import os
import time
from functools import wraps

from dotenv import load_dotenv
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.engine.mock import MockConnection
from typing_extensions import Type


def get_current_time() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def timeit(func):
    # https://dev.to/kcdchennai/python-decorator-to-measure-execution-time-54hk
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(
            f"{get_current_time()} -- Function {func.__name__} Took {total_time * 1000:.2f} ms"
        )
        return result

    return timeit_wrapper


def get_secret(key: str) -> str:
    load_dotenv()
    secret = os.getenv(key)
    if secret is None:
        raise ValueError(f"Secret {key} not found in environment variables.")

    return secret


def get_model_metadata(model: Type[BaseModel], key: str) -> str:
    result = model.model_json_schema().get(key)

    if not isinstance(result, str):
        raise ValueError("key not found in model schema")

    return result


def get_engine() -> MockConnection:
    url = URL.create(
        drivername="postgresql+psycopg2",
        username=get_secret("CRASHCOUNTER_DB_USER"),
        password=get_secret("CRASHCOUNTER_DB_PASSWORD"),
        host="crashcounter-db",
        port=5432,
        database=get_secret("CRASHCOUNTER_DB_NAME"),
    )
    engine = create_engine(url)
    return engine
