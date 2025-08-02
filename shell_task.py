from flytekit import kwtypes
from flytekit.extras.tasks.shell import OutputLocation, ShellTask

t1 = ShellTask(
    name="task_1",
    debug=True,
    script="""
    set -ex
    echo "Hey there! Let's run some bash scripts using a shell task."
    echo "Showcasing shell tasks." >> {inputs.x}
    if grep "shell" {inputs.x}
    then
        echo "Found it!" >> {inputs.x}
    else
        echo "Not found!"
    fi
    """,
    inputs=kwtypes(x=str),
    output_locs=[OutputLocation(var="i", var_type=FlyteFile, location="{inputs.x}")],
)
