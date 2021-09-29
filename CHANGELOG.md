# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

## Unreleased

### Added

### Fixed

### Removed

## v0.0.3 - 2021-09-29

### Changed

- Filtering out yaml files from the dockerfile sources since all three dockerfile linters
  use yaml files as their config files. (#12)

### Fixed

- Changing dockerfilelint rc file to an empty file since dockerfilelint doesn't handle an empty rules list.
  Adding issues to the statick output if one of the dockerfile linter plugins throws an error while parsing
  the output from it's tool. (#11)
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
