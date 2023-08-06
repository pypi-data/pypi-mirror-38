"""Test for TaskCreator class."""
from os import path
from pydoit_project_builder import TaskCreator


def test_venv_path():
    assert TaskCreator.venv_dir == ".env"


def test_bin_dir_path():
    assert path.basename(TaskCreator.bin_dir) == "bin"


def test_pip_path():
    assert path.basename(TaskCreator.get_pip()) == "pip"
    assert path.dirname(TaskCreator.get_pip()) == TaskCreator.bin_dir


def test_python_path():
    assert path.basename(TaskCreator.get_python()) == "python"
    assert path.dirname(TaskCreator.get_python()) == TaskCreator.bin_dir


def test_pytest_path():
    assert path.basename(TaskCreator.get_pytest()) == "py.test"
    assert path.dirname(TaskCreator.get_pytest()) == TaskCreator.bin_dir


def test_pylint_path():
    assert path.basename(TaskCreator.get_pylint()) == "pylint"
    assert path.dirname(TaskCreator.get_pylint()) == TaskCreator.bin_dir


def test_flake8_path():
    assert path.basename(TaskCreator.get_flake8()) == "flake8"
    assert path.dirname(TaskCreator.get_flake8()) == TaskCreator.bin_dir


def test_sphinx_path():
    assert path.basename(TaskCreator.get_sphinx()) == "sphinx"
    assert path.dirname(TaskCreator.get_sphinx()) == TaskCreator.bin_dir


def test_project_name():
    project_name = "my-doit-project"
    python_version = "3.6"
    task_creator = TaskCreator(project_name=project_name, python_version=python_version)
    assert task_creator.project_name == "my-doit-project"
    assert task_creator.project_name_sc == "my_doit_project"


def test_task_names():
    project_name = "my-doit-project"
    python_version = "3.6"
    task_creator = TaskCreator(project_name=project_name, python_version=python_version)
    tasks = task_creator.get_all_tasks()
    tasks.sort(key=lambda task: task.__name__)
    assert len(tasks) == 8
    assert tasks[0].__name__ == "create_virtual_environment"
    assert tasks[1].__name__ == "doc"
    assert tasks[2].__name__ == "install"
    assert tasks[3].__name__ == "lint"
    assert tasks[4].__name__ == "make_distribution"
    assert tasks[5].__name__ == "reset"
    assert tasks[6].__name__ == "setup"
    assert tasks[7].__name__ == "test"
