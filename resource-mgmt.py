from flytekit import task, workflow, Resources
from typing import List

@task(
    requests=Resources(cpu="250m", mem="256Mi"),
    limits=Resources(cpu="500m", mem="512Mi")
)
def validate_data(data: List[float]) -> List[float]:
    if not data:
        raise ValueError("Input list is empty")
    return data

@task
def compute_average(data: List[float]) -> float:
    return sum(data) / len(data)

@workflow
def simple_workflow(numbers: List[float] = [1.5, 2.3, 3.7]) -> float:
    validated_data = validate_data(data=numbers)
    result_default = compute_average(data=validated_data)
    result_large = compute_average(data=validated_data).with_overrides(
        requests=Resources(cpu="750m", mem="1.5Gi"),
        limits=Resources(cpu="1", mem="2Gi")
    )
    return result_large
