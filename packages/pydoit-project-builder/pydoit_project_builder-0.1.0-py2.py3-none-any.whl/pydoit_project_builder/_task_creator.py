"""Define tasks."""
from os import path
from pydoit_project_builder._os_utils import create_dir, \
    remove_directories, remove_files, is_windows


class TaskCreator(object):
    """This class standardize the creation of task used with pydoit.

    In a new project, a `dodo.py` file must be created in the following way:
    ```
    task_creator = TaskCreator(project_name="my_project", python_version="3.6")
    list_callbacks = task_creator.get_all_tasks()
    for callback in list_callbacks:
        fn_name = callback.__name__
        globals()["task_" + fn_name] = callback
    ```

    Once done, in a shell, one can run the following command to see
    all advailable doit tasks:
    ```shell
     doit list
     ```
    """

    venv_dir = ".env"
    bin_dir = path.join(venv_dir, "bin") if not is_windows() else path.join(venv_dir, "Scripts")

    def __init__(self, project_name, python_version):
        """Initializer.

        :param project_name: Name of the project.
        :param python_version: Python version to be used. Must be a string.
        """
        self.project_name = project_name
        self.project_name_sc = project_name.replace("-", "_")
        self.python_version = python_version

    def get_all_tasks(self):
        """Return every tasks that should be launched in shell as a list of callbacks."""
        return [
            self.create_virtual_environment,
            self.doc,
            self.install,
            self.lint,
            self.make_distribution,
            self.reset,
            self.setup,
            self.test,
        ]

    def create_virtual_environment(self):
        """Set a virtual environment for the project."""
        cmd_venv = "python" + self.python_version + " -m venv --prompt \"" + self.project_name + "\" " + TaskCreator.venv_dir
        return {
            "actions": [cmd_venv],
            "verbosity": 2
        }

    @staticmethod
    def setup():
        """Install project dependencies."""
        cmd_install = TaskCreator.get_pip() + " install --upgrade pip setuptools"
        cmd_install_dev = TaskCreator.get_pip() + " install .[dev]"
        return {
            "actions": [
                cmd_install,
                cmd_install_dev
            ],
            "verbosity": 2,
            "setup": ["create_virtual_environment"],
        }

    @staticmethod
    def make_distribution():
        """Create a source distribution and a package to be distributed."""
        return {
            "actions": [TaskCreator.get_python() + " setup.py sdist bdist_wheel"],
            "verbosity": 2,
            "setup": ["setup"],
        }

    @staticmethod
    def install():
        """Build and install the project inside the virtual environment."""
        return {
            "actions": [TaskCreator.get_pip() + " install --upgrade dist/*.whl"],
            "verbosity": 2,
            "setup": ["make_distribution"],
        }

    def test(self):
        """Run tests in the virtual environment."""
        cmd = TaskCreator.get_pytest() + " "
        options = ('-vv '
                   '-n auto '
                   '--ignore=tests/experiments/ '
                   '--html=build/tests/html/tests.html '
                   '--junitxml=build/tests/xml/tests.xml '
                   '--cov ' + self.project_name_sc + ' '
                   '--cov-report term '
                   '--cov-report html:build/tests/coverage/html '
                   '--cov-report xml:build/tests/coverage/xml/coverage.xml ')
        return {
            "actions": [cmd + options],
            "verbosity": 2
        }

    def lint(self):
        """Perform code analysis with pylint."""
        lint_dir = path.join("build",  "lint")
        return {
            "actions": [
                (create_dir, [lint_dir]),
                TaskCreator.get_flake8() + " " + self.project_name_sc + " | tee build/lint/flake8.log",
                TaskCreator.get_pylint() + " --output-format=parseable --reports=no " + self.project_name_sc + " | tee build/lint/pylint.log"
            ],
            "verbosity": 2
        }

    def doc(self):
        """Launch the generation of the project documentation."""
        from distutils.dir_util import copy_tree

        def copy_tree_checker(src, dst):
            """Wrap copy_tree to avoid pydoit error."""
            copy_tree(src, dst)
            return True

        doc_source_dir = path.join("build",  "doc", "source")
        return {
            "actions": [
                (create_dir, [doc_source_dir]),
                (copy_tree_checker, ["docs", doc_source_dir]),
                TaskCreator.get_sphinx() + "-apidoc -o build/doc/source --force --separate --module-first " + self.project_name_sc,
                TaskCreator.get_sphinx() + "-build -j auto -n build/doc/source build/doc/html"
            ],
            "verbosity": 2
        }

    def reset(self):
        """Delete project files except sources."""
        def remove_auxiliary_dir():
            egg_info_dir = self.project_name_sc + ".egg-info"
            remove_directories([
                egg_info_dir,
                ".env",
                ".eggs",
                ".pytest_cache",
                "build",
                "dist",
                ".cache",
                ".benchmark",
                ".tox",
                ".vagrant",
                ".tox"])
            remove_files([
                ".coverage",
                ".doit.db",
                ".doit.bak",
                ".doit.dat",
                ".doit.dir",
            ])

        # TODO(lschneider): Remove unnecessary files without command lines.
        # This code could be run directly from this function. However
        # the pathlib library is not part of the standard python 2.
        prefix = "python -c \"import pathlib; "
        delete_pyfiles = prefix + "import pathlib; [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]\""
        delete_dirs = prefix + "import pathlib; [p.rmdir() for p in pathlib.Path('.').rglob('__pycache__')]\""

        return {
            "actions": [
                delete_pyfiles,
                delete_dirs,
                remove_auxiliary_dir,
            ],
            "verbosity": 2
        }

    @staticmethod
    def get_pip():
        """Return the path to the right pip binary."""
        return path.abspath(TaskCreator.get_python()) + " -m pip" \
            if is_windows() else path.join(TaskCreator.bin_dir, "pip")

    @staticmethod
    def get_python():
        """Return the path to the right python binary."""
        return path.join(TaskCreator.bin_dir, "python")

    @staticmethod
    def get_pytest():
        """Return the path to the right pytest binary."""
        return path.join(TaskCreator.bin_dir, "py.test")

    @staticmethod
    def get_pylint():
        """Return the path to the right pylint binary."""
        return path.join(TaskCreator.bin_dir, "pylint")

    @staticmethod
    def get_flake8():
        """Return the path to the right flake8 binary."""
        return path.join(TaskCreator.bin_dir, "flake8")

    @staticmethod
    def get_sphinx():
        """Return the path to the right sphinx binary."""
        return path.join(TaskCreator.bin_dir, "sphinx")
