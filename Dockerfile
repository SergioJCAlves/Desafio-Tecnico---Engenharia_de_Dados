FROM apache/airflow:2.9.0
USER root

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        gosu \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt