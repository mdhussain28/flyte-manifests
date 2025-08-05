from datetime import timedelta
from flytekit import task, workflow, LaunchPlan
from flytekit import FixedRate

@task
def notify() -> str:
    return "Triggered by fixed-rate schedule"

@workflow
def fixed_rate_workflow() -> str:
    return notify()

# Launch plan with a fixed-rate schedule (every 2 minutes)
fixed_rate_lp = LaunchPlan.create(
    name="every_2_min_lp",
    workflow=fixed_rate_workflow,
    schedule=FixedRate(
        duration=timedelta(minutes=2)
    )
)
