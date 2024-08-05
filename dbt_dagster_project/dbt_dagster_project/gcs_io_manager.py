from dagster import IOManager, io_manager, InputContext, OutputContext
import gcsfs
import os

class GCSIOManager(IOManager):
    def __init__(self, bucket_name):
        self.fs = gcsfs.GCSFileSystem()
        self.bucket_name = bucket_name

    def handle_output(self, context: OutputContext, obj):
        # Define the path in GCS
        output_path = f"{self.bucket_name}/{context.step_key}/{context.name}"
        # Save the object to GCS
        with self.fs.open(output_path, 'wb') as f:
            f.write(obj.encode('utf-8'))
        context.log.info(f"Saved output to {output_path}")

    def load_input(self, context: InputContext):
        # Define the path in GCS
        input_path = f"{self.bucket_name}/{context.upstream_output.step_key}/{context.upstream_output.name}"
        # Load the object from GCS
        with self.fs.open(input_path, 'rb') as f:
            return f.read().decode('utf-8')

@io_manager
def gcs_io_manager(init_context):
    return GCSIOManager(bucket_name=init_context.resource_config["bucket_name"])