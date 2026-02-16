import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    META_URL = "https://api.openbrewerydb.org/v1/breweries/meta"
    response = requests.get(META_URL, timeout=10)
    response.raise_for_status()

    meta = response.json()

    total = meta["total"]

    print(f"Total breweries available: {total}")

    return {"total": total}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
