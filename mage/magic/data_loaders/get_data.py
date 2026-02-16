import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import polars as pl
from time import sleep

BASE_URL = "https://api.openbrewerydb.org/v1/breweries"
PER_PAGE = 200

schema = {
    "id": pl.Utf8,
    "name": pl.Utf8,
    "brewery_type": pl.Utf8,
    "address_1": pl.Utf8,
    "address_2": pl.Utf8,
    "address_3": pl.Utf8,
    "city": pl.Utf8,
    "state_province": pl.Utf8,
    "postal_code": pl.Utf8,
    "country": pl.Utf8,
    "longitude": pl.Float64,
    "latitude": pl.Float64,
    "phone": pl.Utf8,
    "website_url": pl.Utf8,
    "state": pl.Utf8,
    "street": pl.Utf8
}
total_retries = 10
@data_loader
def load_data(page, *args, **kwargs):
    status_code = None
    retries = 0
    page_api = page["page"]
    
    while retries < total_retries:
        response = requests.get(
            BASE_URL,
            params = {"per_page":200, "page":page_api},
            timeout = 20
        )
        
        if response.status_code != 200:
            retries += 1
            sleep(5)
        else:
            data = pl.DataFrame(response.json(), schema = schema)
            break


    return data, page_api, retries


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

@test
def test_no_rows(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output.shape[0] >0, 'No Data'

@test
def test_no_page(output, page, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert page is not None or page > 0 , 'No Data'

@test
def test_retries(output, page, retries, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert retries <= total_retries , f'Some problem at API, retries: {retries} '