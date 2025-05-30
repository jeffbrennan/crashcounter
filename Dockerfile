FROM apache/airflow:3.0.1

USER root
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY .env /opt/airflow/.env
COPY pyproject.toml uv.lock README.md /opt/airflow/


RUN mkdir -p /var/lib/apt/lists/partial && \
    apt-get update && \
    apt-get -y install libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH="/opt/airflow:/opt/airflow/crashcounter"

COPY crashcounter /opt/airflow/crashcounter
# RUN chown -R ${AIRFLOW_UID:-50000}:0 /opt/airflow/crashcounter

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-editable

USER ${AIRFLOW_UID:-50000}
