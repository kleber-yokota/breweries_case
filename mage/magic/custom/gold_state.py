import requests

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def run_silver(*args, **kwargs):
    r = requests.post(
    "http://localhost:6789/api/pipeline_schedules/1/pipeline_runs/812879650d634b63a7840e26714ac7f4"
)
    return r.status_code

@test
def test_output(output, *args) -> None:
    assert output != 200, f"problem to trigger gold state, status code {output}"


