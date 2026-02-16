import requests

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test



@custom
def run_silver(*args, **kwargs):
    r = requests.post(
    "http://localhost:6789/api/pipeline_schedules/5/pipeline_runs/fd4f537d274c49dab232c1f850ff3bd5"
)
    return r.status_code

@test
def test_output(output, *args) -> None:
    assert output  != 200, f"problem to trigger gold city, status code {output}"