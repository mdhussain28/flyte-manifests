from flytekit import task, workflow

@task
def add(a: int, b: int) -> int:
    return a + b

@task
def format_result(total: int) -> str:
    return f"The total is: {total}"

@workflow
def addition_workflow(x: int, y: int) -> str:
    sum_result = add(a=x, b=y)
    final_output = format_result(total=sum_result)
    return final_output
