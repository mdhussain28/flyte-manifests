from flytekit import ContainerTask, kwtypes

add_task = ContainerTask(
    name="add_numbers",
    image="python:3.9-slim",
    input_data_dir="/var/inputs",
    output_data_dir="/var/outputs",
    inputs=kwtypes(a=int, b=int),
    outputs=kwtypes(sum=int),
    command=[
        "sh", "-c",
        "expr $(cat /var/inputs/a) + $(cat /var/inputs/b) > /var/outputs/sum"
    ],
)
