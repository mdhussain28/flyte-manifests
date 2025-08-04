from flytekit import task, Workflow

@task
def slope(x: list[int], y: list[int]) -> float:
    n = len(x)
    sum_xy = sum([x[i] * y[i] for i in range(n)])
    sum_x_squared = sum([x[i] ** 2 for i in range(n)])
    return (n * sum_xy - sum(x) * sum(y)) / (n * sum_x_squared - sum(x) ** 2)

@task
def intercept(x: list[int], y: list[int], slope: float) -> float:
    mean_x = sum(x) / len(x)
    mean_y = sum(y) / len(y)
    return mean_y - slope * mean_x

# Create an imperative workflow
imperative_wf = Workflow(name="imperative_linear_regression")

# Add workflow inputs
imperative_wf.add_workflow_input("x", list[int])
imperative_wf.add_workflow_input("y", list[int])

# Add task nodes
node_slope = imperative_wf.add_entity(
    slope,
    x=imperative_wf.inputs["x"],
    y=imperative_wf.inputs["y"]
)

node_intercept = imperative_wf.add_entity(
    intercept,
    x=imperative_wf.inputs["x"],
    y=imperative_wf.inputs["y"],
    slope=node_slope.outputs["o0"]
)

imperative_wf.add_workflow_output("regression_intercept", node_intercept.outputs["o0"])
