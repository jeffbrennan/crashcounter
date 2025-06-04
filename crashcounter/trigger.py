import datetime
from typing import Any

import requests
from pydantic import BaseModel
from typer import Typer

from crashcounter.common import get_secret

app = Typer(pretty_exceptions_enable=False)


class DagRunResponse(BaseModel):
    dag_run_id: str
    dag_id: str
    logical_date: datetime.datetime
    queued_at: datetime.datetime
    start_date: datetime.datetime | None = None
    end_date: datetime.datetime | None = None
    data_interval_start: datetime.datetime | None = None
    data_interval_end: datetime.datetime | None = None
    run_after: datetime.datetime | None = None
    last_scheduling_decision: datetime.datetime | None = None
    run_type: str
    state: str
    triggered_by: str
    conf: dict[str, str] | None = None
    note: str | None = None
    dag_versions: list[dict[str, Any]] | None = None
    bundle_version: str | None = None


def get_jwt() -> str:
    endpoint = "http://localhost:8082/auth/token"
    headers = {
        "Content-Type": "application/json",
    }

    json_data = {
        "username": get_secret("AIRFLOW_API_USER"),
        "password": get_secret("AIRFLOW_API_PASSWORD"),
    }

    response = requests.post(endpoint, headers=headers, json=json_data)
    if response.status_code != 201:
        raise Exception(
            f"Error getting JWT token: {response.status_code} - {response.text}"
        )

    jwt = response.json().get("access_token")
    if not jwt:
        raise Exception("JWT token not found in response")

    return jwt


def start_run(dag_id: str) -> DagRunResponse:
    endpoint = f"http://localhost:8082/api/v2/dags/{dag_id}/dagRuns"
    jwt = get_jwt()
    headers = {"Authorization": f"Bearer {jwt}"}
    body = {
        "logical_date": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }

    response = requests.post(endpoint, headers=headers, json=body)
    if response.status_code != 200:
        raise Exception(
            f"Error starting DAG run: {response.status_code} - {response.text}"
        )

    return DagRunResponse(**response.json())


@app.command("trigger")
def trigger_dag(dag_id: str) -> None:
    try:
        response = start_run(dag_id)
        print(f"DAG run started successfully: {response.dag_run_id}")
        print(f"Details: {response.model_dump_json(indent=2)}")
    except Exception as e:
        print(f"Failed to start DAG run: {e}")


if __name__ == "__main__":
    app()
