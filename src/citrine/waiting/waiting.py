from time import time, sleep
from typing import Callable
from pprint import pprint
from citrine._rest.collection import Collection
from citrine.resources.workflow_executions import (
    WorkflowExecution,
    WorkflowExecutionStatus,
)


def wait_until(condition: Callable[[], bool], timeout: float = 900.0, interval: float = 3.0):
    """Poll at the specified interval until the provided condition is truthy or the
    timeout (in seconds) is reached."""
    start = time()
    while not condition() and time() - start < timeout:
        sleep(interval)
    assert condition(), "Timeout reached, but condition is still False."


def print_validation_status(
    status: str, start_time: float, line_start: str = "", line_end: str = "\r"
):
    print(
        f"{line_start}Status = {status:<25}Elapsed time = {str(int(time() - start_time)).rjust(3)}s",
        end=line_end,
    )


def pretty_execution_status(status: WorkflowExecutionStatus):
    status_text = status.status
    output_text = status_text if status_text != "InProgress" else "In progress"
    return output_text


def print_execution_status(
    status: WorkflowExecutionStatus, start_time: float, line_end: str = "\r"
):
    print(
        f"Status = {pretty_execution_status(status):<25}Elapsed time = {str(int(time() - start_time)).rjust(3)}s",
        end=line_end,
    )


def wait_until_validated(
    collection: Collection,
    module,
    print_status_info: bool = False,
    timeout: float = 1800.0,
    interval: float = 3.0,
):
    start = time()

    def is_validated():
        status = collection.get(module.uid).status
        print_validation_status(status, start)
        return status != "VALIDATING"

    wait_until(is_validated, timeout=timeout, interval=interval)

    if print_status_info:
        print("\nStatus info:")
        status_info = collection.get(module.uid).status_info
        pprint(status_info)


def wait_until_execution_is_finished(execution: WorkflowExecution):
    start = time()

    def execution_is_finished():
        status = execution.status()
        print_execution_status(status, start)
        return not execution.status().in_progress

    wait_until(execution_is_finished)
