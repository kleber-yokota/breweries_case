import requests

@custom
def run_silver(pipe_info, *args, **kwargs):
    r = requests.post(
    f"http://localhost:6789/api/pipeline_schedules/{pipe_info[0]}/pipeline_runs/{pipe_info[1]}"
)
    return r.json().get("error",{})
    


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output == {}, f'problem to call pipeline, error: {output}'
