if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import math


PER_PAGE = 200

@transformer
def generate_pages(meta_data, *args, **kwargs):
    """
    Receives meta info with total breweries
    Returns list of pages to extract
    """

    total = meta_data["total"]

    total_pages = math.ceil(total / PER_PAGE)

    pages = []

    for p in range(1, total_pages + 1):
        pages.append({"page":p})

    return [pages]

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'


@test
def test_lenght(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert len(output) != 0, 'The output is Empty'