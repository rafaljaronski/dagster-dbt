import os

from dagster import Definitions, OpExecutionContext
from dagster_dbt import DbtCliResource

from dbt_dagster_project.assets import dbtlearn_dbt_assets
from dbt_dagster_project.constants import dbt_project_dir
from dbt_dagster_project.schedules import schedules
# from dbt_dagster_project.gcs_io_manager import gcs_io_manager

defs = Definitions(
    assets=[dbtlearn_dbt_assets],
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir)), 
        # "io_manager": gcs_io_manager.configured({"bucket_name": "dagster-io-manager"})
    },
)

