import os
import gcsfs
import shutil
import stat
import pwd
import grp
from pathlib import Path

from dagster_dbt import DbtCliResource

def copy_from_gcs(fs, gcs_path, local_path):
    # Ensure the local directory exists
    if not os.path.exists(local_path):
        os.makedirs(local_path)
    
    # List all files and directories at the current GCS path
    items = fs.ls(gcs_path, detail=True)
    
    for item in items:
        gcs_item_path = item['name']
        local_item_path = os.path.join(local_path, os.path.relpath(gcs_item_path, gcs_path))
        
        if item['type'] == 'directory':
            # Recursively copy directories
            copy_from_gcs(fs, gcs_item_path, local_item_path)
        else:
            # Copy file
            os.makedirs(os.path.dirname(local_item_path), exist_ok=True)
            with fs.open(gcs_item_path, 'rb') as src_file:
                with open(local_item_path, 'wb') as dst_file:
                    shutil.copyfileobj(src_file, dst_file)
            
            # Set permissions if necessary
            os.chmod(local_item_path, 0o644)

def load_dbt_project_from_gcs(bucket_name, dbt_project_path, local_path="/opt/dagster/dbt-project"):
    fs = gcsfs.GCSFileSystem()
    
    # Clean up the local path if it exists
    if os.path.exists(local_path):
        shutil.rmtree(local_path)
    
    # Copy files and directories from GCS to local path
    copy_from_gcs(fs, f"{bucket_name}/{dbt_project_path}", local_path)

    return local_path

#Przy kopiowaniu projektu dbt w Dockerfile
# dbt_project_dir = Path("/opt/dagster/dbt-project").resolve()

bucket_name = "dbt-project"
dbt_project_path = "dbtlearn/"
# print("Print z constants")
# print(bucket_name)
# print(dbt_project_path)
local_dbt_project_dir = load_dbt_project_from_gcs(bucket_name, dbt_project_path)
print(local_dbt_project_dir)
print("Wczytałem projekt")
dbt_project_dir = Path(local_dbt_project_dir).resolve()
print(dbt_project_dir)
print(os.listdir(dbt_project_dir))
dbt = DbtCliResource(project_dir=os.fspath(dbt_project_dir))
print(dbt)

print("Listing files with permissions:")
for root, dirs, files in os.walk(dbt_project_dir):
    for name in files:
        file_path = os.path.join(root, name)
        # Get file permissions
        stat_info = os.stat(file_path)
        permissions = stat.filemode(stat_info.st_mode)
        # Get owner and group
        owner = pwd.getpwuid(stat_info.st_uid).pw_name
        group = grp.getgrgid(stat_info.st_gid).gr_name
        print(f"{file_path}: {permissions} {owner}:{group}")

# If DAGSTER_DBT_PARSE_PROJECT_ON_LOAD is set, a manifest will be created at run time.
# Otherwise, we expect a manifest to be present in the project's target directory.
if os.getenv("DAGSTER_DBT_PARSE_PROJECT_ON_LOAD"):
    dbt_manifest_path = (
        dbt.cli(
            ["--quiet", "parse", "--debug", "--profiles-dir", "profile"],
            target_path=Path("target"),
        )
        .wait()
        .target_path.joinpath("manifest.json")
    )
    print(dbt_manifest_path)
else:
    dbt_manifest_path = dbt_project_dir.joinpath("target", "manifest.json")