"""
Validate that all the required environment variables have been set to execute this integration. If this fails,
it indicates a bug in the PythonEnvironment machinery. Currently, this doesn't offer the ability for the user to
run custom validations but we could add it here.

eg:

We could look for a method like `module.entrypoint_validate()` and run it. Currently we don't
"""
import inspect

import click

from lhub_integ import action, util
from lhub_integ.env import MappedColumnEnvVar
from lhub_integ.params import ConnectionParam, ActionParam
from lhub_integ.util import (
    exit_with_instantiation_errors,
    print_successful_validation_result,
)


@click.command()
@click.option("--entrypoint", "-e", required=True)
def main(entrypoint):
    try:
        validation_errors = validate_entrypoint(entrypoint)
    except Exception as ex:
        validation_errors = [{"message": f"Unexpected exception: {ex}"}]

    if validation_errors:
        exit_with_instantiation_errors(
            1, validation_errors, message="Integration validation failed."
        )
    else:
        print_successful_validation_result()


def validate_entrypoint(entrypoint):
    module_name = ".".join(entrypoint.split(".")[:-1])
    function_name = entrypoint.split(".")[-1]

    if module_name == "" or function_name == "":
        return [{"message": "Bad entrypoint format. `Expected filename.functionname`"}]

    # Try to import the world and find the entrypoint
    try:
        util.import_workdir()
    except ImportError as ex:
        return [{"message": f"Can't import {module_name}: {ex}"}]

    method = action.all().get(entrypoint)
    if method is None:
        return [
            {
                "message": f"No matching action found. Is your action annotated with @action?"
            }
        ]

    errors = []

    # Read the arguments and environment variables we expect and make sure they've all been defined
    args, _, _ = inspect.getargs(method.__code__)
    for arg in args:
        if not MappedColumnEnvVar(arg).valid():
            errors.append({"message": "Column mapping must be defined", "inputId": arg})

    env_vars = list(ConnectionParam.all()) + list(ActionParam.for_action(entrypoint))
    for var in env_vars:
        if not var.valid():
            errors.append(
                {"message": "Environment variable must be defined", "inputId": var.name}
            )
    return errors


if __name__ == "__main__":
    main()
