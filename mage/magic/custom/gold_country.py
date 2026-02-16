import requests

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test



@custom
def run_silver(*args, **kwargs):
    r = requests.post(
    "http://localhost:6789/api/pipeline_schedules/4/pipeline_runs/f79cc4ca00784948be373674c6899346"
)
    return r.status_code

@test
def test_output(output, *args) -> None:
    assert output  != 200, f"problem to trigger gold country, status code {output}"

