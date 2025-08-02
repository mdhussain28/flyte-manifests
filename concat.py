from flytekit import task

@task
def concat_strings(a: str, b: str) -> str:
    return a + b
