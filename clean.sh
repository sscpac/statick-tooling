#!/bin/bash

rm -rf build/ dist/ .tox/ output-py* .pytest_cache */*.egg-info *.egg-info statick_output/* *.log
find . -name "*.pyc" -type f -delete
find . -type d -name .mypy_cache -exec rm -r {} +;
find . -type d -name __pycache__ -exec rm -r {} +;
