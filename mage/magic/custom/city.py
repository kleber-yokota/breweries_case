if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from pyspark.sql.functions import col, count

@custom
def transform_custom(*args, **kwargs):
    spark = kwargs['spark']
    GOLD_PATH = "s3a://gold/openbrewery/breweries_by_city/"
    SILVER_PATH = "s3a://silver/openbrewery/"

    df_silver = df_silver = (
    spark.read
    .format("delta")
    .load(SILVER_PATH)
)

    df_gold = (
        df_silver
        .groupBy(
            col("country"),
            col("state"),
            col("city"),
            col("brewery_type")
        )
        .agg(
            count("*").alias("brewery_count")
        )
    )
    df_gold.write.format("delta").mode("overwrite").save(GOLD_PATH)
    spark.stop()


