from flytekit import *

@task
def say_hello(name: str) -> str:
    return f"Hello, {name}!"

@workflow
def hello_workflow(name: str = "Flyte User") -> str:
    return say_hello(name=name)
