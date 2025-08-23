# Changelog

## [0.5.8](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.5.7...v0.5.8) (2025-08-23)


### Bug Fixes

* Fix token criteria ([#746](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/746)) ([4ecba7d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4ecba7da256ce6cd26643446d5ec8c902c3fbc89))

## [0.5.7](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.5.6...v0.5.7) (2025-08-23)


### Bug Fixes

* Restore the None option for repo_setup_actions ([#744](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/744)) ([042edef](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/042edef78c1170179d510b5bc5da7d16493c7833))

## [0.5.6](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.5.5...v0.5.6) (2025-08-22)


### Bug Fixes

* Fix azdo update check ([#742](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/742)) ([535ff77](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/535ff7749079ac222b4f5a2c64af4f6794d6ac24))

## [0.5.5](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.5.4...v0.5.5) (2025-08-22)


### Features

* Refactor license question ([#740](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/740)) ([5895839](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5895839b424f9c8012ae96d7eb0a66fbf5ca5d0a))

## [0.5.4](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.5.3...v0.5.4) (2025-08-22)


### Features

* Refactor github_repo_description to project_description ([#738](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/738)) ([ff8a9f3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ff8a9f3195d0bf88de57fdd28786cd07bfcc59b7))

## [0.5.3](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.5.2...v0.5.3) (2025-08-22)


### Features

* Ask setup questions once ([#736](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/736)) ([1f93115](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1f93115fd1c9cede407c058f067a0fd12aecbfeb))
* Implement copyright_year computed value ([#732](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/732)) ([c08a7ab](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c08a7ab7d824be48e90167fb5071871c44a909a2))
* Remove context.py in favor of _copier_operation ([#734](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/734)) ([4d02a22](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4d02a22aed21b5093de56b45b93567358782ed1b))

## [0.5.2](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.5.1...v0.5.2) (2025-08-15)


### Bug Fixes

* Properly make vcs_ref optional for copy_template_files ([#730](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/730)) ([6dcfcf4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6dcfcf4c57585a7d61a5f621ae5b67240f4484c5))

## [0.5.1](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.5.0...v0.5.1) (2025-08-15)


### Features

* Add checks for secret existence to all workflows ([#727](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/727)) ([a89cddb](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a89cddb31bc900f5088acb4bd07d57f3ee13d99e))


### Bug Fixes

* Fix copier-update mise task ([#724](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/724)) ([65c61da](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/65c61da528de566f602a06471e4744414408a68d))
* Fix template update github workflow ([#726](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/726)) ([b2c233a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b2c233a3d557a70d5634de771a3c5bf578259816))
* Fix template-update-check azdo pipeline ([#728](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/728)) ([dbc7d9a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/dbc7d9ad706d4fdf462de66baf00af68aa81fab8))
* Rename to copier-update-check ([#729](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/729)) ([4a066ef](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4a066ef9ef1feb7ced6f33f27ab1c5a82289b872))

## [0.5.0](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.4.4...v0.5.0) (2025-08-14)


### ⚠ BREAKING CHANGES

* remove overcomplex template extensions ([#669](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/669))
* remove copier-template-overrides.yml from template structure ([#647](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/647))

### Features

* Add mkdocs for azdo ([#708](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/708)) ([09fd850](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/09fd85029e4d5afebef7ac1b5abf8e4464e14ac5))
* Implement github_repo_owner calculated value ([#687](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/687)) ([f08dc4e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f08dc4eeee4c9f9a249592ce8c433adb796f5abb))
* Move ci tooling into mise.ci.toml ([#688](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/688)) ([fe56eef](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/fe56eef5ff83b2461e3c314449f0201fbdbda657))
* Remove copier-template-overrides.yml from template structure ([#647](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/647)) ([1c1efbf](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1c1efbf9ef0da9f98edf72f7a085d709b46bd18e))
* Remove cruft ([#652](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/652)) ([d892af4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d892af45122766dfc7dc953f3c2586984226dc49))
* Remove lychee ([#650](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/650)) ([0a07459](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0a0745973c903ca36c1b85e829d34ad4c102610e))
* Remove overcomplex template extensions ([#669](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/669)) ([074c640](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/074c64016ec9619c23b43eda62fa7c5d1eeac25b))
* Simplify postinstall hook ([#714](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/714)) ([1adf257](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1adf257ec4a2b85dd253679948ae5d2c4fb61e51))
* Switch from unicode-slugify to python-slugify ([#646](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/646)) ([4aeb511](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4aeb5116073777df8fb29e9a28b351f0ae877672))
* Switch to renamed copier-template-extensions library ([#655](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/655)) ([339ada5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/339ada59ee63542d339867d4919d5b53168a2e7d))
* Update repo to template v0.4.4 ([#642](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/642)) ([762a909](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/762a9095ada4106114be9ffb36ca2c45a4447589))


### Bug Fixes

* Fix path for markdownlint config ([#644](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/644)) ([edde88f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/edde88f2fe406844008b1ccbaecc52a315d14dc0))
* Fix template rendering on windows ([#720](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/720)) ([f82b22e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f82b22efd32122394334d022aef907d5e496fee7))
* Give invoke the dependencies it needs ([#675](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/675)) ([658c608](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/658c608a4c9efc5c3ed3eb09de27cc32263984b8))
* Inject copier into invoke ([#674](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/674)) ([bb805fa](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/bb805faefcc4b7f6d3647f7a21fc358ed004194c))
* Make sure invoke is on path ([#668](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/668)) ([53dca16](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/53dca166e1d053db597bcd7d1faae618109b0e6b))
* Remove bad include ([#658](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/658)) ([a3b218d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a3b218dbe3dd17df5e7bdc02f5d18adaaaf236aa))
* Remove duplicate pr workflow ([#649](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/649)) ([28be5df](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/28be5df81a92128e3efa4283d0168c151f56bd08))
* Remove mise.init.toml from delete_unneeded_template_files task ([#722](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/722)) ([20f66e9](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/20f66e99742e62f04eb2ede4c2a53a5f301279d6))
* Remove requirements-txt-fixer from pre-commit ([#679](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/679)) ([141c249](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/141c249cb775512ea69fb7e88eaa470cc406f9a2))
* Remove slugify dep ([#670](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/670)) ([88ac131](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/88ac1311e23f4ee507cffb67a535fb8e3ce9980d))
* Remove unneeded git clone depth ([#712](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/712)) ([3fe92ab](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3fe92abc1dbb6f97a2c07dcfc5431414986ec474))
* Restructure intergraton tests ([#716](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/716)) ([476d069](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/476d0697368d0ec7a385187b5791d0c0063d0078))
* Wrap mise templates in jinja raw tags ([#717](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/717)) ([d1990a7](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d1990a72a57d54a957a83826515f089d1e9887a1))


### Miscellaneous

* **deps:** Update actions/checkout action to v5 ([#707](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/707)) ([70c0417](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/70c04178a9a976245207e0da86ffb047ac67ed01))
* **deps:** Update dependency apprise to v1.9.3 ([#628](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/628)) ([20ecab0](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/20ecab08174a0d5c950a87cd64ea19d4f5a1c317))
* **deps:** Update dependency apprise to v1.9.4 ([#693](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/693)) ([945e7b7](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/945e7b74ff31ca2390ff041178361f69e0832a0c))
* **deps:** Update dependency astral-sh/uv to v0.7.21 ([#629](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/629)) ([ebbfd52](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ebbfd528bd939ec9c33095e2576d589d8307de9b))
* **deps:** Update dependency astral-sh/uv to v0.8.0 ([#676](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/676)) ([14c7de8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/14c7de8c0238c9fdddfd270a2f5b04a6c7682f67))
* **deps:** Update dependency astral-sh/uv to v0.8.5 ([#681](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/681)) ([6e0b355](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6e0b35515f37e85bd41d21bf89d3e71c92d46e06))
* **deps:** Update dependency astral-sh/uv to v0.8.8 ([#702](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/702)) ([e763858](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e76385821d885f86010bb3d593854de6ed5e048a))
* **deps:** Update dependency astral-sh/uv to v0.8.9 ([#709](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/709)) ([9f212a1](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9f212a1bf85d9a7d49b8d9d00becf15ed8757d96))
* **deps:** Update dependency commit-and-tag-version to v12.5.1 ([#625](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/625)) ([478c886](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/478c886f13de671393bb2189cceb3abfe2fd19cd))
* **deps:** Update dependency commit-and-tag-version to v12.5.2 ([#697](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/697)) ([447a1ee](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/447a1ee2b3ee77b35889ecd8b4fcc5bc9515e84c))
* **deps:** Update dependency copier to v9.8.0 ([#632](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/632)) ([dc2f55c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/dc2f55cc81dc11c865e9ecd94904695a3bdd133b))
* **deps:** Update dependency copier to v9.9.0 ([#691](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/691)) ([e830494](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e830494951e5e01a80649d6cbc1addafaa956009))
* **deps:** Update dependency copier-template-extensions to v0.3.3 ([#656](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/656)) ([5929342](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5929342a2e8a2eb4e3f4dc618ad347e21b4f3094))
* **deps:** Update dependency githubkit to v0.12.16 ([#633](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/633)) ([988d1d1](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/988d1d11b0af86ccf82419a00947258dd67d2cc2))
* **deps:** Update dependency githubkit to v0.13.0 ([#686](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/686)) ([f64fe7a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f64fe7a2112dda256fc4eae29ad9919b00634aaa))
* **deps:** Update dependency githubkit to v0.13.1 ([#706](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/706)) ([a51174a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a51174a2b5637e2e32e26ccbaf1149f400d0c083))
* **deps:** Update dependency google/yamlfmt to v0.17.2 ([#622](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/622)) ([4372bf0](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4372bf01c703a4d6a6f183fa072274d89de066e9))
* **deps:** Update dependency invoke to v2.2.0 ([#660](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/660)) ([c62c9f2](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c62c9f21296d143fb93b329fd2f5ed1dd1456bbe))
* **deps:** Update dependency invoke to v2.2.0 ([#671](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/671)) ([fe5174a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/fe5174a1455d8b112e6282e0c82ddd36259f2ec5))
* **deps:** Update dependency jinja2-shell-extension to v2.1.1 ([#634](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/634)) ([48678be](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/48678be64879d8a438d31cf47a471b9d9094e185))
* **deps:** Update dependency jinja2-time to v0.2.0 ([#661](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/661)) ([fd79dd0](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/fd79dd0b84a16890844ddb0fe3a96e2e64cd9c9b))
* **deps:** Update dependency mikefarah/yq to v4.46.1 ([#635](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/635)) ([a339a36](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a339a36438b64fd957278a9087054995e088597e))
* **deps:** Update dependency mikefarah/yq to v4.47.1 ([#699](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/699)) ([c6bda8e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c6bda8e1c008103b67f2975b55c3376110e40c39))
* **deps:** Update dependency mkdocs-material to v9.6.16 ([#698](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/698)) ([311f90d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/311f90ddfd8f5b3ac10d1c13038daa593df5f1aa))
* **deps:** Update dependency pipx:apprise to v1.9.3 ([#653](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/653)) ([c28ecba](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c28ecba85a29d9b93c7ccc1f81c4df09fe418ced))
* **deps:** Update dependency pipx:apprise to v1.9.4 ([#694](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/694)) ([2f03c0d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2f03c0d88ee5a24d52560807fde1aab16430d235))
* **deps:** Update dependency pipx:copier to v9.8.0 ([#662](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/662)) ([2ea8e8d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2ea8e8d31f94b40ae3ce7c90b3b8f40c13435d53))
* **deps:** Update dependency pipx:copier to v9.9.0 ([#692](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/692)) ([5d3f525](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5d3f5254ebdde14c56c530b80bad6e3d7a705e99))
* **deps:** Update dependency pipx:invoke to v2.2.0 ([#672](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/672)) ([fcc26f5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/fcc26f5b842115667bf8e573ab0a6fb42c5b7210))
* **deps:** Update dependency pipx:pre-commit to v4.2.0 ([#663](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/663)) ([8d264d1](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8d264d19c2a31f5c4021dae25e675913f14fcdc5))
* **deps:** Update dependency pipx:pre-commit to v4.3.0 ([#704](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/704)) ([bb03bf0](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/bb03bf011b32edb497790400a2302aa94617f0b1))
* **deps:** Update dependency pre-commit to v4.2.0 ([#664](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/664)) ([b5a2e08](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b5a2e08b8cfc7b4b8b500f4b20707fe53a27dd94))
* **deps:** Update dependency pre-commit to v4.3.0 ([#705](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/705)) ([d21a6a5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d21a6a5bcfc81220cf03b6423d1721eb7afb71c1))
* **deps:** Update dependency python to v3.13.5 ([#654](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/654)) ([351b8ae](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/351b8ae9cddd3a20e7596fc63f50c7e909bff4b9))
* **deps:** Update dependency python to v3.13.6 ([#695](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/695)) ([8594904](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8594904a4a0990d38a1a2645891dd1524fbf9e37))
* **deps:** Update dependency requests to v2.32.4 ([#657](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/657)) ([afc09af](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/afc09af60b34211f0e87cdf4a328b177882c6e5f))
* **deps:** Update dependency rich to v14 ([#667](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/667)) ([2c510ea](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2c510eac3b3d1c809d48c0af75fc52571411b735))
* **deps:** Update dependency rich to v14.1.0 ([#685](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/685)) ([ef808a4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ef808a432383ab7b67fca56cdc455bc93241d66e))
* **deps:** Update dependency uv to v0.7.21 ([#659](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/659)) ([e9df8f8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e9df8f8a177df8b30a08560b5714ab6b70b0c455))
* **deps:** Update dependency uv to v0.8.0 ([#677](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/677)) ([dba2b02](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/dba2b02da4abb56286f2a2da102e62d2d1bd6287))
* **deps:** Update dependency uv to v0.8.5 ([#682](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/682)) ([385aeb6](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/385aeb639acd855b5bcceaf88cd35de27c383093))
* **deps:** Update dependency uv to v0.8.8 ([#703](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/703)) ([fc523c8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/fc523c8237d876595960e547b845037dc9be5aab))
* **deps:** Update dependency uv to v0.8.9 ([#710](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/710)) ([9c6e045](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9c6e0453ae2cd30303c1e93f20039abdccd292f7))
* **deps:** Update dependency yamlfmt to v0.17.2 ([#623](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/623)) ([56d37fa](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/56d37fac4ad26fb812938461000e43d6a47cec0c))
* **deps:** Update dependency yq to v4.46.1 ([#665](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/665)) ([8071e94](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8071e947277e047f70d44d3701cc375984a1746e))
* **deps:** Update dependency yq to v4.47.1 ([#684](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/684)) ([437c769](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/437c7690038b1d571d9aa0bcf35c5a3b8fd407fb))
* **deps:** Update node.js to v22.17.1 ([#666](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/666)) ([6bcdb29](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6bcdb29cb8328c304cc2b1c09c05d878781b532f))
* **deps:** Update node.js to v22.18.0 ([#700](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/700)) ([6275d3b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6275d3bd31c3441cdbf8242c249411bdfb05894c))
* **deps:** Update peter-evans/create-pull-request action to v7 ([#701](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/701)) ([f87eb7b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f87eb7bc20956cf481ae24c70e9df8513cb082e2))
* Remove mise.init.toml ([#721](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/721)) ([55676e5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/55676e57fa146001ebbfc540e768f50d0682d92c))

## [0.4.4](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.4.3...v0.4.4) (2025-06-24)


### Bug Fixes

* Wrap custom manager code in raw tags ([#640](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/640)) ([5f6cd4b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5f6cd4b89ce36e573b829f600351847bdd3824e8))

## [0.4.3](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.4.2...v0.4.3) (2025-06-24)


### Bug Fixes

* Backport config changes into template ([#638](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/638)) ([fc64a6b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/fc64a6b45781de02c628ad3a389c6132ed263078))

## [0.4.2](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.4.1...v0.4.2) (2025-06-24)


### Bug Fixes

* Wrap double brackets in raw tag ([#636](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/636)) ([f563902](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f56390247b5fc48f1410a258121df8323029dc19))

## [0.4.1](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.4.0...v0.4.1) (2025-06-20)


### Features

* Add mise task copier-update ([#616](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/616)) ([dd3304e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/dd3304eb31470c47725d054e40b14bcd11dddbc5))
* Centralize all dependencies into mise.toml ([#624](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/624)) ([372eda7](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/372eda7ac8764f44f694f4ccff2abb354c8b42e5))
* Clean up workflows and pipelines ([#631](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/631)) ([dba611a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/dba611a7accb547fc25e4aca12c79538cc050150))
* Convert azdo to a notification model for copier updates ([#620](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/620)) ([0cbf09e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0cbf09e66804dc468995dc583bfe20a9aa61def5))
* Overhaul copier update workflow ([#617](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/617)) ([d1c3c66](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d1c3c6697bef377dc8ca406530d0cb9c7dd7a552))
* Send apprise notifcations for copier updates from github actions ([#619](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/619)) ([9f5b8dd](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9f5b8ddbc4d10a4f5b43cea41fc286ca880b003e))


### Bug Fixes

* Fix bad dependency comments ([#627](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/627)) ([9d05ad5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9d05ad550e212a69aeedd8faf854d74084fe1c16))
* Fix jinja syntax in mise.toml.jinja ([#614](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/614)) ([6d0fcb7](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6d0fcb71601afec4d610f647a5a5edef7971bcdb))
* Fix renovate pipx custom manager ([#630](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/630)) ([2808c39](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2808c39aad2b967f40d4949f0d826d4a6d82095f))

## [0.4.0](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.47...v0.4.0) (2025-06-18)


### ⚠ BREAKING CHANGES

* remove devcontainer setup in favor of mise ([#613](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/613))
* move copier answers into .config directory ([#610](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/610))
* move version file for azdo repos into .config
* move release-please configuration into .config

### Features

* Add renovate updating for templated mise.toml ([#589](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/589)) ([142ce5f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/142ce5fedaf8254663e02f3e661f6b519d002579))
* Improve how renovate works with mise.toml.jinja ([#596](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/596)) ([2878a68](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2878a68964e02c5ab7ef1ee3e1e84f6c2b2e3fbe))
* Improve repo_name default to be dst_path ([#577](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/577)) ([aed1ecd](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/aed1ecdaf02495f8bfc3fa73c75244c87502cd3a))
* Improve templates for lychee and typos config ([#575](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/575)) ([d90b167](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d90b1674879c385c0150be741b1ab7eab287d6e9))
* Move copier answers into .config directory ([#610](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/610)) ([0cd9a8a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0cd9a8a561698d67b0fd8405e42d9a8dbdfa2dcb))
* Move release-please configuration into .config ([036b39a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/036b39ac073163997d3a4b31e95342e840c45d79))
* Move version file for azdo repos into .config ([396244d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/396244d74f8b2fb97542494252b9d0d4fb55b25d))
* Reactor pip installations to work better cross-platform ([#583](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/583)) ([64ea97f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/64ea97fc45d67c91e624c3ff337c9a7b7a9cbae6))
* Remove devcontainer setup in favor of mise ([#613](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/613)) ([6dafa15](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6dafa15804c23c4d2d75b322e08c33c34292f742))
* Replace hk with pre-commit ([#586](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/586)) ([6205a02](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6205a02494201f622f82a7a9cb86b9488f3a40de))
* Sync renovate config between template and repo ([#602](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/602)) ([900fe5c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/900fe5c946a71f9d9e5a50e124cfe7b50358d325))
* Update renovate versioning ([#597](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/597)) ([975d15a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/975d15a0e2360655ae238bad5f105b8f830c46bf))


### Bug Fixes

* Change hk --from-ref option ([#572](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/572)) ([8ac4aba](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8ac4aba5c4b577add2272539ce3cf04fec1b4d35))
* Fix azure devops bugs ([#588](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/588)) ([69eccb3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/69eccb3e99b4ee1e435c47d0cef31c593154c75e))
* Fix mise hook setup on sh systems ([#611](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/611)) ([487b63c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/487b63cbb6a7840aaf26a85a8f497fab61e04d1f))
* Fix renovate config ([#606](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/606)) ([d0cdd53](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d0cdd53bc38180a8269100b6175487fa9a471725))
* Fix yamlfmt renovate comment ([#592](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/592)) ([e15e00f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e15e00fd04babb5c55089aadd919239990937ad3))
* Make sure pipx is installed before other tools ([#570](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/570)) ([cf9eac0](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/cf9eac0992562bd6265e9441ab95dae531f7e2ae))


### Miscellaneous

* **deps:** Update dependency commit-and-tag-version to v12.5.1 ([#595](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/595)) ([df49e17](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/df49e17dfab699c41b0f5aa1da3b8ae956f77ffd))
* **deps:** Update dependency commit-and-tag-version to v12.5.1 ([#598](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/598)) ([8898581](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8898581f3853fdd9510508f8d39478106a212e42))
* **deps:** Update dependency githubkit to v0.12.14 ([#584](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/584)) ([73a2c01](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/73a2c01254885002ec286c50f043793df6f4bda0))
* **deps:** Update dependency google/yamlfmt to v0.17.0 ([#594](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/594)) ([0179212](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/017921271ea3853b49df944ea88fea1a0929aea6))
* **deps:** Update dependency google/yamlfmt to v0.17.0 ([#600](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/600)) ([1f97c1f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1f97c1fe25b5733f3bb2f976f84c0a31c5bc0c97))
* **deps:** Update dependency python to v3.13.5 ([#578](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/578)) ([01cfd3a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/01cfd3a1f8863fab3499f2da613dfe634facbd83))
* **deps:** Update dependency python to v3.13.5 ([#599](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/599)) ([8884e32](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8884e3217d2baaf514ab08fb0f4046246a6b96ad))
* **deps:** Update dependency requests to v2.32.4 ([#580](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/580)) ([f7acfdc](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f7acfdcfe96df90d74478282bcba3a1b0ee091dc))
* **deps:** Update dependency yamlfmt to v0.17.0 ([#591](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/591)) ([d0b23d9](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d0b23d97cbce184c9f486c3f429ad238db8b0c3c))
* **deps:** Update node.js to v22.16.0 ([#601](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/601)) ([f88ead3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f88ead31ec702fa290a57c25c5a3f44e2a8b6049))

## [0.3.47](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.46...v0.3.47) (2025-06-02)


### Bug Fixes

* Set fetch-depth to 0 to support hk ([#561](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/561)) ([1dd03c2](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1dd03c294a8d061d627d6e4a64a27262c78a75ce))

## [0.3.46](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.45...v0.3.46) (2025-06-02)


### Bug Fixes

* Don't lint azure pipelines yaml files ([def2560](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/def256020899a6eeea6d9d280da8b85096ab9e43))
* Fix azdo copier update pipeline ([200d952](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/200d95240c11b2994418a1a23514624a308bd397))
* Fix azdo copier updating pipeline ([12471b0](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/12471b05ca5aa5cc8f82fc67c9246fcad4a875d6))
* Fix hk to properly run on PRs ([#559](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/559)) ([6c581a6](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6c581a659ae56f2c747d2906147cf3f2cee24705))

## [0.3.45](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.44...v0.3.45) (2025-06-02)


### Features

* Improve logging for mise postinstall hooks ([fe2eed3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/fe2eed344153fab4319b41ab5b6be465852662d2))
* Improve logging for mise postinstall hooks ([9a8f4ac](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9a8f4ac6f7e55d64c5f99e1b99c19aa5023fcf8c))

## [0.3.44](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.43...v0.3.44) (2025-06-02)


### Bug Fixes

* Change to always use token for first git push ([b2f575b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b2f575b8b2c172721798b885582e47ada77ba71e))
* Change to always use token for first git push ([a7cb007](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a7cb007063a28b9e54e8c3f4c85924328e3488af))
* Clean up git credentials settings ([5b5220d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5b5220d7899120ca4820ce8d0d20d0d7d09425ee))
* Clean up git credentials settings ([5d4cab0](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5d4cab02405b940ea4ff6bd7218e9f427e265996))

## [0.3.43](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.42...v0.3.43) (2025-06-02)


### Features

* Copier update to parent template v0.3.42 ([dea71ff](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/dea71ffb6a05f053d663cd0a46141d0d9b03eda9))
* Copier update to parent template v0.3.42 ([7b328f6](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7b328f675d6f42d1c694f394cb54eb79c252f6ad))
* Replace phase_extension.py with _copier_operation ([73519d8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/73519d8c0d58a9d0548b5ced708d9c642189b316))
* Replace phase_extension.py with _copier_operation ([f26646d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f26646d4654fd46e0ed6874de7542cc5e39927c6))

## [0.3.42](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.41...v0.3.42) (2025-06-02)


### Bug Fixes

* Fix template structure issues ([beae721](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/beae72174637cd8207f81927bdbe350e73f599c5))
* Fix template structure issues ([609a61b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/609a61b28e9dbbdd91e0b092e8768cb85a2c31e9))

## [0.3.41](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.40...v0.3.41) (2025-06-02)


### Bug Fixes

* Activate venvs as needed ([26fd914](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/26fd914dba1f348de682b4e93093623d951c230a))
* Add necessary invoke dependency for copier ([7099a1a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7099a1a6f280dd4880d70253d2b2f2d819130e4d))
* Switch copier workflows to pure bash ([3a81c49](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3a81c498c95563d2fa34c4188d234910713ac52a))
* Switch copier workflows to pure bash ([81b4b15](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/81b4b1502d271d4bdfc045c10b142aeef455025d))

## [0.3.40](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.39...v0.3.40) (2025-06-02)


### Features

* Copier update to parent template v0.3.39 ([c9b34cc](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c9b34cc63a2e9e1c6c453f6408c78f857ac05453))
* Copier update to parent template v0.3.39 ([f9e24af](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f9e24afee6c79c97770fec2f62ed93385d22ea98))
* Update copier update workflows to use mise ([e19976d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e19976db2f01c7abc043c548f3b70d512af12936))
* Update copier update workflows to use mise ([aa2fa33](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/aa2fa33a597398c3301638d27a572c6e57da2b88))


### Bug Fixes

* Fix errors in template ([90479ad](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/90479ad0c57d1432d5da25a673f5cc855f1c50f6))
* Fix errors in template ([335d910](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/335d910e1fd26a1dadca9169bfbc7a4b1c298f97))

## [0.3.39](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.38...v0.3.39) (2025-06-02)


### Bug Fixes

* Fix jinja errors in template ([52060a6](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/52060a646a3ad303b8e3cfcb7995a862a4bfbf7b))
* Fix jinja errors in template ([5916961](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5916961b04c0f84897f4a755d3124d901c2a71e3))

## [0.3.38](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.37...v0.3.38) (2025-06-02)


### Features

* Improve yaml linting ([3812016](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3812016da7ddb3a7e96433d3c5ee6d5621e7b918))
* Migrate markdownlint and cspell to mise/hk ([ceeaebc](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ceeaebc8f8a8d417e13035522eb704e0db9a4fc7))
* Migrate yamllint from trunk to hk ([532903b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/532903bdfeaa356d63fbd2a9be3fa25cc0e34b42))
* Move actionlist from trunk to mise/hk ([14bc05a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/14bc05ac42e2ba5770a0136653ff15b7f9fbc382))
* Move commitlint from trunk to mise/hk ([07fbf82](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/07fbf829b83aba27b2a91802ee1750d454cfd235))
* Move markdown-link-check from trunk to mise/hk ([e977b42](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e977b42a61695ae738f7f2d755c3271cf4588e98))
* Move prettier from trunk to mise/hk ([3d01ebf](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3d01ebfb63115f6728e355740475685f945c1e34))
* Move ruff from trunk to mise/hk ([ad9afac](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ad9afac53bcaa1c4958ed3f7fc8f5f805eb73734))
* Move taplo from trunk to mise/hk ([41fbb7b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/41fbb7b14020b6ecf6aa2665c380145387d7cdce))
* Remove last pieces of trunk ([d33fcae](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d33fcaee9daba08b6fb5cc0b967e38a0b29ca26f))
* Remove prettier ([4b57064](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4b570645c64e4dbdbd6498c52cac5d2b5ae45fbd))
* Replace commitlint/cli with committed ([e3e7bb9](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e3e7bb967b13d52d9568c0cc9f7666cbc0b9ac53))
* Replace markdownlint-cli2 with mado ([999e42e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/999e42eea0c44d2616f43e2db55392b72f530a45))
* Restructure yaml linting & hk config ([8603808](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/860380840f930c368f6c43e6b6b857b3a426005e))
* Switch cspell to typos ([b279020](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b2790203c6f141f566abe7b05d8e3638199d7ae8))
* Switch from markdown-link-checker to lychee ([e1359ae](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e1359ae6aebb251a41389db4d7e777d24b789e21))
* Switch mise to use bun for npm ([97b4a9a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/97b4a9a5631753ed16b8cca374a4dd12162a7f1b))
* Update committed settings ([735c445](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/735c445a0fdbb19ec66007ba16d9f99420579548))


### Bug Fixes

* Adjust pr testing ([155b0e5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/155b0e52a65abb6b58e7c23785d7159c99663aa5))
* Cross-platform pkl linting ([41ed286](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/41ed2868cbf5e2d5f6b00c73d448f9e24c0de54f))
* Fix git hook setup task ([c65867e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c65867efca488a26cb29ef94b23c6fdcda36544f))
* Fix markdown linting ([f035773](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f035773c8e4aa1678321c58d98767775a9359599))
* Fix mise in template ([a01854f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a01854f63f726c49617ca8cf494057ab24840ac6))
* Fix prettier settings in template ([808600a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/808600a6fc25518196cb3acda0f0082a36d08701))
* Fix vscode extensions and settings ([2b6e3b6](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2b6e3b6a7697723ab6f0eee4560c49893e2a8680))
* Fix yamllint vscode config ([b50c0a1](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b50c0a163800f08388dd3956150760dcccace0e0))
* Remove requirements from non-template children ([4b24598](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4b2459838099da9fba6a00d267cf31558dae9a24))
* Set up mise to work properly in CI ([b2b9e43](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b2b9e43e42bef65a7a8897ae5420cfebbf11b5d0))


### Miscellaneous

* Add versionrc to dictionary ([3885196](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3885196026451fe87b6883c6adca68cbe09983a1))
* **deps:** Update dependency copier to v9.7.1 ([f01eca7](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f01eca7d5f136235fd1713a96e587706ba73e65d))
* **deps:** Update dependency copier to v9.7.1 ([f10523a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f10523a586315aa656add2137d43c4eccedff158))
* **deps:** Update dependency copier-templates-extensions to v0.3.1 ([2f19967](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2f19967315b924d7dd3a54ede5d8bc4188dddcad))
* **deps:** Update dependency copier-templates-extensions to v0.3.1 ([17e2c66](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/17e2c6625ba5b998e23f82000a19666a98624a13))
* **deps:** Update dependency githubkit to v0.12.13 ([0db47a4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0db47a48b9793781b58419dc9064b99ff1930277))
* **deps:** Update dependency githubkit to v0.12.13 ([a8405fc](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a8405fc3127cac8ba52a4a6205cd86db7c291e31))
* **deps:** Update dependency jinja2-shell-extension to v2.1.1 ([3f1ada1](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3f1ada1dd7d2f92a400e7dd6c8e792ca92ad6925))
* **deps:** Update dependency jinja2-shell-extension to v2.1.1 ([2948f2c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2948f2c7be0ad4fe1b212b8383ac2f5fa304a38f))
* **deps:** Update dependency pipx:yamlfix to v1.17.0 ([22505f8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/22505f8fd58d397373251062d7bf10a1fa6ac856))
* **deps:** Update dependency pipx:yamlfix to v1.17.0 ([82d617d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/82d617dc9c084be4816bb26858e51303f59d1532))
* **deps:** Update dependency rich to v14 ([4c9a7ef](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4c9a7efc1c602cd7ba97396e6e19571ef5c8c078))
* **deps:** Update dependency rich to v14 ([75a5725](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/75a5725714fb4125e372892afe30e8293fabbbd6))
* **deps:** Update yamlfix in template ([5db60ea](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5db60ea1982ace75e0704414e31184fd743e17e1))
* Remove cruft ([ad2f03d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ad2f03dde900b1414a55d455e717a9f64595dfd2))

## [0.3.37](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.36...v0.3.37) (2025-01-09)


### Features

* Improve logging for azure pipeline creation ([f6244c4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f6244c4d893dbb97059fa40cac2730c54bcfc02e))
* Overhaul trunk linters ([4d4f485](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4d4f4852d55c100a9f14e013db4e20304c002507))
* Update cspell words ([6129917](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/61299171d516c1214f618969455434ee9c2a7c8e))

## [0.3.36](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.35...v0.3.36) (2025-01-09)


### Features

* Improve repo_actions help ([1e7f854](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1e7f8541acc1962b1e3c845c633fb478b5563957))


### Bug Fixes

* Fix azdo_org question ([7887895](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7887895d9dd069d3ba5d96c0db2b3f71596849b7))

## [0.3.35](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.34...v0.3.35) (2025-01-09)


### Features

* Add repo_actions validators ([1736b3f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1736b3f7f97ec13617c8eadc17213aca9338a661))

## [0.3.34](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.33...v0.3.34) (2025-01-09)


### Features

* Copier update to parent template v0.3.33 ([ed5ed64](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ed5ed6402ed11e35816657f9c9f7b6faf96f46cc))


### Bug Fixes

* Fix credential file creation ([0bbd0f3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0bbd0f33aeaebe529a4e221311af5a8780f55752))

## [0.3.33](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.32...v0.3.33) (2025-01-09)


### Features

* Improve question help ([4fc9be2](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4fc9be2ad612a4e1cf6a11be780f47adfb0555a2))

## [0.3.32](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.31...v0.3.32) (2025-01-09)


### Bug Fixes

* Fix other yaml validity issue ([3dd58f8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3dd58f8a3371756aee49e8eede3f6a25f3e96e99))
* Fix yaml validity issue ([d6f8ed4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d6f8ed4803f88bab35843c22205d8cf913858ea2))

## [0.3.31](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.30...v0.3.31) (2025-01-09)


### Features

* Improve structure of questions ([a40f7ab](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a40f7abd1db3f860708daafd52a2b29eaf74117b))

## [0.3.30](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.29...v0.3.30) (2025-01-09)


### Bug Fixes

* Fix path extension copies ([db5ba3c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/db5ba3c2e992623b45d1d177e7ec6795c8fbee5a))

## [0.3.29](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.28...v0.3.29) (2025-01-09)


### Bug Fixes

* Refactor cwd_name function ([008cb79](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/008cb79e34cc2428b404f7419cf75ebc52be0b72))

## [0.3.28](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.27...v0.3.28) (2025-01-09)


### Bug Fixes

* Fix bad extensions definition ([7f06478](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7f06478bdf62b056ece2ee856f056060312b90cc))

## [0.3.27](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.26...v0.3.27) (2025-01-09)


### Bug Fixes

* Fix cwd_name ([e69bf2f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e69bf2f995a2d2c901e214fd106eacf9c8919912))

## [0.3.26](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.25...v0.3.26) (2025-01-09)


### Features

* Move repo name question first ([d19a289](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d19a289ed4a19429810b315074a8ee8916e2b36b))

## [0.3.25](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.24...v0.3.25) (2025-01-09)


### Bug Fixes

* Fix cwd_name function ([84c5215](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/84c521524a91352cb9da1bd06fd15a83895a9167))

## [0.3.24](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.23...v0.3.24) (2025-01-09)


### Features

* Copier update to parent template v0.3.23 ([5d5c0ee](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5d5c0eebb0c5278d6cc3bb602eb24e3124538ddb))


### Miscellaneous

* **deps:** Update ghcr.io/natescherer/postmodern-tools-container:latest docker digest to f56e2b1 ([18587e1](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/18587e19870503b0b7174b9734b78af413e1c559))

## [0.3.23](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.22...v0.3.23) (2025-01-09)


### Features

* Add default for repo_name question ([29dbfa9](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/29dbfa940396d167cb8570690c8703050131b84a))
* Copier update to parent template v0.3.22 ([e70de2c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e70de2cb0aa47b232a04daf336a46f37f6994e3e))

## [0.3.22](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.21...v0.3.22) (2025-01-09)


### Bug Fixes

* Fix template devcontainer.json ([0ac2f81](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0ac2f8143148c2d2efdb769d802f9395090a7f69))

## [0.3.21](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.20...v0.3.21) (2025-01-09)


### Bug Fixes

* Disable pinning for devcontainer features ([6825179](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/68251792e2050c95be6ff20a5a53df30618e55fd))
* Fix copier update workflow ([#462](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/462)) ([e3fe6f6](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e3fe6f6a55859eb8afbd4ec15b0fdab488ff1365))
* Make release please config a template ([9e0b7e2](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9e0b7e259dfbf5605afded37e81e8f7037581522))

## [0.3.20](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.19...v0.3.20) (2025-01-08)


### Features

* Copier update to parent template v0.3.19 ([2e20189](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2e201894737590759b186f5c978ad76a953ef2a4))
* Update release please config to include chores ([f48a6d5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f48a6d5066f9c464b6511a9e6543c772eba3c091))
* Use postmodern-tools-container ([1afe85b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1afe85bc9d8191d89cb6c34153d2999056ac35e2))


### Miscellaneous

* **deps:** Pin dependencies ([63c51a4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/63c51a400648dcc3b779f2ddb4b32afe58392274))
* Fix merge conflict ([44d0d09](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/44d0d099e9dfa3b838009ceb1040738cc77ea024))

## [0.3.19](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.18...v0.3.19) (2024-12-31)


### Features

* Have release please run with pat ([4a65522](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4a655228a5ad797c794fc65416af34a67e02c892))

## [0.3.18](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.17...v0.3.18) (2024-12-31)


### Features

* Copier update to parent template v0.3.17 ([9e43de8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9e43de88470df98e33c6058f2937c7929cef28b2))

## [0.3.17](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.16...v0.3.17) (2024-12-31)


### Features

* Add infisical to cspell dictionary ([c9686ab](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c9686ab0e1be97d1eb80360eba0cac1b08c102e9))
* Switch to using REPO_MAINTENANCE_PAT secret ([dedc2f7](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/dedc2f758432c8a69d68580ea064e313a032c9a6))

## [0.3.16](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.15...v0.3.16) (2024-12-31)


### Features

* Copier update to parent template v0.3.15 ([e6e1e32](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e6e1e32e4d8cf2ff2d51980562b37d933b2ce332))
* Update cron schedules for workflows ([8c6fffc](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8c6fffceadbf54bd5a52c5e4a4577814877bd02b))

## [0.3.15](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.14...v0.3.15) (2024-12-31)


### Features

* Copier update to parent template v0.3.14 ([fbd41ba](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/fbd41baa94238dedea701e0e5ae415953e14c2ac))


### Bug Fixes

* Fix os.getenv ([2a6f711](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2a6f7115fb3297a1c4da7e64ab2a634510e4ed82))

## [0.3.14](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.13...v0.3.14) (2024-12-31)


### Features

* Add workflow for upgrading trunk ([b64ca97](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b64ca9774d35f9e9da9f9a568cb7f93fa2018f31))


### Bug Fixes

* Fix naming of trunk upgrade prs ([531e451](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/531e45130369a879aef06fae6f5d3ea2ea120023))
* Fix repo creation credential setting ([21eae37](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/21eae37023af83ad1bd53c24ccc7e645f8477d2b))
* Fix trunk testing for prs ([91cc9bb](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/91cc9bb57e8fd354cce082cf8243ea745645c7f0))
* Fix trunk workflows ([4ece49e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4ece49e693841c3a694b0faf3021b065603661a4))
* Force pr tests to save trunk annotations ([217e1bb](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/217e1bb20dd5c6be11057deb7065446f3bbb9acb))
* Update trunk check workflows ([f585c7d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f585c7d8b0cbcb3817f267452b7273e91a07ccb6))

## [0.3.13](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.12...v0.3.13) (2024-12-31)


### Bug Fixes

* Actually fix trunk for prs ([d768c98](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d768c9877dcc557911fad61fedc69bdc0a50f3b4))
* Fix checkout action version ([65e2300](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/65e23004a70df2f83ddd5e136976ad587bc3cc57))
* Fix trunk testing on PRs ([75abbfb](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/75abbfb27a4ec0a80d83c758fc8014e8e3a4ebc3))

## [0.3.12](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.11...v0.3.12) (2024-12-31)


### Bug Fixes

* Disable renovate dependency dashboard ([51c941f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/51c941f5ae5efc3265e5038dae6575857b02d42b))
* Fix bad jinja syntax ([5517bbb](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5517bbbf917e6c4714e629fa063198635bf8303e))

## [0.3.11](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.10...v0.3.11) (2024-12-31)


### Features

* Add renovate config to downstream templates ([2eef993](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2eef9932ab471b84ba71f2039dbdd9e5fc572c32))

## [0.3.10](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.9...v0.3.10) (2024-12-31)


### Features

* Copier update to parent template v0.3.9 ([3f93ecf](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3f93ecf5ecd262fced63c50073ea8078274773ab))
* Restore devcontainer template ([a979d80](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a979d80bfaf0143bc721c7344e5625c1a061ebaa))
* Switch to renovate from dependabot ([ba81a3e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ba81a3e3eb18e9698908d3d27aed98fdddd1ad77))


### Bug Fixes

* Fix devcontainer fileMatch ([61d17da](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/61d17daf9a8befea1b5a12b1326336ddfd16c77a))
* Fix handling of renovate and azure pipelines version numbers ([9b2de06](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9b2de06517204be027f45f53dc9541869fe2e571))
* Fix renovate config ([f1f3b1f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f1f3b1f5ccd5001d77947703399e0f02bf932278))
* Fix version number for trunk ([b2de10b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b2de10bac0b7a5ba86cf088dd25d3c9e83e1a6b1))
* Restore devcontainer json ([f2977b7](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f2977b7045d6b296230bcc71562b0a36b1ffdd83))
* Switch renovate config to json5 ([7f1a6fb](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7f1a6fbff025a51764e3710c73a346ce842997b2))
* Update devcontainer files for renovate compatibility ([3ee8163](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3ee816363930e884cca0b1a3d8fac88e4916eb1c))

## [0.3.9](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.8...v0.3.9) (2024-11-04)


### Bug Fixes

* Don't use encoded git tokens ([4451416](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4451416fc31245e9ac285cc1362b99252b4ba219))

## [0.3.8](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.7...v0.3.8) (2024-11-04)


### Bug Fixes

* Fix git cred file path ([bc3f06a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/bc3f06a518e5fdaf64a6b23b41fdcb60004eaa1b))

## [0.3.7](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.6...v0.3.7) (2024-11-04)


### Bug Fixes

* Fix open mode for credential file ([1994441](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/19944413cfc84c78863dec33a83ad7ea2109b451))

## [0.3.6](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.5...v0.3.6) (2024-11-04)


### Features

* Add cred handling for docker ([f03b4fd](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f03b4fd3ed2cbe27ea3ecd11c6a89ce2b82e8d9c))
* Apply parent template v0.3.5 ([6dcc9eb](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6dcc9eb7f314deeb11ad91d290f5476f0d332a8c))


### Bug Fixes

* Fix yaml formatting on azdo cron schedule ([414a245](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/414a2455afd11a87187d1ba6176f1ba0f3b04521))

## [0.3.5](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.4...v0.3.5) (2024-11-01)


### Features

* Add copier update workflow for Azure DevOps ([b448721](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b448721e261fd165ccb09f0dec016b42e05ac928))

## [0.3.4](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.3...v0.3.4) (2024-11-01)


### Bug Fixes

* Fix payload for azdo pipeline creation ([ee2ddf7](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ee2ddf7212ab62b420bf7579086d28b15d183352))

## [0.3.3](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.2...v0.3.3) (2024-11-01)


### Bug Fixes

* Fix pipeline naming for azdo ([9a00ce8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9a00ce8ff7a0738b766c6c4465724b891af664a2))

## [0.3.2](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.1...v0.3.2) (2024-11-01)


### Features

* Add vscode associations for azure pipelines ([5162a29](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5162a29a93cdba7d4d4c769e5b8095135696b5bd))
* Allow create_pipelines_azdo task to dynamically register multiple pipelines ([0ab6b1d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0ab6b1d3904939f611a03bb23838e1e5bac71d17))
* Copier update to parent template v0.3.1 ([0c85845](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0c8584504f07a095b7da969dfe9c98fe183d0143))

## [0.3.1](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.3.0...v0.3.1) (2024-11-01)


### Features

* Apply parent template v0.3.0 ([f0fcc6f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f0fcc6f4089f30257266dd1bb4531e3c9fa9b050))
* Improve azdo release pipeline ([4c75e72](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4c75e7206ad82238e46bcd162db656ad614f6817))


### Bug Fixes

* Port azdo workflow improvements from test repo ([983558d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/983558d35c163d2a841c79eb6b82ab46327c23af))

## [0.3.0](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.47...v0.3.0) (2024-10-23)


### ⚠ BREAKING CHANGES

* all-contributors and dependabot PRs will no longer automatically merge

### Features

* Remove automerge workflow on PRs ([653d9dc](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/653d9dcb31ad566651a65b49ae061b0764df04b5))


### Bug Fixes

* Fix formatting issues in template ([2cf9df2](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2cf9df23ef6f243f6df539a30b54d3d9475bfe74))

## [0.2.47](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.46...v0.2.47) (2024-10-23)


### Features

* Copier update to parent template v0.2.46 ([34f31fe](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/34f31fe6bf1c5ff9242ad2debfba58304ec8cc63))


### Bug Fixes

* Don't create public workflows for private gh repos ([c4279da](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c4279da97e8804e33567b7bdaf016690ea985f08))
* Fix trunk check prs (closes [#316](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/316)) ([0191943](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0191943b9e2bad400a22d83ab240c77d42c2bfe9))

## [0.2.46](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.45...v0.2.46) (2024-10-23)


### Features

* Copier update to parent template v0.2.45 ([9b169fe](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9b169fe08a7830c5b623843f5d6a1fab690e4e4a))


### Bug Fixes

* Fix extension recs in template ([7fe3770](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7fe3770f597a695a5ee6188f742134241091632d))

## [0.2.45](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.44...v0.2.45) (2024-10-18)


### Bug Fixes

* Add extension definition ([1fc1b1e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1fc1b1e1530b2ee15320c92295fa45e67e05cb68))

## [0.2.44](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.43...v0.2.44) (2024-10-18)


### Bug Fixes

* Add missing extension file ([f1ec90c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f1ec90c17517917d0de274783a73c1e17b016353))

## [0.2.43](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.42...v0.2.43) (2024-10-18)


### Features

* Copier update to parent template v0.2.42 ([83bca46](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/83bca468e57852fd5678b1df5d30de4feb61cf26))


### Bug Fixes

* Make parent_template_name question input-safe ([a32c6b3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a32c6b3fe6fcfdebc51d268100132a36b77c2ebb))

## [0.2.42](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.41...v0.2.42) (2024-10-18)


### Features

* Add scherer back into cspell words ([8e8d625](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8e8d62581bc83b9c6a2db646a7a3f8433a9c8c45))
* Apply linting updates from trunk ([0ed8a98](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0ed8a9807320dd29f19d91967438e5709a75eb47))
* Copier update to parent template v0.2.41 ([9d15582](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9d15582b0514802a2542dfbefb6607e9bfb7fb71))
* Improve spell checking ([5942041](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/59420419134ee9a24a93ed0ca35572c95d5af012))
* Update trunk, cspell, and ruff ([500e594](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/500e59419306ec93d0cc358700456a908231c9a1))

## [0.2.41](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.40...v0.2.41) (2024-10-18)


### Bug Fixes

* Ensure CHANGELOG.md exists for created projects so trunk doesn't error out ([b5e3048](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b5e304881a81cdfad3bd4be6064d3157727b3afd))
* Fix yamllint config for templates ([4a472e8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4a472e83fe0ba0c3a0d69386ad24cd4bd7369662))

## [0.2.40](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.39...v0.2.40) (2024-10-13)


### Features

* Replace bash dict with shell dict in cspell config ([f6bb0a2](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f6bb0a2c1b6ebf7ae86caef6bdfb1caf09aa3961))


### Bug Fixes

* Clean up template to not deploy template-only settings for regular projects ([b696349](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b696349e1526e256a44d674a93ec004b17692b87))

## [0.2.39](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.38...v0.2.39) (2024-10-12)


### Features

* Copier update to parent template v0.2.38 ([204dfdd](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/204dfdd22ee9d66b1e7ebfaab66d57ebfa58553c))


### Bug Fixes

* Only use actionlint on github projects ([37dce71](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/37dce71701ce3a862d6065bdefb3cf3628c79a8d))

## [0.2.38](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.37...v0.2.38) (2024-10-12)


### Features

* Copier update to parent template v0.2.37 ([b71857c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b71857cc0f65d399a3776955480888b5c503bdcf))
* Remove unneeded node feature ([5937100](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/59371005dc9315ed3c5c2a3fc45f3426e48bb9c8))

## [0.2.37](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.36...v0.2.37) (2024-10-12)


### Bug Fixes

* Fix dynamic plugin logic ([4c9e37c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4c9e37c7ff60d05aed6eca2aa9bc507021708454))

## [0.2.36](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.35...v0.2.36) (2024-10-12)


### Features

* Copier update to parent template v0.2.35 ([910e011](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/910e011a8ab6dfe1ac75eba0d7b4f04625206cce))
* Make plugins dynamic ([70d2070](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/70d2070500ea4e5df45963f7e7cca91e5677a9c3))


### Bug Fixes

* Add natescherer back to cspell ([fd466ba](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/fd466ba060f73add8fdc1b9ebf63c33e23b3ad9a))

## [0.2.35](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.34...v0.2.35) (2024-10-12)


### Features

* Update cspell settings ([49c2825](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/49c282580bf5a5395652e59bf2881e54d92f4432))
* Update trunk ([792b08e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/792b08eb800cb01406a41c15b8919440f50f7b25))


### Bug Fixes

* Fix devcontainer home mount ([1e58765](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1e58765afd7eae8a1d1525c342551a44a414f722))

## [0.2.34](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.33...v0.2.34) (2024-10-12)


### Features

* Add built-in slugify extension (closes [#300](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/300)) ([9feadb5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9feadb5b1f1463b7c0f3c0a0f89c8449bc935d4d))
* Copier update to parent template v0.2.33 ([b03ee51](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b03ee51865cde019b0af3cf615f8f523535d9e6b))

## [0.2.33](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.32...v0.2.33) (2024-10-12)


### Bug Fixes

* Fix copier update workflow formatting ([eab7839](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/eab78391cf3fadf12d1e753a6c350707aef28129))

## [0.2.32](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.31...v0.2.32) (2024-10-12)


### Bug Fixes

* Fix NEW_VERSION calculation in copier update workflow ([5ee3e2d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5ee3e2d37932ffedd5a94787a8fccd289e5bbfd1))

## [0.2.31](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.30...v0.2.31) (2024-10-12)


### Bug Fixes

* Fix branch name ([064f75a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/064f75a568121a7ced480054948ce08a85c9d9f1))

## [0.2.30](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.29...v0.2.30) (2024-10-12)


### Features

* Fix mount permission issues on windows hosts ([0d12cc9](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0d12cc901cbc7e7240fec8039f281cc819b2dc63))
* Improve template update workflow ([0a497ff](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0a497ff28abded831b80a81fe9b52d982db7434e))

## [0.2.29](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.28...v0.2.29) (2024-10-12)


### Bug Fixes

* Update base image in template ([e75ca21](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e75ca2103b98cb074d30b20d5ff875cf9c9bbabb))

## [0.2.28](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.27...v0.2.28) (2024-10-12)


### Features

* Bump devcontainer base image ([9ff6950](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9ff695093c16b44517bc68b2b5127e4e772dc049))

## [0.2.27](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.26...v0.2.27) (2024-09-25)


### Features

* Add more cSpell dictionaries ([a3e81c5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a3e81c5aebe17468e480f08db1c50b06249a8852))

## [0.2.26](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.25...v0.2.26) (2024-09-25)


### Bug Fixes

* Fix readme format ([d2a84c1](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d2a84c1ed0b1785c615a3080ba71a8c18c1e15c5))

## [0.2.25](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.24...v0.2.25) (2024-09-25)


### Bug Fixes

* Fix formatting issues from downstream ([e6d899a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e6d899aecba8ab0afe8bd751d759028196382766))

## [0.2.24](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.23...v0.2.24) (2024-09-25)


### Bug Fixes

* Fix versionrc formatting ([e20724c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e20724c9200fbacaad6bb1da2e572ea0fa3cfcfd))

## [0.2.23](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.22...v0.2.23) (2024-09-25)


### Bug Fixes

* Fix readme formatting ([69a1bbd](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/69a1bbdd0e6fac30c4dd86765481b135072ef76f))

## [0.2.22](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.21...v0.2.22) (2024-09-25)


### Bug Fixes

* Fix formatting issues found downstream ([838a5db](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/838a5db116de3f4b85423711c75f3a0bdfa37c7a))

## [0.2.21](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.20...v0.2.21) (2024-09-25)


### Bug Fixes

* Dynamic trunk ignores ([4e01eb9](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4e01eb9a6fd53a58fc818bcbcd696486db5c93f3))

## [0.2.20](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.19...v0.2.20) (2024-09-25)


### Features

* Apply parent template v0.2.19 ([199bef3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/199bef320336cc67d2ca20d7ffbe305cbf5b01b5))

## [0.2.19](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.18...v0.2.19) (2024-09-25)


### Bug Fixes

* Bump minimum copier version ([2d0bd03](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2d0bd030c337f10bf66a584df55d1cd19c7bb4e5))

## [0.2.18](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.17...v0.2.18) (2024-09-25)


### Features

* Skip linting/formatting on release please manifest ([8eae6f3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8eae6f34b2c30fa6b5f9a51fc768b372714f6dc6))

## [0.2.17](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.16...v0.2.17) (2024-09-25)


### Bug Fixes

* Fix release please formatting ([32b0c7a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/32b0c7af654dde897639b2b343d46a11a76cb5d1))

## [0.2.16](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.15...v0.2.16) (2024-09-25)


### Features

* Add pscore to dictionary ([ec0d937](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ec0d937d3cf22e7306546dae6238144772d63e02))

## [0.2.15](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.14...v0.2.15) (2024-09-25)


### Bug Fixes

* Fix link format ([f98121a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f98121aec0c2dff73e300af21de57df6404fe133))

## [0.2.14](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.13...v0.2.14) (2024-09-25)


### Features

* Apply v0.2.13 ([f81b0b9](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f81b0b929d71fb48cebfff1efa9498bc636ca600))
* Improve formatting ([f3cf8f3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f3cf8f3875334edf342ca8eaf305f08b8bd474a1))

## [0.2.13](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.12...v0.2.13) (2024-09-25)


### Bug Fixes

* Fix readme formatting ([e6fdd30](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e6fdd30d86a9b6df82cc3d585e59a4911997c271))

## [0.2.12](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.11...v0.2.12) (2024-09-25)


### Bug Fixes

* Fix doc templates ([f3227c3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f3227c3ce605cf37665346240f335ee596fbee1c))

## [0.2.11](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.10...v0.2.11) (2024-09-25)


### Bug Fixes

* Remove unneeded ignore ([5425d18](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5425d18c8db7d9a3a69342ad77e554aa2f8e774c))

## [0.2.10](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.9...v0.2.10) (2024-09-25)


### Bug Fixes

* Fix bad formatting on dependabot template ([e00510c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e00510c21d3e3c6f21dbddc1b350ff973804d782))

## [0.2.9](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.8...v0.2.9) (2024-09-25)


### Features

* Add dependabot grouping (closes [#6](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/6)) ([6dee4bb](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6dee4bb415f7c52e6d5b937fcb223541165215e1))
* Add devcontainers to dependabot (closes [#8](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/8)) ([298ffe7](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/298ffe717e0812062b5a332efe7e55a70f26a8aa))


### Bug Fixes

* Add commitlint config to template ([3f2684b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3f2684be64b974f11ba100955efb517cafe75d83))
* Fix yaml format ([9cb2bb8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9cb2bb87cbcd04938e45769f8d9955f5597c9358))

## [0.2.8](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.7...v0.2.8) (2024-09-25)


### Features

* Add toml vscode plugin ([ed3c986](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ed3c986e4949c52e886e3a884186025a0c7a91fa))

## [0.2.7](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.6...v0.2.7) (2024-09-25)


### Features

* Apply parent template v0.2.6 ([30796a4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/30796a4ef1ff154cebd409ff3b540f8b697daefd))


### Bug Fixes

* Fix trunk nits ([49f36bc](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/49f36bc981cd1d1aa6b516cee7c869ad956a94eb))

## [0.2.6](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.5...v0.2.6) (2024-09-25)


### Bug Fixes

* Fix jinja conditionals ([8144c49](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8144c498beb7826f2be9e283767ce322760c55b8))

## [0.2.5](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.4...v0.2.5) (2024-09-25)


### Features

* Remove unneeded workflows ([17a5a4a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/17a5a4ac6e8675eb5992c13cf2f28d8d4a50333e))


### Bug Fixes

* Fix task conditionals in root copier.yml ([cdc3d4c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/cdc3d4c89e9653da714c8767f4d2147a5e17dab4))

## [0.2.4](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.3...v0.2.4) (2024-09-25)


### Bug Fixes

* Fix conditionals on copier tasks ([5d7baad](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5d7baad1154b7ad2ce532503c7ea7e8a055fbc21))

## [0.2.3](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.2...v0.2.3) (2024-09-25)


### Features

* Apply trunk quality and formatting ([cb66c16](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/cb66c165720a4f6e5cc9f2942c7f3a4f4a3112a0))
* Change devcontainer mount (closes [#211](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/211)) ([78e3353](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/78e335346322ba10d9df5202122287c4ee808154))
* Implement trunk ([e711206](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e711206352ae9fdc9f792a3cb6eb88a117ee6366))

## [0.2.2](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.1...v0.2.2) (2024-09-24)


### Features

* Ensure devcontainer folder is made for all projects ([e5ae1c7](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e5ae1c7dd6014bc8f78c371735fd0c78eb7eb5b9))

## [0.2.1](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.2.0...v0.2.1) (2024-09-24)


### Features

* Update vscode extensions ([5e46c4f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5e46c4f186f7c580c4562e8821edb8f483e51b90))


### Bug Fixes

* Fix license file ([6fc1d10](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6fc1d10c628cc1843abd7e55ac0dc31dbf8847fe))
* Fix pull request ruleset settings (closes [#221](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/221)) ([f882058](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f882058927b4b73c437857fd1f2814bd23aab3cf))

## [0.2.0](https://github.com/natescherer/postmodern-repo-copiertemplate/compare/v0.0.1...v0.2.0) (2024-09-23)


### ⚠ BREAKING CHANGES

* overhaul release system
* replace GitVersion with commit-and-tag-version

### Features

* Add azdo pipeline creation ([c6b3da5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c6b3da5a9ec0fc0fca3f9e02d7920584816e2114))
* Add better azdo pipeline formatting ([dd465ec](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/dd465ecb90a16ca7d85327e18723555e6a42ad8d))
* Add dynamic repo urls in doc ([9effa48](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9effa4833eef52d712d98e8120589398e63ddec2))
* Add inherited variables into child templates ([d3a7411](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d3a7411d6b8dada247815257b74921f42e95b448))
* Add management of project lifecycle ([3f17f03](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3f17f0352d33310d531e6d29fec9b5367ebcb00f))
* Add question override file for child templates ([7e6b661](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7e6b6610730a7124545ccee10e575c30071e8d54))
* Add support for conventional changelog ([03fdfd2](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/03fdfd22be9cc009a35b161acd6653dab8272a08))
* Add template files rename task ([0d61af6](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0d61af6b3cce67d7db6f4b331c0f708e639de323))
* Add template release pipeline for azure devops ([457e017](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/457e01721d3aa4c4edbae204425bb2b647210880))
* Add thumbs.db to .gitignore ([1a73021](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1a730219fc7ccc4a4b2601fb3f65de5e54574dd9))
* Core template functionality ([#10](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/10)) ([e3a0895](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e3a089575ea3037f72d683990e71c43842ea9ae6))
* Fix tasks names ([6cff855](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6cff855bc803195141ccbe0dfd56793c7cab1fb0))
* Make template inheritance links dynamic ([5619a1f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5619a1ffb41df98b815076622dfdfbc153e84598))
* Overhaul release system ([4b2c677](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4b2c677bde7c0dcbc27bc956de6b35d0cf0742ec))
* Remove unneeded pre-render functions ([dac3564](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/dac3564aaaedf7ec07b7710d33f786bd5c5b0909))
* Replace GitVersion with commit-and-tag-version ([0b8d9e6](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0b8d9e64325e7b68df6a055c4f5d20593b2e0380))
* Restructure azure devops extensions ([c1905f5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c1905f58427e492558007c90bc1da5615c26129f))
* Switch to using tarball for template copy ([b31fbf7](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b31fbf7d38f6921c36a5ae3e21055ecbb4afe8f2))
* Synchronize files from outside template into template ([90ac90e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/90ac90eac9771c86b783bb83a648d9c7f55802ab))


### Bug Fixes

* Actually fix azdo parserOpts in versionrc.json ([11f594f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/11f594fce237ea3babae1fc0a38f665b098822ba))
* Add dummy question to override file ([3999006](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3999006b3ca1a813fc99a88b92a92d213b78d8c6))
* Add new copying method to template template release workflow ([dc0219f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/dc0219f77567df2a3aa0291737569f5b3d707268))
* Add part 1 of new renaming subtemplate policy ([8c78a83](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8c78a833c0a6738317b9bfc2774c29d7edd8ba83))
* Add permissions for workflows to commit ([#15](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/15)) ([39563ee](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/39563eeab6a564def3691b2f6e5b06201f5807c9))
* Add release please manifest ([9d46d52](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9d46d52a37ef5a2023254709ce770488239c5d68))
* Adjust tarball creation ([f2b2ec3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f2b2ec34227249797e628b7dbc0ed4c56447a2b1))
* Allow workflows to create PRs ([#16](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/16)) ([4b0a675](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4b0a67519a8a91416d6bee523f0ea83cb0512223))
* Attempt two at subtemplate copy fix ([7a22bce](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7a22bceea26bddc4b3004b097af34e70d4e3d423))
* Azdo pipeline autocommit message formatting ([ebb4d12](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ebb4d12b5aae4ca7434bf07630a183bb4542dbfe))
* Azdo subtemplate generation ([cba0f5d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/cba0f5d4bc504ac02b42724f68d6f4f7c01bdaaa))
* Bad azdo release indent ([72240ad](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/72240ade430fe468b2611838162461580bcf592f))
* Bad indentation in copier.yml tasks ([1b7805d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1b7805d3c646533cdd11d40bb12d65bf168e773e))
* Bad template subtemplate generation ([5eea927](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5eea927831dbf3967ce0cecbd78ff37acf02111b))
* Bad url construction for azdo projects with spaces ([46c312f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/46c312f02abe25ad9d53118395506d80d5af19da))
* Change commenting to fix copier.yml ([9b436dc](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9b436dc06cda5f2e0ff50b4a27448b12a928e990))
* Change how folders are renamed ([cc7f93c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/cc7f93c8ab05744ede611e51eb4f5633f2058245))
* Copier tasks ([3de8164](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3de8164edb9cca5df116b5cfceabd482b1ff7180))
* Copier.yml when statements ([00509c5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/00509c541b415a78c543492422025f9b1e964d5e))
* Copier.yml whitespace ([7f295c1](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7f295c190fc9b242a5443fe973e9e367ae5d6ff3))
* Don't commit 'template_copy.zip' to git ([7ce077a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7ce077af06038e402771a50f9f813653ed3214e5))
* Ensure get-childitem returns all items ([35538db](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/35538dbd049ebe28d1229cf4a97514727fe1dfb2))
* Ensure hidden files are processed for subtemplate rename ([e746644](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e7466446a3f796ee29daf6e5dd7ff1cebf7565ee))
* Ensure tasks.py exists for Standard project types ([f13c9aa](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f13c9aa84e855bd3562f1ded558c6271bc3cee60))
* Escape square bracket for pwsh ([127fdd2](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/127fdd2b15f0a5e627a8bdfe8fe70195c699b514))
* Escape azdo projects with spaces ([ef90cab](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ef90cab7f7eebf6a574e10d4e679b0ad3702da84))
* Fix azdo repo creation ([05de222](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/05de2225dc22b6467c96d4e27eccbb952ccfc380))
* Fix deletion of subtemplate directory ([b88f147](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b88f14792535801105337d2fc76628d5fb4a4eea))
* Fix formatting in README files ([9f2f70f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9f2f70f1dd10a581a1c84f8c3478b27efc74526a))
* Fix include formatting everywhere ([6166dc9](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6166dc93c4aac21046d78a3b00f4994cf5754fc9))
* Fix params for move-item ([8d8fc78](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8d8fc78ea3c27e0ba65e5ee1fc08804332ebd8fe))
* Fix release note generation ([a85ba7d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a85ba7d9a35e7968bdda16179328e17c019595b6))
* Fix rename-template-files task root path ([a93a7a9](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a93a7a91d6db0cc3211691961e9f94492911b2b5))
* Fix run statements and jinja formatting in workflows ([3bf93d3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3bf93d37af110e994cc3ead7001f9a4fcd87a781))
* Fix subtemplate renaming ([c028785](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c0287852ab1dfdd669a028a54067df524b9b4cd1))
* Fix template release workflow ([b3933db](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b3933db475a7f6a6dc9ff4dde92b040d818cc557))
* Fix typo ([8dc6980](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8dc69806b508ed9f153772c62ac0dc86312923cd))
* Fix typo in deleted-unneeded-template-files task name ([a7723ba](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a7723baf817ea24fb0831b29c174e755bad55e32))
* Force pwsh renames ([8755220](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8755220a88109a9c484564d35d76e00b63675c62))
* Formatting of copier.yml include ([946b1dc](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/946b1dc5275098a78909f3edadda7be90f171e07))
* Have rename-template-files step overwrite files ([3fbb72e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3fbb72eba151e6617be86bb233a7f13acfecad80))
* Have tarball deletion fail gracefully ([37c287e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/37c287e9072b5efc725caf2145f48a5c5b568b7a))
* Improve whitespace formatting in READMEs ([0800040](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0800040af6e9a1e55fc042a288c7aa25842690fb))
* Is_prerelease value typo ([80679cf](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/80679cf572c2ae36a3326ee34287f790be49893a))
* Jinja escaping in gh release workflows ([3582ed7](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3582ed7bdef9a6d4107cb6f741e4f5d90ffa7891))
* Lifecycle question in copier.yml ([e86fc4c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e86fc4c42e8b0a83154eb798ad84b1542480aab4))
* Make is_prerelease not prompt user ([5063c13](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5063c132c24390e3ee282fbd6c84ebd13bb0bb9e))
* Only create labels if they don't already exist ([79ac9ff](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/79ac9ff6cad0f3c352760f7e424f6e133c75b96a))
* Only have rename-template-files task alter files in template and not subtemplate ([fdd75d3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/fdd75d3cce499204a6f21dcca313d9137b038a60))
* Prepare for new release ([851e7d3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/851e7d30900627ad7e6103c8cd8ffb4d66b40f94))
* Project name in template README ([ad5eea2](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ad5eea2d23a69aa360c6922d8d749ce4b39fc937))
* Reformat pwsh oneliners ([11593fa](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/11593fa64dff52384472da297064e0f5a1179cd1))
* Remove bad tarball deletion ([8b39f96](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8b39f96606a327ea6a1eb90c539095e19186015b))
* Remove definition of decommissioned function ([04d27df](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/04d27df53e6ed938804a84c7eed65a71a15a6e1f))
* Remove duplicate versionrc file ([f617ac4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f617ac4926779531167ba250412fa62dc8b0112b))
* Remove extract-changelog-release when in Keep a Changelog mode ([2801b3e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2801b3e2b3725d63e34a56727adf9842b19d6384))
* Remove hardcoded test repo name from create-pipelines-azdo task ([e208929](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e2089292fcd42e4ce9c9044e0e83366324bf7e27))
* Remove unused function ([1203a97](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1203a9725c021bb32cc03a4c4429a82db5bb82ee))
* Rename-template-files target paths ([1592e0e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1592e0e6cff8daf5578081a6d06bc04a9950b58c))
* Rename-template-files task remove conflicting directories ([46b8e9f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/46b8e9f66463f2505087b1d40f34c9b0ccd5bf52))
* Reorder rename-template-files operations ([a6a2f40](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a6a2f409b62b7646aac5d3af5de74062031bdefd))
* Replace bad targets for moves and copies ([fd5fae7](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/fd5fae7535d9fbb0fa9b3665db540c2a7e2d30b5))
* Root path for rename-template-files step ([e9a75d5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e9a75d521b249586687760e8fbd8ea382a152567))
* Stop template-only files from being added to Standard mode projects ([adb7207](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/adb72075bdb651f9116683c8ce860de29f325cc4))
* Stop wiping target folders as part of subtemplate ([f33479d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f33479d23bfb94ed40685adeb3e6504a73a43038))
* Subtemplate generation attempt 3 ([aa98b22](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/aa98b22de191de2a7c7c0c58f5c2c09fff270a25))
* Switch back to shutil.move ([d766f58](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d766f585d2cf3b17adcdf9bdbfca0d6d9890d18c))
* Tagging in azdo repos ([c599a1b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c599a1bdf6abd9b84bf3ae9be4f9d4a53b64a763))
* Target proper directory for file renames ([04c91f6](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/04c91f6930810e95ed43a4db565d4a7bb53a3ba9))
* Try renaming only the files in rename-template-files ([41cb70a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/41cb70a6df8c91c13776895b72788bcf457aac79))
* Try shutil.move with only target file name ([d69d4b5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d69d4b50db39aa95a42172405ba7d8208e5fcaab))
* Update bad variable in standard project readme ([17066e5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/17066e5be08f895edf6606a014eaddc786c3b21c))
* Update release process to tag at the proper time ([82df74c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/82df74c1d9f803f593fd0e8120503bd73c2f18dd))
* Update src_path for new template name ([b4dfe87](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b4dfe8748499ad30d18e5da1c4df54c8fc0185ec))
* Url generation in workflow doc ([a7bd1fb](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a7bd1fb5b120fb904e12066f837ee4bd2f6b5050))
* Use move-item instead of rename-item ([6d0c9fa](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6d0c9fab59980408dcf65f3afbfd3802e9064adc))
* Use pwsh for rename-template-files task ([5969678](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5969678d69851bbc9eb52dd8bdbc609fb261d135))
* Use same renaming both ways for subtemplate ([4e3ddd8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4e3ddd8ba1901bf454d2a52d50350799158261ce))
* Use shutil.copytree for directory rename ([4bd523c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4bd523c6fe540b4e1987c516d7fc0db43b125959))
* Versionrc.json parserOpts for Azure DevOps ([2ad17c8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2ad17c80969fa940a214c1abb8a05800ef657da4))
* Wrap square bracket for pwsh ([3d838dc](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3d838dcba69c06ac7ac5981d0d4402cdcdeae5e5))


### Miscellaneous Chores

* Bump version to v0.2.0 ([a69b596](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a69b596b59a14478c3cfe5f17d7427f9d161b453))
