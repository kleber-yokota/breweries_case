
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from pyspark.sql import Row, SparkSession

from mage_ai.data_preparation.repo_manager import RepoConfig, get_repo_path
from mage_ai.services.spark.config import SparkConfig
from mage_ai.services.spark.spark import get_spark_session
from pyspark.sql import Row, SparkSession


@data_loader
def load_openbrewery_data(*args, **kwargs):

    spark = kwargs["spark"]
    return spark.read.parquet("s3a://bronze/openbrewery/*/*/*.parquet").toPandas()

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    print(output)
    assert output is not None, 'The output is undefined'

