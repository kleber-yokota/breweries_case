from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.s3 import S3
from pandas import DataFrame
from os import path
import json
from datetime import datetime

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_s3(info, **kwargs) -> None:
    """
    Template for exporting data to a S3 bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#s3
    """
    page = info[1]
    data = info[0]
    datetime_now = kwargs["execution_date"]

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    file_type="parquet"
    
    date =  datetime_now.strftime("%Y%m%d")  
    time = datetime_now.strftime("%H%M%S")

    bucket_name = 'bronze'
    object_key = f"/openbrewery/{date}/{time}/data_{page:03d}.parquet"


    S3.with_config(ConfigFileLoader(config_path, config_profile)).export(
        data.to_pandas(use_pyarrow_extension_array=True),
        bucket_name,
        object_key,
    )
