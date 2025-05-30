import datetime

from airflow.decorators import dag, task

from crashcounter.refresh import refresh_data, refresh_map


@dag(
    dag_id="refresh_nyc_opendata",
    start_date=datetime.datetime(2025, 5, 29),
    catchup=False,
)
def refresh_nyc_opendata() -> None:
    @task
    def refresh_task(models) -> None:
        refresh_data(*models)

    tasks = []
    for dataset, models in refresh_map.items():
        task_id = f"refresh_{dataset.value}"
        t = refresh_task.override(task_id=task_id)(models)
        tasks.append(t)

    for i in range(len(tasks) - 1):
        tasks[i] >> tasks[i + 1]  # pyright: ignore[reportUnusedExpression]


refresh_nyc_opendata()
