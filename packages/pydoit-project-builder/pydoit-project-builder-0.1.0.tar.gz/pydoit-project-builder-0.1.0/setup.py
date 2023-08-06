import os
from setuptools import setup, find_packages

runtime_dependencies = [
]

build_dependencies = [
    'wheel',
]


dev_dependencies = build_dependencies + [
    'pylint',
    'flake8',
    'flake8-docstrings',
    'pytest',
    'pytest-cov',
    'pytest-html',
    'pytest-xdist',
    'coverage',
]

setup(
    name='pydoit-project-builder',
    version='0.1.0',
    author='Loïc Schneider',
    description='Templates to be used when creating projects.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
    license='Apache 2',
    url='https://github.com/schneiderlo/pydoit-project-builder',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    setup_requires=build_dependencies,
    install_requires=runtime_dependencies,
    extras_require={
        'dev': dev_dependencies
    }
)
