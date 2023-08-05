"""
Setup Module to setup Python Handlers (Git Handlers) for the Git Plugin.
"""
import setuptools

VERSION = '0.0.1'

setuptools.setup(
    name = 'datalayer',
    version = VERSION,
    description = 'Datalayer',
    long_description = open('README.md').read(),
#    packages = setuptools.find_packages(),
    packages = [
        'jupyterlab_twitter',
    ],
    package_data = {
        'py/jupyterlab_twitter': [
            '*',
        ],
    },
    setup_requires = [
    ],
    install_requires = [
        'notebook',
        'psutil',
    ],
    tests_requires = [
        'pytest',
        'pytest-cov',
        'pylint',
    ],
)
