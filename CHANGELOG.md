# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## Unreleased

### Added

### Fixed

## v0.1.1 - 2022-10-11

### Changed

- Updated tool plugins to match new structure introduced in sscpac/statick#423.
- Update `inherits_from` usage in configuration file to match new list format.

### Fixed

- Pin flake8<5 and pycodestyle<2.9.0 until <https://github.com/tholo/pytest-flake8/issues/87> is fixed.

## v0.1.0 - 2022-01-04

### Removed

- Drop support for Python 3.6 due to end-of-life of that distribution.
  See <https://endoflife.date/python>.
  To continue using Statick with Python 3.6 [pin the version](https://pip.pypa.io/en/stable/user_guide/)
  used to the `0.0` tags.
  An example is at the discussion at <https://github.com/sscpac/statick/discussions/376>.

## v0.0.4 - 2022-01-04

### Added

- Add Python 3.10 support. (Thomas Denewiler, @tdenewiler, #18)
- Switch testing environment from macos-latest to macos-10.15.
  This is to retain support for Python 3.6. (Thomas Denewiler, @tdenewiler, #16)

### Fixed

- Adding Python 3.10 to setup.py and tox.ini to allow tests to run properly. (#20)
- Use quotes for version numbers in YAML to avoid truncating trailing zeros. (Thomas Denewiler, @tdenewiler, #18)

### Removed

## v0.0.3 - 2021-09-29

### Changed

- Filtering out yaml files from the dockerfile sources since all three dockerfile linters
  use yaml files as their configuration files. (#12)

### Fixed

- Changing dockerfilelint rc file to an empty file since dockerfilelint doesn't handle an empty rules list. (#11)
- Adding issues to the statick output if one of the dockerfile linter plugins throws an error while parsing
  the output from its tool. (#11)
- Adding dockerfile_lint to npm dependency file. (@gregtkogut, #10)

## v0.0.2 - 2021-08-05

### Fixed

- Correcting usage of dockerfilelint config file
  (the tool expects a directory path, not the full file path). (#3)

## v0.0.1 - 2021-06-09

### Added

- Initial release (Alexander Xydes, @axydes)
- Dockerfile discovery plugin.
- [dockerfilelint](https://github.com/replicatedhq/dockerfilelint) tool plugin.
- [dockerfile-lint](https://github.com/projectatomic/dockerfile_lint) tool plugin. (#1)
