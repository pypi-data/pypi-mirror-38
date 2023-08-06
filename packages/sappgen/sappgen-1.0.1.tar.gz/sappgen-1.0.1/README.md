[![GitHub contributors](https://img.shields.io/github/contributors/aayushuppal/sappgen.svg)](https://github.com/aayushuppal/sappgen/graphs/contributors)
[![Build Status](https://travis-ci.org/aayushuppal/sappgen.svg?branch=master)](https://travis-ci.org/aayushuppal/sappgen)

# SAPPGEN

Simple App Generator for Python

Python `3.7`

## Usage:

    $ sappgen [options] <project_name> <app_name>
    $ sappgen proj app

## Available options are:

    -h, --help         Show help

## Template 1 - App structure

    project
    ├── Makefile
    ├── testapp
    │   ├── cfg
    │   │   ├── config.py
    │   │   └── __init__.py
    │   ├── __init__.py
    │   ├── main.py
    ├── README.md
    ├── requirements-dev.txt
    │   └── util
    │       ├── __init__.py
    │       └── log_util.py
    └── tests
        └── test_testapp.py

    4 directories, 10 files

## Contact

- https://aayushuppal.github.io

## Links

- https://pypi.org/project/sappgen
- https://github.com/aayushuppal/sappgen
