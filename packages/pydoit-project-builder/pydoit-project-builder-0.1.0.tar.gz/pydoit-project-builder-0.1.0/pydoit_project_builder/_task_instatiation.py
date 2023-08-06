"""Utility to be called to create pydoit tasks."""
from pydoit_project_builder._task_creator import TaskCreator


def instantiate_tasks(project_name, python_version):
    """Instantiate tasks to be used by pydoit.

    TODO(lschneider): This function currently do not achieve
    the desired result. It should be the only function called
    inside the dodo.py file.
    """
    task_creator = TaskCreator(
        project_name=project_name, python_version=python_version)
    list_callbacks = task_creator.get_all_tasks()

    for callback in list_callbacks:
        fn_name = callback.__name__
        globals()["task_" + fn_name] = callback
