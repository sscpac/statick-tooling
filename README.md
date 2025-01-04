# Statick Tooling Plugins

![Unit Tests](https://github.com/sscpac/statick-tooling/workflows/Unit%20Tests/badge.svg)
[![PyPI version](https://badge.fury.io/py/statick-tooling.svg)](https://badge.fury.io/py/statick-tooling)
[![Codecov](https://codecov.io/gh/sscpac/statick-tooling/branch/main/graph/badge.svg)](https://codecov.io/gh/sscpac/statick-tooling)
![Python Versions](https://img.shields.io/pypi/pyversions/statick-tooling.svg)
![License](https://img.shields.io/pypi/l/statick-tooling.svg)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
![Daily Downloads](https://img.shields.io/pypi/dd/statick-tooling.svg)
![Weekly Downloads](https://img.shields.io/pypi/dw/statick-tooling.svg)
![Monthly Downloads](https://img.shields.io/pypi/dm/statick-tooling.svg)

This is a set of plugins for [Statick](https://github.com/sscpac/statick) that will discover tooling related
files and perform static analysis on those files.

Custom exceptions can be applied the same way they are with [Statick exceptions][Exceptions].

## Table of Contents

- [Statick Tooling Plugins](#statick-tooling-plugins)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Pip Install](#pip-install)
    - [Pip Install and Custom Configuration](#pip-install-and-custom-configuration)
    - [Source Install and Custom Configuration](#source-install-and-custom-configuration)
  - [Existing Plugins](#existing-plugins)
    - [Discovery Plugins](#discovery-plugins)
    - [Tool Plugins](#tool-plugins)
  - [Contributing](#contributing)
    - [Mypy](#mypy)
    - [Formatting](#formatting)

## Installation

The recommended method to install these Statick plugins is via pip:

```shell
pip install statick-tooling
```

You can also clone the repository and use it locally.

## Usage

Make sure you install all the dependencies from apt/npm.
See <https://github.com/nodesource/distributions> for Node/npm installation instructions.

Configure npm to allow a non-root user to install packages.

```shell
npm config set prefix '~/.local/'
```

Make sure `~/.local/bin` exists.
Check your `PATH` with `echo $PATH`.
If `~/.local/bin` is not listed then add it to your `PATH`.

```shell
mkdir -p ~/.local/bin
echo 'export PATH="$HOME/.local/bin/:$PATH"' >> ~/.bashrc
```

Install npm packages.

```shell
npm install -g dockerfilelint
npm install -g dockerfile_lint
```

### Pip Install

The most common usage is to use statick and statick-tooling from pip.
In that case your directory structure will look like the following:

```shell
project-root
 |- tooling-project
 |- statick-config
```

To run with the default configuration for the statick-tooling tools use:

```shell
statick tooling-project/ --output-directory statick-output/ --profile tooling-profile.yaml
```

### Pip Install and Custom Configuration

There are times when you will want to have a custom Statick configuration.
This is usually done to run a different set of tools than are called out in the default profile, or to add exceptions.
For this case you will have to add the new Statick configuration somewhere.
This example will have custom exceptions in the tooling-project, such that the directory structure is:

```shell
project-root
 |- tooling-project
 |- statick-config
     |- rsc
         |- exceptions.yaml
 |- statick-output
```

For this setup you will run the following:

```shell
statick tooling-project/ --output-directory statick-output/ --user-paths tooling-project/statick-config/ --profile tooling-profile.yaml
```

### Source Install and Custom Configuration

The last type of setup will be to have all of the tools available from cloning repositories, not installing from pip.
The directory structure will look like:

```shell
project-root
 |- tooling-project
 |- statick-config
     |- rsc
         |- exceptions.yaml
 |- statick-output
 |- statick
 |- statick-tooling
```

Using the example where we want to override the default exceptions with
custom ones in the tooling-project, the command to run would be:

```shell
./statick/statick tooling-project/ --output-directory statick-output/ --user-paths statick-tooling/,tooling-project/statick-config/ --profile tooling-profile.yaml
```

## Existing Plugins

### Discovery Plugins

Note that if a file exists without the extension listed it can still be discovered if the `file` command identifies it
as a specific file type.
This type of discovery must be supported by the discovery plugin and only works on operating systems where the `file`
command exists.

File Type | Extensions
:-------- | :---------
dockerfile | `Dockerfile*`

### Tool Plugins

Tool | About
:--- | :----
[dockerfilelint][dockerfilelint] | A rule based 'linter' for Dockerfiles.
[dockerfile-lint][dockerfile-lint] | A rule based 'linter' for Dockerfiles.
[hadolint][hadolint] | Dockerfile linter, validate inline bash, written in Haskell.

## Contributing

If you write a new feature for Statick or are fixing a bug,
you are strongly encouraged to add unit tests for your contribution.
In particular, it is much easier to test whether a bug is fixed (and identify
future regressions) if you can add a small unit test which replicates the bug.

Before submitting a change, please run tox to check that you have not
introduced any regressions or violated any code style guidelines.

### Mypy

Statick Tooling uses [mypy][MyPy] to check that type hints are being followed properly.
Type hints are described in [PEP 484][Pep484] and allow for static typing in Python.
To determine if proper types are being used in Statick Tooling the following command will show any errors, and create several
types of reports that can be viewed with a text editor or web browser.

```shell
python3 -m pip install mypy
mkdir report
mypy --ignore-missing-imports --strict --html-report report/ --txt-report report src
```

It is hoped that in the future we will generate coverage reports from mypy and use those to check for regressions.

### Formatting

Statick code is formatted using [black][Black].
To fix locally use

```shell
python3 -m pip install black
black src tests
```

[Black]: https://github.com/psf/black
[Exceptions]: https://github.com/sscpac/statick/blob/master/GUIDE.md#exceptionsyaml
[MyPy]: http://mypy-lang.org/
[Pep484]: https://www.python.org/dev/peps/pep-0484/
[dockerfilelint]: https://github.com/replicatedhq/dockerfilelint
[dockerfile-lint]: https://github.com/projectatomic/dockerfile_lint
[hadolint]: https://github.com/hadolint/hadolint
