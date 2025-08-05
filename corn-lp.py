from flytekit import task, workflow, LaunchPlan
from flytekit import CronSchedule

@task
def greet(name: str) -> str:
    return f"Hello, {name}! Triggered every 2 minutes."

@workflow
def greet_workflow(name: str = "Flyte User") -> str:
    return greet(name=name)

# LaunchPlan to trigger every 2 minutes
demo_schedule_lp = LaunchPlan.create(
    name="every_2_minute_lp",
    workflow=greet_workflow,
    schedule=CronSchedule(
        schedule="*/2 * * * *"  # Every 2 minutes
    ),
    default_inputs={"name": "Demo User"}
)
