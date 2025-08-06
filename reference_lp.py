from flytekit import workflow
from flytekit import reference_launch_plan

# Reference the launch plan already registered in Flyte
@reference_launch_plan(
    project="my-project",
    domain="development",
    name="default_lp.hello_workflow",
    version="v1",
)
def hello_lp(name: str) -> str:
    """Reference to default launch plan of hello_workflow"""
    ...

# Workflow that calls the referenced launch plan
@workflow
def call_hello_lp() -> str:
    return hello_lp(name="Referenced User")
