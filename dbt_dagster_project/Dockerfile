FROM python:3.10

# Install dbt
RUN pip install dbt-bigquery
RUN pip install -U uv
# Install Dagster and Dagster-GCP
RUN python -m uv pip install \
    dagster \
    dagster-dbt \
    dagster-postgres \
    dagster-gcp \
    dagster-k8s \
    dagster-celery[flower,redis,kubernetes] \
    dagster-celery-k8s \
    gcsfs

# COPY dbtlearn /opt/dagster/dbt-project
COPY dbt_dagster_project /opt/dagster/dbt_dagster_project
COPY pyproject.toml /opt/dagster/
COPY workspace.yaml /opt/dagster/
COPY dbtsakey.json /opt/dagster/
COPY setup.py /opt/dagster/

ENV DAGSTER_DBT_PARSE_PROJECT_ON_LOAD=1
ENV DAGSTER_HOME=/opt/dagster
ENV GOOGLE_APPLICATION_CREDENTIALS="/opt/dagster/dbtsakey.json"

# Set the working directory for Dagster
WORKDIR /opt/dagster

# EXPOSE 3000

# CMD ["dagster-webserver", "-w", "workspace.yaml", "-h", "0.0.0.0", "-p", "3000"]