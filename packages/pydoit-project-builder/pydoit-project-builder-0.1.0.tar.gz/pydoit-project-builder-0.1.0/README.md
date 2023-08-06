**pydoit-project-builder** is an open source python library that provides command line interface to accelerate python development. The library is build on top of [doit](http://pydoit.org/).

Inside a new project and assuming the presence of a `setup.py` file, pydoit-project-builder provides a series of command lines to manage a python project:

* Create a virtual environment for the project.
* Install dependencies.
* Create documentation.
* Check code style with pylint and flake8.
* Create a distribution and package the project.
* Remove auxialiary files such as the virtual environment, the auxialiary files, ects.
* Launch tests.

## Installation

To install the current release:

```shell
pip install pydoit-project-builder
```

**Dependencies**

In order to be use, the [doit](http://pydoit.org/) tool must be installed.


## First steps

Lets start a new project called `my-py-project` with the following structure:

```
my-py-project
├── docs
│   ├── conf.py
│   ├── index.rst
│   ├── static
│   └── templates
├── my_py_project
│   ├── __init__.py
│   ├── src_file_1.py
│   ├── src_file_2.py
│   └── ...
├── README.md
├── LICENSE
├── setup.cfg
├── setup.py
├── dodo.py
└── test
    ├── __init__.py
    ├── test_src_file_1.py
    └── test_src_file_2.py
```

The `setup.py` should define on which library the project relies upon. The `dodo.py` file is the file used by the automation tool `doit` to generate command line to be used in a terminal. Its content must be:
```python
"""Define tasks to be used by the library pydoit."""
from pydoit_project_builder import TaskCreator

# Define project parameters.
project_name = "pydoit_project_builder"
python_version = "3.6"
# Instantiate tasks for pydoit library.
task_creator = TaskCreator(
    project_name=project_name, python_version=python_version)
list_callbacks = task_creator.get_all_tasks()
for callback in list_callbacks:
    fn_name = callback.__name__
    globals()["task_" + fn_name] = callback
```

In the shell, in the folder containing the `dodo.py` file, enter the command `doit list` to see the list of available tasks.


## License

[Apache License 2.0](LICENSE)