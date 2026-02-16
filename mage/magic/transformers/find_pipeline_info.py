from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import sqlite3


@data_loader
def load_data_from_postgres(*args, **kwargs):
    DB_PATH = "/home/src/mage_data/magic/mage-ai.db"
    PIPELINE_UUID = "silver_layer"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, token
        FROM pipeline_schedule
        where pipeline_uuid = ?
    """, (PIPELINE_UUID,)
    )

    row = cursor.fetchall()
    conn.close()
    return row


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

@test
def test_output_empty(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output != [], 'Pipeline not found'


@test
def test_output_more_than_one_pipeline(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert len(output) != 1, 'Find more than 1 pipeline'

        