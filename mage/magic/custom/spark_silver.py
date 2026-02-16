if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test
from pyspark.sql.window import Window
from pyspark.sql.functions import (
    col,
    concat_ws,
    current_timestamp,
    input_file_name,
    regexp_extract,
    substring,
    to_date,
    to_timestamp,
    trim,
    row_number
)


@custom
def transform_custom(*args, **kwargs):
    """
    args: The output from any upstream parent blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your custom logic here
    spark = kwargs["spark"]
    df = spark.read.parquet("s3a://bronze/openbrewery/*/*/*")

    df_silver = (
        df.withColumn("__file_path", input_file_name())
        .withColumn("__ingestion", current_timestamp())
        .withColumn(
            "__bronze_date_raw",
            regexp_extract(col("__file_path"), r"/openbrewery/(\d{8})/", 1),
        )
        .withColumn("__bronze_date", to_date(col("__bronze_date_raw"), "yyyyMMdd"))
        .withColumn(
            "__bronze_time_raw",
            regexp_extract(col("__file_path"), r"/openbrewery/\d{8}/(\d{6})/", 1),
        )
        .withColumn(
            "__bronze_datetime",
            to_timestamp(
                concat_ws(
                    " ",
                    col("__bronze_date"),
                    concat_ws(
                        ":",
                        substring(col("__bronze_time_raw"), 1, 2),
                        substring(col("__bronze_time_raw"), 3, 2),
                        substring(col("__bronze_time_raw"), 5, 2),
                    ),
                ),
                "yyyy-MM-dd HH:mm:ss",
            ),
        )
        .drop("__bronze_date_raw")
        .drop("__bronze_time_raw")
    )

    window_spec = (
    Window
    .partitionBy("id")
    .orderBy(col("__bronze_datetime").desc())
)

    df_silver_latest = (
        df_silver
        .withColumn("__row_number", row_number().over(window_spec))
        .filter(col("__row_number") == 1)
        .drop("__row_number")
    )

    df_silver = (
        df_silver.withColumn("country", trim(col("country")))
        .withColumn("state", trim(col("state")))
        .withColumn("city", trim(col("city")))
    )

    df_silver.write.mode("overwrite").format("delta").partitionBy(
        "country", "state", "city"
    ).save("s3a://silver/openbrewery/")
    spark.stop()
