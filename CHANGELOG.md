# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.15] - 2024-04-03
## Added
- Add Azure DevOps template release pipeline
- Add Azure DevOps pipeline creation

## [0.1.14] - 2024-04-02
## Fixed
- Fix run statements in release workflows

## [0.1.13] - 2024-04-02
## Added
- Support for choosing between Keep a Changelog and Conventional Changelog

## Fixed
- Update bad variable in standard project readme
- 'template_copy.zip' will no longer be committed to git for template repos

## Changed
- GitVersion replaced with commit-and-tag-version

## [0.1.12] - 2024-04-01
### Fixed
- Actually fix is_prerelease computer value in copier.yml

## [0.1.11] - 2024-04-01
### Fixed
- is_prerelease computer value in copier.yml

## [0.1.10] - 2024-04-01
### Fixed
- Lifecycle question in copier.yml

## [0.1.9] - 2024-04-01
### Fixed
- Remove copier.yml 'when' statements that caused important answers to be lost on template updates
- Remove template_copy.zip before generating new one

## [0.1.8] - 2024-04-01
### Added
- Project lifecycle state management

### Fixed
- Project name in template README

## [0.1.7] - 2024-03-30
### Fixed
- Attempt to unbreak copier.yml

## [0.1.6] - 2024-03-30
### Added
- Release PRs will now automerge

### Fixed
- Validators won't block upgrades anymore
- Documentation is automatically chosen
- Disable validators to allow updating

## [0.1.4] - 2024-03-28
### Fixed
- License file generation
- Better handling of tags and repo rulesets already existing

## [0.1.3] - 2024-03-28
### Fixed
- GitHub tags are only created when they don't already exist (attempt 2)

## [0.1.2] - 2024-03-28
### Fixed
- GitHub tags are only created when they don't already exist

## [0.1.1] - 2024-03-28
### Fixed
- Tagging of proper commit in releases
- Creation of sub-templates

## [0.1.0] - 2024-03-27
### Added
- Initial release

[Unreleased]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.15..HEAD
[0.1.15]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.14..v0.1.15
[0.1.14]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.13..v0.1.14
[0.1.13]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.12..v0.1.13
[0.1.12]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.11..v0.1.12
[0.1.11]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.10..v0.1.11
[0.1.10]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.9..v0.1.10
[0.1.9]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.8..v0.1.9
[0.1.8]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.7..v0.1.8
[0.1.7]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.6..v0.1.7
[0.1.6]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.4..v0.1.6
[0.1.5]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.5..v0.1.5
[0.1.5]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.4..v0.1.5
[0.1.4]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.3..v0.1.4
[0.1.3]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.2..v0.1.3
[0.1.2]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.1..v0.1.2
[0.1.1]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.0..v0.1.1
[0.1.1]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.0..v0.1.1
[0.1.0]: https://github.com/natescherer/postmodern-repo-template/tree/v0.1.0