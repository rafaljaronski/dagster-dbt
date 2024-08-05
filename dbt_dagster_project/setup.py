from setuptools import find_packages, setup

setup(
    name="dbt_dagster_project",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "dagster-dbt",
        "dbt-bigquery",
    ],
)