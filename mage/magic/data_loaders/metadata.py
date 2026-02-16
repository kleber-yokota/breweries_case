import io
import pandas as pd
import requests
from datetime import datetime
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    META_URL = "https://api.openbrewerydb.org/v1/breweries/meta"
    response = requests.get(META_URL, timeout=10)
    response.raise_for_status()

    meta = response.json()
    status_code = response.status_code

    total = meta["total"]


    return {"total": total, "status_code": status_code}

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

@test
def test_status_code(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """

    assert output["status_code"] == 200, 'status code not equal 200'

@test
def test_total(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """

    assert output["total"] > 0, 'No Data'