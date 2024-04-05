# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.47] - 2024-04-05
### Fixed
- Have rename-template-files task remove directories if there would be a conflict

## [0.1.46] - 2024-04-05
### Fixed
- Wrap square bracket for pwsh

## [0.1.45] - 2024-04-05
### Fixed
- Escape square bracket for pwsh

## [0.1.44] - 2024-04-05
### Fixed
- Use pwsh for rename-template-files task

## [0.1.43] - 2024-04-05
### Fixed
- Fix bad variables for move targets

## [0.1.42] - 2024-04-05
### Fixed
- Try using shutil.copytree for directory rename

## [0.1.41] - 2024-04-05
### Fixed
- Try another method of renaming

## [0.1.40] - 2024-04-05
### Fixed
- Try renaming just files as part of rename-template-files

## [0.1.39] - 2024-04-05
### Fixed
- Switch rename-template-files back to shutil.move
- Change how folders are renamed

## [0.1.38] - 2024-04-05
### Fixed
- Change how rename-template-files target paths are build

## [0.1.37] - 2024-04-05
### Fixed
- Reorder rename-template-files operations

## [0.1.36] - 2024-04-05
### Fixed
- Fix rename-template-files task root path

## [0.1.35] - 2024-04-05
### Fixed
- Update rename-template-files task to only alter files in template, not subtemplate

## [0.1.34] - 2024-04-05
### Fixed
- Fixed root path for rename-template-files task

## [0.1.33] - 2024-04-05
### Fixed
- rename-template-files task will now overwrite files

## [0.1.32] - 2024-04-05
### Added
- Dynamic repo URL in workflow doc

### Fixed
- New renaming-based subtemplate methodology

## [0.1.31] - 2024-04-05
### Fixed
- Fix bad template subtemplate generation

## [0.1.30] - 2024-04-05
### Fixed
- Whitespace issues in github release workflow
- Remove unneeded .versionrc.json

## [0.1.29] - 2024-04-04
### Fixed
- Remove now-defunct tarball from delete-unneeded-template-files task

## [0.1.28] - 2024-04-04
### Changed
- Root-level files synchronized into template
- Switch subtemplate generation from zip to copying to a subdirectory

## [0.1.27] - 2024-04-04
### Fixed
- Tagging in Azure DevOps repos

## [0.1.26] - 2024-04-04
### Fixed
- Ensure tasks.py exists for Standard projects

## [0.1.25] - 2024-04-04
### Fixed
- Typo in deleted-unneeded-template-files task name

## [0.1.24] - 2024-04-04
### Fixed
- Remove template-only files from being laid down in Standard mode
- Bad indentation in copier.yml tasks
- Removed hardcoded test repo name from create-pipelines-azdo task

## [0.1.23] - 2024-04-03
### Fixed
- Bad copier task names

## [0.1.22] - 2024-04-03
### Changed
- Switch to using tarball for template copy

### Fixed
- Tarball deletion will gracefully fail if file is missing

## [0.1.21] - 2024-04-03
### Fixed
- Escaping in github release workflows

## [0.1.20] - 2024-04-03
### Fixed
- Ensure template_copy.zip is included in release tag

## [0.1.19] - 2024-04-03
### Added
- Add full automation for template inheritance links

## [0.1.18] - 2024-04-03
### Added
- Make template inheritance links (somewhat) dynamic

### Fixed
- Commit formatting on Azure DevOps pipelines autocommits

## [0.1.17] - 2024-04-03
### Fixed
- Actually fix versionrc.json parserOpts for Azure DevOps

## [0.1.16] - 2024-04-03
### Fixed
- Jinja whitespace formatting in README docs
- versionrc.json parserOpts for Azure DevOps
- extract-changelog-release removed when in Keep a Changelog mode

## [0.1.15] - 2024-04-03
### Added
- Add Azure DevOps template release pipeline
- Add Azure DevOps pipeline creation

## [0.1.14] - 2024-04-02
### Fixed
- Fix run statements in release workflows

## [0.1.13] - 2024-04-02
### Added
- Support for choosing between Keep a Changelog and Conventional Changelog

### Fixed
- Update bad variable in standard project readme
- 'template_copy.zip' will no longer be committed to git for template repos

### Changed
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

[Unreleased]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.47..HEAD
[0.1.47]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.46..v0.1.47
[0.1.46]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.45..v0.1.46
[0.1.45]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.44..v0.1.45
[0.1.44]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.43..v0.1.44
[0.1.43]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.42..v0.1.43
[0.1.42]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.41..v0.1.42
[0.1.41]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.40..v0.1.41
[0.1.40]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.39..v0.1.40
[0.1.39]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.38..v0.1.39
[0.1.39]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.38..v0.1.39
[0.1.38]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.37..v0.1.38
[0.1.37]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.36..v0.1.37
[0.1.36]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.35..v0.1.36
[0.1.35]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.34..v0.1.35
[0.1.34]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.33..v0.1.34
[0.1.33]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.32..v0.1.33
[0.1.32]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.31..v0.1.32
[0.1.31]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.30..v0.1.31
[0.1.30]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.29..v0.1.30
[0.1.29]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.28..v0.1.29
[0.1.28]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.27..v0.1.28
[0.1.27]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.26..v0.1.27
[0.1.26]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.25..v0.1.26
[0.1.25]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.24..v0.1.25
[0.1.24]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.23..v0.1.24
[0.1.23]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.22..v0.1.23
[0.1.22]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.21..v0.1.22
[0.1.21]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.20..v0.1.21
[0.1.20]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.19..v0.1.20
[0.1.19]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.18..v0.1.19
[0.1.18]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.17..v0.1.18
[0.1.17]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.16..v0.1.17
[0.1.16]: https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.1.15..v0.1.16
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