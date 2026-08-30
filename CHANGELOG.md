# Changelog

## 0.8.1 (2026-08-30)

### Features

- generate changesets from upstream template updates (#1099)
- fold REPO_MAINTENANCE_PAT expiration check into a repo health check (#1100)
- add extending-the-template guide and a docs preview tool (#1106)

### Fixes

- remove now-obsolete _old_tag_overrides from answer_matrix.py (#1094)
- fix knope current version (#1096)
- reformat CHANGELOG.md headings for Knope compatibility (#1097)
- cover Release (Manual) - Create Prerelease in AzDO pipeline check (#1101)
- rename Link Check to Repo Health Check in AzDO pipeline check (#1102)
- sync root workflow/copier.yml with the knope-native PR revert (#1103)
- close two Renovate coverage gaps and document a third (#1105)

## 0.8.0 (2026-08-28)


### ⚠ BREAKING CHANGES

* mark Azure DevOps support as deprecated  ([#1021](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1021))

### Features

* Add a Best-README-Template-style header to README.md ([#1072](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1072)) ([08bbd56](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/08bbd56392a03a25ee18d23e016746586dd95dff))
* Add a monthly link-checking workflow/pipeline ([#1067](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1067)) ([80df84d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/80df84db9cf677bed202284849018b713f43c0ff))
* Add a scheduled Renovate pipeline for Azure DevOps ([#1020](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1020)) ([188f4a6](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/188f4a67b3017e3b96b44f09f9b8028845f2df8d))
* Add an integration-test checkbox to the Knope release PR body ([#1074](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1074)) ([647bbf6](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/647bbf62f1920e9cc6b4ab0a1b761dc60fe0cb8f))
* Block lifecycle from regressing through its stages ([#1061](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1061)) ([7492ff2](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7492ff2f22d1b822188eb7f545801859188d2a11))
* Cache CI tool installs and migrate off knope-dev/action ([#1077](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1077)) ([a3bb276](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a3bb2767089ece2b21ca3c1422f14f57fddca7ec))
* Enable CodeQL code scanning for public GitHub repos ([#1049](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1049)) ([cb917ad](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/cb917adfe0f5cc82d9100ad1c6003294b32fb1ec))
* Enable private vulnerability reporting for public GitHub repos ([#1050](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1050)) ([29e9be6](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/29e9be699b14b066ad1ec3c4474a3d7249df7dde))
* Enable secret scanning for public GitHub repos ([#1051](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1051)) ([fe019a2](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/fe019a23fcb4a0d992cce3f40f4b3f5435d08427))
* Gate AGENTS.md/CLAUDE.md behind a new agent_instructions question ([#1045](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1045)) ([7f6b40b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7f6b40b2662b60337bd856a4dac55ac73e3a8e75))
* Improve template integration tests ([#1091](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1091)) ([d943db4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d943db49735c1ead22f524153ab01601956a88fc))
* Improve template test performance ([#1062](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1062)) ([a849652](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a849652c2387a8f8496372bba6cd76d24790f90d))
* Mark Azure DevOps support as deprecated  ([#1021](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1021)) ([a6102ec](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a6102ec54574e48779b1266cdf8b312f61d907b5))
* Pin and Renovate-track copier.yml's min_copier_version ([#1052](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1052)) ([b4f8e10](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b4f8e1088a440d4040dec1a72e795cbd4623ff64))
* Remove scheduled integration-test CI and all automatic repo deletion ([#1085](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1085)) ([f3c2440](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f3c2440a35f1c4036dd2e1d7a474e87514ad6040))
* Replace commitizen with knope ([#1060](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1060)) ([bd12132](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/bd121320c26d47f4b0c74af87223b616d80bae8f))
* Replace release-please with knope ([#1058](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1058)) ([9bf565f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9bf565f4eddf4a50a068b7da84d11d50aed4e933))
* Require PR titles to be a Conventional Commit ([#1070](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1070)) ([72f417b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/72f417b7247e333633f7d4ea21848ccf3eb470ea))
* Scaffold code coverage reporting infrastructure ([#1046](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1046)) ([a2d11d3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a2d11d30e7a4681802e53b8fee1bcfdd6ec1a396))
* Track post-copy setup items as a GitHub Issue or printed checklist ([#1073](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1073)) ([4ccbaf9](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4ccbaf9552f6722ca7167051e9a43366bec3ba1f))
* Unified workflow naming scheme ([#1075](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1075)) ([7efa432](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7efa432032286d8ba254854ed97b77fd3596c1be))


### Bug Fixes

* Align AzDO pipeline timeouts with their GitHub counterparts ([#1036](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1036)) ([bfee3aa](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/bfee3aad54c2f67dca7812d8a95689501d29afac))
* Cancel superseded PR-validation runs on new pushes ([#1033](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1033)) ([35f7646](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/35f7646718accef13a4a962bedeba7b9d845f3da))
* Correct and minimize is_template gating in renovate.json.jinja ([#1064](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1064)) ([041d89c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/041d89c8e09850e3a909c2cbe2069086622fc68b))
* Correct copier-update-check's display name and schedule ([#1038](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1038)) ([051104c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/051104c0079e1ea1160a2738b0d7934f4a44fdc3))
* Correct knope's mise pin to its per-crate monorepo tag format ([#1059](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1059)) ([0a7dd1b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0a7dd1bb9d6e74ba9ea2a347b7515befa20ca006))
* Correct the after-copy message's repo-setup guidance ([#1030](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1030)) ([9c4c60a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9c4c60a6bc7a756eb1ff7faee3c1333bd40f71d1))
* Current_knope_version's _copier_operation guard never evaluates ([#1066](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1066)) ([8bec0db](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8bec0db9f195c0653aeb20af202f26636e67eabb))
* Drop unneeded experimental flag from jdx/mise-action ([#1078](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1078)) ([e579b48](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e579b4893a010def5916b63699f9c353e38ee497))
* Extend AzDO integration test coverage to renovate + PR policy ([#1031](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1031)) ([f81409d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f81409d25eb724338e774d149e43734e0a0d434f))
* Group GitHub CLI's two Renovate package names ([#1019](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1019)) ([11249e0](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/11249e00a598428f0c37e2027741d7976971ecc4))
* Inline gh-workflow-keepalive to fix Windows compatibility ([#1081](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1081)) ([4ada95d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4ada95db0e164260b314fc677fa10cd79f53846f))
* Make Renovate see .jinja-suffixed template workflow files ([#1010](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1010)) ([145e213](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/145e213cefbd1247ea3c2f633610421b8eb82b2d))
* Make Renovate see .jinja-suffixed template workflow files ([#1012](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1012)) ([90270d9](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/90270d98031013c62c24509a9150c8077409fdf9))
* Make Renovate see conditionally-named mise.*.toml files ([#1023](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1023)) ([695a768](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/695a76895cef34362bb529b8185548cbfa1d15ab))
* Pin a minimum required mise version ([#1044](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1044)) ([2a53757](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2a53757ae6b1a470131faaccca6fe59df723030e))
* Pin the mise install script in Azure Pipelines to a known version ([#1026](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1026)) ([09a56fd](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/09a56fdfd7fc51f9f0ab1656ab6290f0fcab6899))
* Provision APPRISE_URL for the Azure DevOps Renovate pipeline ([#1028](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1028)) ([1633d58](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1633d58a18bcccab028a879d0469af77a7d7a91d))
* Quote changed-file paths passed to prek in CI ([#1048](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1048)) ([df26ded](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/df26ded14306090bf92ad9ca341fd42edb66393f))
* Remove unneeded experimental=true mise setting ([#1043](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1043)) ([2717468](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2717468e3e6c482e44235f712982c056ebe2471e))
* Replace .gitattributes eol=lf with a prek hook ([#1053](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1053)) ([396f37b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/396f37b077afe8e944cd270967802d308714277b))
* Replace unmaintained file-exists-action with an inline check ([#1063](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1063)) ([33b5ad3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/33b5ad32cd18e4847cdb8893c0a3a33ec1edd0ab))
* Scope AzDO PR validation's lint to changed files only ([#1035](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1035)) ([07af9da](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/07af9da7019cf307d904ca4aa721870f62ffaff6))
* Standardize GitHub workflows on Bash for runner portability ([#1083](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1083)) ([bef90cd](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/bef90cdd68be5c9392aa45845d60fa35efe5a61c))
* Sync template's rumdl config with root's MD007 override ([#1076](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1076)) ([be1029c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/be1029ceab1db87e293120da102404d402cc7016))
* Wait for PR validation to pass before auto-merging release/docs PRs ([#1025](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1025)) ([2ba1d93](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2ba1d937e49c517578a9c99fa2f9d75dd49a6942))


### Miscellaneous

* **deps:** Pin dependencies ([#1014](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1014)) ([bedc94b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/bedc94b15367b1389aad77a519e6d3d41a69cbbb))
* **deps:** Update cstuder/apprise-ga digest to bf5b598 ([#1015](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1015)) ([26a087b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/26a087b6861284e506e7b583d5f59f112dc2eb93))
* **deps:** Update googleapis/release-please-action digest to 45996ed ([#1016](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1016)) ([f6178fc](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f6178fc9017eebdfaf1b0d7bc636fb8be58d1c54))
* **deps:** Update jdx/mise-action digest to 3c2e0cf ([#1017](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1017)) ([d5acded](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d5acded4b298f2c41220ef2f293c6719ffed86c2))
* **deps:** Update liskin/gh-workflow-keepalive digest to f72ff1a ([#1018](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1018)) ([7e07135](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7e0713529c97cb2c1dcbc62f078a9b27bbf2b47a))
* Remove dead docker/devcontainer config from renovate.json.jinja ([#1065](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1065)) ([cee1ac8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/cee1ac82a3e7b9b604a18962226c87ebd6412015))

## 0.7.20 (2026-08-23)


### Features

* Enable auto-merge on all repos, not just Zensical ones ([#1006](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1006)) ([66f93e4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/66f93e4b6587205707f4c6ce1fe2ca62f1036dcf))


### Bug Fixes

* Resolve az via shutil.which() in the AzDO PR-policy task ([#1008](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1008)) ([6cc453b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6cc453ba6ab218f617c7539d27fd522706d8d864))

## 0.7.19 (2026-08-23)


### Features

* Remind users to set CI secrets after copy, add opt-in provisioning task ([#1003](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1003)) ([f967fd0](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f967fd0dd46e155e2bfbaa5a4be65e6bb556f7e5))
* Require PR validation to pass before merge, with admin override ([#1004](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1004)) ([093c4b9](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/093c4b9c5aa8b36debd815675d162913078359b4))


### Bug Fixes

* Fail fast when az/gh CLI or the azure-devops extension are missing ([#1000](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/1000)) ([53ee91f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/53ee91f908d0af3068b82f194787f342ab63cd6b))

## 0.7.18 (2026-08-23)


### Bug Fixes

* Fix azdo integration test ([#995](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/995)) ([a5fdda8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a5fdda805e5f4bdbd1221ac43df8dbf561bd8474))

## 0.7.17 (2026-08-23)


### Bug Fixes

* Fix integration test structure ([#992](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/992)) ([8a961cd](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8a961cd989bf3f1ad4427aad4ff22a028deab51d))

## 0.7.16 (2026-08-23)


### Features

* Set more github settings via settings app ([#987](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/987)) ([15ab4df](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/15ab4df1641f41b5bf36fc490dd718f779b1ce6f))


### Bug Fixes

* Fix integration test interactivity ([#990](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/990)) ([b826361](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b826361a6f69ae1a88e8811c28bf9d3a9c046fbd))

## 0.7.15 (2026-08-22)


### Features

* Add release-please labels to settings.yml, group by source ([#981](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/981)) ([3b66041](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3b66041ce8b8239370f4c1a1533674e441ddcf9d))


### Bug Fixes

* Restore GitHub default labels deleted by Settings App sync ([#977](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/977)) ([eebf2e4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/eebf2e482474e441c85748494eeb7e113e2fb2c2))

## 0.7.14 (2026-08-22)


### Features

* Add set-lifecycle mise task ([#645](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/645)) ([#968](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/968)) ([e44721f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e44721f19fd73cb14b1c3e26e28ac40e35ba16e9))
* Centralize tool caches ([#961](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/961)) ([246bec4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/246bec43699cf9137914a89510488c9d1ae79461))
* Improve integration tests ([#967](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/967)) ([e8f628f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e8f628fb27d4455dc5c188e7249424daeffc17b5))
* Migrate Azure DevOps repo setup to az CLI ([#962](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/962)) ([b43e84b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b43e84b4e469528b263ac21f03dfab0a114e7250))
* Migrate GitHub repo setup from githubkit to gh CLI ([d12d567](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d12d5677627c783990259503c7caa45d4c76929a))
* Replace imperative GitHub repo settings with Settings App ([54f18a8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/54f18a8974e569166fcd8bd0f94f6941a4e84394))


### Bug Fixes

* Remove whitespace from template's lychee.toml.jinja ([97c150e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/97c150e43fc3cd12fcaa63d62e740128a3436559))


### Miscellaneous

* **deps:** Update jiangxin/file-exists-action digest to 81a413f ([#958](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/958)) ([9eb754d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9eb754d7d2d8d9b1703ac33dd0b6ba8ac0e9ae74))

## 0.7.13 (2026-08-07)


### Features

* Set sensible lychee and ryl linting rules ([74903d1](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/74903d11a64f9a5f145ec3f243f8e82d10052313))


### Miscellaneous

* Fix dead link ([dab8d1e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/dab8d1ede95ae33fc710881c58b61a4d5f978aa3))

## 0.7.12 (2026-08-07)


### Features

* Replace yamlfmt with ryl ([a9ffd3b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a9ffd3b335c3771ce005619925e1b279ca9a59aa))


### Bug Fixes

* Renovate cron schedule needs asterisk minutes ([c82b4e4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c82b4e433e565fbea4671514f9f2d006bc12aea7))
* Wrap renovate managerFilePatterns in slashes for regex mode ([5c842f5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5c842f54cfb94a18e9324668a8f965f2f5391372))


### Miscellaneous

* **deps:** Update dependency python to v3.14.7 ([#953](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/953)) ([7122573](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7122573d173287cd43337d4b4445e073a84eaabd))
* **deps:** Update rumdl to v0.2.52 ([#957](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/957)) ([b922502](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b9225028c16ae4f254ed360fa5220018557e1b43))
* **deps:** Update uv to v0.12.2 ([#955](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/955)) ([8124c01](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8124c010949b74c40cac21b7a5f853ce733193ad))

## 0.7.11 (2026-08-07)


### Bug Fixes

* Sync repo root with template v0.7.10 ([1f46166](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1f461662fa54e3b50c36274b85ea9b8f259f8eb8))

## 0.7.10 (2026-08-06)


### Features

* Add Azure DevOps PR validation pipeline ([55a0958](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/55a09583a4bdeb822c7c903d0baf89c18a25fde2))
* Add bidirectional nav-completeness test ([79fc8cb](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/79fc8cb0cb4612c1ee1643546661e4ace6a58c17))
* Add explicit nav ordering to zensical.toml ([73009e1](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/73009e15675d15ec9854cce2995361ab5e895796))
* Add lychee link-checking for text files ([e647526](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e647526d717a888fe0dd41bdba5d7344e47190a4))
* Add render-validation test suite ([7932132](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/793213247ea6f1513999ff7a32dd003e7430e85d))
* Add shellcheck as a standalone prek hook ([eab14bf](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/eab14bf1d7a9f6f9d7f9292a7d14f607bad5ad1e))
* Add test verifying invalid answer combinations are rejected ([d42cb75](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d42cb7501ed833cfd46304e4523f0d60bb2b613c))
* Add update-path testing (last tag -&gt; current) to render suite ([5eab8a1](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5eab8a11e4ae71ec97e4bc688d09a60c9f4a1ddf))
* Add workflow_dispatch trigger to release-please and zensical workflows ([166be1d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/166be1d50ce3205dcf789fabf63835b67372ea50))
* Compute current_release_please_version_is_pre_1 for real via git+from_json ([097c248](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/097c2485ae30119c9a2fa73a42933617ff692c3a))
* Replace placeholder test step with the render-validation suite ([b4385ca](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b4385ca6522800da02dbb85e08d7e25e6ad326a2))
* Run pytest suite for tasks.test, add pytest as pipx tool ([6c14917](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6c149174969e4de3cf37a8cebf0e9eac5e6a066a))
* Surface pytest failures/warnings as native CI annotations ([8af1c0c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8af1c0c62dd525d981af933574d8561a37ee7af3))
* Template prek.toml to mirror mise.toml's tool gating ([4c30ec2](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4c30ec290650f37792dfcf3542a2de4c903e7ce3))
* Verify answer_matrix.py covers all copier.yml choices ([04038f9](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/04038f957f2b70d1f4beab31a438efc93bfe11ed))
* Warn in README when a public project has no license set ([adfb43f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/adfb43f7f2e78f3163be8ada5b57e509159cc927))


### Bug Fixes

* Add concurrency groups to prevent overlapping workflow runs ([e89acb3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e89acb31d827f52940dbfb77357b9ea4faeadd5b))
* Add jinja-toml VS Code file association for prek.toml.jinja ([49b0cc6](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/49b0cc6d6c5b7fdd0ff0f331964dac430831208e))
* Align release-please manifest package key with config for Standard projects ([402ec29](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/402ec29f684ccb5ac8b0d8f4677afcb037bb1b92))
* Compile-time gate the render-test CI step to Template projects only ([8ad8ec9](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8ad8ec934931586cfc1dfd541f89937afbba7cf7))
* Correct APPRISE_URI typo to APPRISE_URL in AzDO update-check pipeline ([5dcec3b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5dcec3baec4773c577ffb3f6bc8820d7a4c924fe))
* Correct broken doc links in docs/index.md ([424f39a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/424f39af94acbbeee0e7fd737b8c7abdfaf95de4))
* Correct broken Getting Started link in applying_to_existing_projects.md ([e7eaf73](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e7eaf733f172fd23a8368460335e6f1c2b030bc5))
* Correct dead anchor link in template_questions.md ([388083b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/388083bad98ce1a39457568e0b1dde7995152215))
* Correct garbled sentence in token_permissions.md ([f74a279](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f74a279c6ec2857f93be026acc7ce07d7bf5a685))
* Correct inaccurate step reference in applying_to_existing_projects.md ([5a97ddf](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5a97ddf7f7556ae9ba3fe99386c863a6febbe5a0))
* Correct renovate cron from every-minute to once-monthly ([1883bf4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1883bf47e9fa98bbe678eadeb2fc8ee4893afc8d))
* Correct yamlfmt config path in VS Code settings (missing leading dot) ([ca20e32](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ca20e32c9ae3d32a82b95be50cac5801e3e54d80))
* Don't emit nonsense typos.toml entry when github_org is unset ([123663f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/123663f57432ca0c3ee22c3e8a3b2cc0e5713a22))
* Don't render README License section unless using_mit ([a8fc949](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a8fc94976d98830beebe7a0874147fd4e0e9a17d))
* Drop unneeded MISE_ENV: ci from test-pr_validation.yml ([6a0f8d1](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6a0f8d163e297af9323d1f620c1236b8b4f0453f))
* Enable automatic GitHub Action digest pinning via Renovate ([04e73b5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/04e73b5338083a59520e83ad8c8ad522aceed1a1))
* Fix jinja whitespace issues ([#947](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/947)) ([ba9e7b1](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ba9e7b12e11fe4e4e1a4a210d182f994cb8d01d1))
* Gate [tasks.test] on is_template like the integration-test tasks ([846ba41](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/846ba41a3be3ec785e7065659c5b756a4c7b87e4))
* Gate actionlint/ruff tooling to when they're actually needed ([352fd76](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/352fd7679c60fd8ad1686b1a349d1a4f062e8f5b))
* Gate docs_site/ folder on zensical_repo instead of undefined mkdocs_repo ([674992e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/674992ec6b2e568be454de15c6a5699e9baa7a30))
* Make CONTRIBUTING.md's license clause license-agnostic ([aad791c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/aad791c23893483d541a353c23330d6500fa0844))
* Pin third-party GitHub Actions to commit SHAs ([8760d7b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8760d7b105a46ce100dd1927679365463cd8128f))
* Qualify doc-versioning claim to GitHub Pages target only ([80a677e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/80a677e97433e57a63c171dbe6f4f231060edb6f))
* Remove dead LICENSE link from CONTRIBUTING.md for no-license projects ([2239e0c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2239e0cd7d4df7ccdd3d7bddc25079bd2ebbf49f))
* Remove orphaned taplo.toml, add missing tombi.toml ([944ba1d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/944ba1d5f68bc1e90d311a01eabf397bbfea3318))
* Remove trailing comma in release-please-config.json for Standard projects ([2f0254e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2f0254e85af6fa8278e471ba46f03ed8f4457243))
* Remove trailing comma in vscode extensions.json.jinja ([959aeaa](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/959aeaa13b1708c4b7ece55ba9223ccf6201b256))
* Remove windows_default_inline_shell_args from mise.toml ([45bf939](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/45bf9390a8e3e052e3df199afe0cf023eb1f8c8d))
* Replace custom yaml_quote_extension with to_yaml filter chain ([4f14596](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4f14596e6d6d0f6470c5d86ef3fdba7a14d85741))
* Replace no-op 360min timeouts with realistic per-job values ([665dcaf](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/665dcaf51cd488f4a23e9b59204d75494fe1cbb5))
* Rewrite prek.toml hooks as TOML array-of-tables, not inline ([3b4ce07](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3b4ce07ff71a2c4ebc074e3234fd0a8dcd649302))
* Scope workflow permissions to job level least-privilege ([863fd7d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/863fd7d7a2e9246367076a411a3664ecd6d258d6))
* Urlencode azdo_project_encoded instead of manual replace ([a7131be](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a7131be8b31d987ade8508323900d526683dbd21))

## 0.7.9 (2026-08-05)


### Features

* Apply 0.7.8 and correct drift from inner template ([#944](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/944)) ([9dc6d04](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9dc6d04ca64326f16ac05127086a5a80d8c68a1a))

## 0.7.8 (2026-08-05)


### Features

* Apply parent template 0.7.7 and refactor between levels ([#942](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/942)) ([3f22c53](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3f22c53a49e599b65e76837c5c4ade0baf601673))

## 0.7.7 (2026-08-05)


### Bug Fixes

* Fix github_repo_owner calculation ([#940](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/940)) ([21afc2c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/21afc2c2ac9d50953f92d7fa972b9d7494298b46))

## 0.7.6 (2026-08-05)


### Bug Fixes

* Restore missing endraw ([#938](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/938)) ([b061476](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b06147644c9385cd3880579b982f594d0996a77f))

## 0.7.5 (2026-08-05)


### Features

* Improve help text on update ([#925](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/925)) ([f8722b8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f8722b8b39bcc74712529653cb952c2c2f2a7012))


### Bug Fixes

* Undo failed ask once conversion ([#924](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/924)) ([9bdb2c4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9bdb2c42154f0ec356a70dbfe1bbf73253be4220))


### Miscellaneous

* **deps:** Update actions/cache action to v6 ([#932](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/932)) ([76d8e65](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/76d8e6501b4bc4f40aa273d0d0cf8cd557345b6d))
* **deps:** Update actions/checkout action to v7 ([#933](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/933)) ([6339405](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6339405b73a57c01185670af2eec71e95d6515e2))
* **deps:** Update actions/upload-pages-artifact action to v5 ([#934](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/934)) ([81ee43f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/81ee43fa1e7bf9022157c3f39ea7ae87f844fb2b))
* **deps:** Update apprise to v1.12.0 ([#927](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/927)) ([23b016e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/23b016e267e3f68b7f06a6fadf96c147764b9bde))
* **deps:** Update commitizen to v4.17.0 ([#914](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/914)) ([3d77408](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3d774081edd34fc8d4fb61f40b64ca1cba445507))
* **deps:** Update copier to v9.17.1 ([#928](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/928)) ([f353146](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f3531466e0c8a54e20d8879cd46fbda8991cd095))
* **deps:** Update dependency githubkit to v0.16.0 ([#915](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/915)) ([f144271](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f144271f33faf60eea0201b418d87bc0398030ea))
* **deps:** Update dependency python to v3.14.6 ([#921](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/921)) ([1f33adb](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1f33adbc71396b8f89f3641a7738da7ad6f19aa3))
* **deps:** Update dependency requests to v2.34.2 ([#929](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/929)) ([ad37959](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ad3795922d0c739a0fa3714f0dcca2c0106083b9))
* **deps:** Update dependency rich to v15 ([#935](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/935)) ([d6ade25](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d6ade256e7ddb4bb1ebf54cd610bf7fa1368bb50))
* **deps:** Update googleapis/release-please-action action to v5 ([#936](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/936)) ([0e588da](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0e588da96f7c2fa6847355ad8757b8da9314fe3a))
* **deps:** Update joshuakgoldberg/all-contributors-auto-action action to v0.6.1 ([#926](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/926)) ([8402b35](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8402b352bcd59555d092d40553113bfa90b77991))
* **deps:** Update prek to v0.4.12 ([#917](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/917)) ([047aa9f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/047aa9f81f42ee03cadbe277bb624824b563ce65))
* **deps:** Update ruff to v0.16.1 ([#918](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/918)) ([f82a8eb](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f82a8ebf580bd815690a84658e3cf5d071d80868))
* **deps:** Update rumdl to v0.2.50 ([#919](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/919)) ([59f11c4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/59f11c4700658f2ac8e29ca7e0792a8cdaf31223))
* **deps:** Update tj-actions/changed-files action to v47.0.6 ([#920](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/920)) ([8b4989e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8b4989edd5e09977bc49bb34ea433d4ddd0579fb))
* **deps:** Update tombi to v1 ([#937](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/937)) ([ab9cb9f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ab9cb9fbd7a9c7e5f0c18dcb154a36a00ec1939d))
* **deps:** Update typos to v1.49.0 ([#931](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/931)) ([46f31e1](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/46f31e16fb70f195b0d7d322a9caf4c9a2ea9d0e))
* **deps:** Update uv to v0.12.1 ([#922](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/922)) ([57f8f35](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/57f8f350a2bd025a0d9a71d646ef8503aa7186c3))
* **deps:** Update zensical to v0.0.53 ([#923](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/923)) ([7bd606d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7bd606d70c6ba69c98bbeeba5cd8cd19825286fc))

## 0.7.4 (2026-04-09)


### Bug Fixes

* Ensure there are defaults for all questions with choices ([020c253](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/020c2536330226007e0a581fb465360726624d0a))

## 0.7.3 (2026-04-09)


### Bug Fixes

* Fix typos dep in template ([0c7aaba](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0c7aaba1cbdb775f637079ec533353609f679770))


### Miscellaneous

* **config:** Migrate Renovate config ([#910](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/910)) ([ad5f9f5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ad5f9f565c803fe9511ab20a20e895d4cc6201de))
* **deps:** Update actionlint to v1.7.12 ([#896](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/896)) ([f8fb949](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f8fb9495573038f36c8537357bb25600777cfe32))
* **deps:** Update committed to v1.1.11 ([#897](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/897)) ([77e7361](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/77e736141a0db4ca4f6abb3b19009ee22c605783))
* **deps:** Update dependency python to v3.14.4 ([#898](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/898)) ([10b1881](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/10b188127b9b8dcfc9bda124fe4d265ebf52e9b9))
* **deps:** Update invoke to v3.0.3 ([#887](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/887)) ([7b1deae](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7b1deae7fa311742d4f35ade8d5330f69c1acfa2))
* **deps:** Update ruff to v0.15.9 ([#899](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/899)) ([b0bc5f5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b0bc5f50db898bfa1f67c8f91b7b63fc1934cb20))
* **deps:** Update rumdl to v0.1.68 ([#900](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/900)) ([3fd2096](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3fd20967eb6a85f726272a01d6da6cec43c7f175))
* **deps:** Update shellcheck to v0.11.0 ([#905](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/905)) ([9016bce](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9016bce829ec5a543452a3608a40ad0339775860))
* **deps:** Update tombi to v0.9.16 ([#901](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/901)) ([80d1f26](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/80d1f261da0061176e1211d30e5da0c23873a724))
* **deps:** Update uv to v0.11.5 ([#902](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/902)) ([313b25e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/313b25ee1cd974ba43d4052a3768ab023717409f))
* **deps:** Update yamlfmt to v0.21.0 ([#906](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/906)) ([9347d29](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9347d298bc9e69031811e84ccff8c950a4a79b31))
* **deps:** Update zensical to v0.0.32 ([#903](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/903)) ([143b490](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/143b490c4ca6d79ac9a09785a4e4d566b03a6f0f))

## 0.7.2 (2026-04-09)


### Bug Fixes

* Fix handling of github_org question ([d645e28](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d645e2852c999ec1d213914da33ad67075b35d15))

## 0.7.1 (2026-04-09)


### Features

* Update copier questions to only ask once ([#907](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/907)) ([06a0de8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/06a0de8f69bc703a7446a61654e4608abbbfd183))


### Bug Fixes

* Add renovate support for zensical's mike fork ([44a26cc](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/44a26cc3ef1f20ffbc2d4af64df5ea894c55e6bc))
* Adjust renovate regex ([770c361](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/770c36145b2b2d6457dbe5f9570915bb104377d2))
* Fix template syntax ([e9dfb05](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e9dfb0574cac7d6474422faa414237bfdc4405ba))
* Fix zensical github in-repo builds ([c4a346d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c4a346d5c54b6a65593c7a616fc5fcf621adb338))
* Fix zensical_repo computed value for template ([0b2fdb5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0b2fdb59c02d7af87e66141bded31b60c6eb1759))
* Remove ambiguity in renovate parsing ([4c6a5ef](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4c6a5ef1f454b7c18c040e8c21fa0027f868644c))

## 0.7.0 (2026-04-09)


### ⚠ BREAKING CHANGES

* replace mkdocs with zensical ([#893](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/893))

### Features

* Execute prek hooks directly with mise ([cb16de9](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/cb16de94daecf2519e3307a9b2c8e0e8fbbf0b07))
* Move from markdownlint-cli2 to rumdl ([3d0b2af](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3d0b2af2e72e5aa4816c3d8d1504135aca768ca5))
* Move prek dependencies into mise ([3de4d84](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3de4d841dcffac5035c05f25cf9a66ec9d9d9426))
* Move ruff from prek to mise ([de382e0](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/de382e0b6df5f75e6a713725d300e694bccdf86b))
* Move typos from prek to mise ([7921b8b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7921b8bc04c46c136a7e6e94243c41bc8a84d770))
* Move typos from prek to mise ([4352f62](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4352f62be604ff1bf2cf00b031d9d3146b29981b))
* Replace mkdocs with zensical ([#893](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/893)) ([c3e8b07](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c3e8b07d1c8ea219ce21e58b0472385891f17272))

## 0.6.0 (2026-04-07)


### ⚠ BREAKING CHANGES

* switch azdo to use commitizen for releases ([#878](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/878))

### Features

* Finish renovate groupings ([eaef352](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/eaef3522ce4ccbef208e1a8842d9f4571c9ea821))
* Improve renovate configuration ([8588c67](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8588c6753c5d5d2f36b5a32c4586aa062835291a))
* Improve renovate.json template ([bf8e46e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/bf8e46e1b589a63092831ac67cc371bb0c7b5d51))
* Move renovate from json5 to json ([e534ffc](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e534ffc02f83602b21ff46ea6f8276dfff8415f3))
* Replace taplo with tombi ([#833](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/833)) ([d8002a0](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d8002a0650a4ddfffec265d9d78da6c383321b70))
* Start using copier check-update for template update checking ([#867](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/867)) ([7ca7ab3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7ca7ab338ffd8a62e76466b78d19a7e79e02b9ea))
* Switch azdo to use commitizen for releases ([#878](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/878)) ([3bed035](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3bed0352997abdf4daba3242395ef055296d7262))
* Switch from pre-commit to prek ([9328bcb](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9328bcbf29d61564f920b385202263fe163e8232))


### Bug Fixes

* Fix azure devops update workflow ([b4387f2](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b4387f27ba4296e06844d439e3ea7da87e25803e))
* Fix extensions.json whitespace ([#842](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/842)) ([ad5f719](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ad5f7199acdfb2337ce9321ee898c80d1a17c235))
* Fix prek execution across the board ([b65a400](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b65a40024128409efa7509e59059dabae8d9c04f))
* Have renovate detect pipx deps in mise.toml ([129346e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/129346e009ebce82d5cb2b7bbf2031418d3644ea))


### Miscellaneous

* Backdate all deps for renovate testing ([e6dd349](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e6dd349aa10a3471fa782d678e1ccd8e6bec01da))
* **deps:** Update actions/cache action to v5 ([#857](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/857)) ([c7cfdcd](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c7cfdcd111830a5d002cc39e2c872ea83fbcde7e))
* **deps:** Update actions/checkout action to v6 ([#858](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/858)) ([ae12385](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ae1238541b91f7205679aa92844f7af81810b50a))
* **deps:** Update actions/configure-pages action to v6 ([#859](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/859)) ([22dc949](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/22dc949023013ad8249ba628c3c66a27d0277ded))
* **deps:** Update actions/deploy-pages action to v5 ([#860](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/860)) ([54b4620](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/54b4620f0790cf01288feca808c481f6466b9d35))
* **deps:** Update apprise to v1.9.9 ([#865](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/865)) ([1e59f91](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1e59f9199f9e4d6794a1503e1615b36f56ae5cc8))
* **deps:** Update commitizen to v4.13.9 ([#886](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/886)) ([c1b9165](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c1b916555ac95429b51cca541ccec1a44205b47f))
* **deps:** Update copier to v9.14.1 ([#889](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/889)) ([662510d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/662510da1d9238d1b184d8925235d4ad894b3f6d))
* **deps:** Update dependency apprise to v1.9.7 ([#820](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/820)) ([a330c63](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a330c63899dcf0e079ce0ea41c76c92826c1d911))
* **deps:** Update dependency astral-sh/uv to v0.10.8 ([#821](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/821)) ([794a777](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/794a7776a3ff342581045246a4d734862e625350))
* **deps:** Update dependency astral-sh/uv to v0.11.2 ([#841](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/841)) ([fdbd080](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/fdbd080aec40301256dc8a943ca7aca017d72fad))
* **deps:** Update dependency commit-and-tag-version to v12.7.1 ([#843](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/843)) ([6051521](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/60515210c7100a6ebe5898bd55cc34555438e5a3))
* **deps:** Update dependency copier to v9.12.0 ([#822](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/822)) ([72d508f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/72d508f73217eb99d04a71d518461649c20132be))
* **deps:** Update dependency copier to v9.14.1 ([#844](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/844)) ([603969e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/603969eef36248571f89435318501a3572dbe4db))
* **deps:** Update dependency copier-template-extensions to v0.3.3 ([#870](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/870)) ([a8928f0](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a8928f0a7d8cb5814c8b7c61f343d7d7f97bddfc))
* **deps:** Update dependency githubkit to v0.14.6 ([#823](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/823)) ([e86a949](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e86a949813389e6fc7b8e928d3bacfb2c123ae9f))
* **deps:** Update dependency githubkit to v0.15.2 ([#846](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/846)) ([bc16905](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/bc1690541e75ad9540b7f92b35f93017a3fdb7db))
* **deps:** Update dependency google/yamlfmt to v0.21.0 ([#828](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/828)) ([35f9287](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/35f92876e306eb8d9c0fbd7b07f57e3e9c2c6019))
* **deps:** Update dependency invoke to v2.2.1 ([#824](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/824)) ([4ede68d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4ede68df81406fbebe5a2b7f42aa7c9932913b75))
* **deps:** Update dependency jinja2-shell-extension to v2.1.1 ([#872](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/872)) ([24ad246](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/24ad24619387cadfb4b07fead2eebf6e8a7ad780))
* **deps:** Update dependency mikefarah/yq to v4.52.4 ([#829](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/829)) ([da4877a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/da4877af346bbe0cb8b3f3dd749ebc6ff286a7b4))
* **deps:** Update dependency mkdocs-material to v9.7.4 ([#825](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/825)) ([8f16a97](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8f16a97f1b39a6784e5591194f553493296e9145))
* **deps:** Update dependency mkdocs-material to v9.7.6 ([#837](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/837)) ([b6feb79](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b6feb79cd83bae7e2df7b8c087dbe2e9cf13234f))
* **deps:** Update dependency mkdocs-static-i18n to v1.3.1 ([#838](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/838)) ([1a12ae6](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1a12ae63f432e2a5bc767b8064f31535a3fd7d8c))
* **deps:** Update dependency python to v3.14.3 ([#849](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/849)) ([adf2224](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/adf222426a14efa3a8325b144b94d329a1b5b9a0))
* **deps:** Update dependency requests to v2.33.1 ([#850](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/850)) ([eb73738](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/eb73738947c583643fa03ea8cf5316a0674ce548))
* **deps:** Update dependency rich to v14.3.3 ([#851](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/851)) ([3a61aa4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3a61aa4c308409eddc11d98c120640137e657ec6))
* **deps:** Update invoke to v3 ([#891](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/891)) ([9d557e1](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9d557e1bb983728ffdf1bcdfd76f8ed92cc20a3c))
* **deps:** Update jdx/mise-action action to v4 ([#861](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/861)) ([a9750a9](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a9750a9dc23c11d1e001242f40af6ea9e7b022d6))
* **deps:** Update joshuakgoldberg/all-contributors-auto-action action to v0.6.0 ([#855](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/855)) ([e9abba5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e9abba583987131aa5e93fc44b554694cd3b0982))
* **deps:** Update mike to v2.1.4 ([#866](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/866)) ([aafe970](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/aafe97043bc343c77f5edc89bfaea9bd57151dce))
* **deps:** Update mkdocs to v1.6.1 ([#884](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/884)) ([575ae9d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/575ae9de9970d20a1c3fe0cb2725288027208a12))
* **deps:** Update peter-evans/create-pull-request action to v8 ([#863](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/863)) ([d14374f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d14374f5df147f108e322b0b6524233fa230c933))
* **deps:** Update prek to v0.3.8 ([#888](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/888)) ([c94197a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c94197a006d7c850f0b63c995c67b0ecdaaa6969))
* **deps:** Update tj-actions/changed-files action to v47 ([#864](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/864)) ([3905f95](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3905f95cd40f4ac092f10cb1c739d201e887f496))
* **deps:** Update uv to v0.11.3 ([#890](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/890)) ([1dc8454](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1dc84543728f3d820a519beb24a30e386fdab5c3))
* **deps:** Update yamlfmt to v0.21.0 ([#885](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/885)) ([d297d0e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d297d0ebbf10e72064a9eefd338617243b1d5da1))

## 0.5.25 (2025-09-10)


### Features

* Switch to squash merges for azdo pipelines ([#817](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/817)) ([9acddad](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9acddadb70eaab304576ff2727c851acc1709ae2))

## 0.5.24 (2025-09-10)


### Bug Fixes

* Move .versionrc.json back to root ([#814](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/814)) ([ad33980](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ad33980efd7e96c150fd6541af82423b1267b88d))

## 0.5.23 (2025-09-10)


### Bug Fixes

* Fix azdo versioning ([#811](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/811)) ([80ab965](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/80ab965160e16b8e5348114edcf15ce69479403f))

## 0.5.22 (2025-09-08)


### Bug Fixes

* Fix versionrc formatting ([#807](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/807)) ([b15c6b9](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b15c6b9bc8b397c37b26c251ad2a19668c4c0b12))

## 0.5.21 (2025-09-08)


### Features

* Use src directory for standard repos ([#804](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/804)) ([48ac808](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/48ac808535fe199dda3735deb330e60088e131b4))

## 0.5.20 (2025-09-08)


### Bug Fixes

* Fix changelog path ([#799](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/799)) ([7f3d5d8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7f3d5d8ae23aebde5e985d2d06496d403acc3c6d))
* Fix changelog path to be absolute ([#800](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/800)) ([1e37fda](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1e37fda3cf673c9d377ec5b030592fcb5332f6ac))

## 0.5.19 (2025-09-08)


### Bug Fixes

* Adjust release please config to only target template dir ([#796](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/796)) ([df1ca99](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/df1ca994f88e7ac0529f719876678063ae9f503a))
* Fix release please manifest ([#797](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/797)) ([897dc5f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/897dc5f790aae2654ba0927bb4a49287ba57dde2))

## 0.5.18 (2025-09-08)


### Features

* Add explicit timeouts to all workflows and pipelines ([#777](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/777)) ([2228a5b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2228a5b28f3df0c0de224da061b4713352edcdcb))
* Add renovate support for uvx requirements with extra ([#791](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/791)) ([78daa01](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/78daa014b4c94361d7d756ff22a415b1baef7d5f))
* Apply parent template v0.5.17 ([#773](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/773)) ([1fde79b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1fde79b354aa6fb5c8efc2962284fdb1b87b08c4))
* Move .versionrc.json into .config ([#790](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/790)) ([d05cdf3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d05cdf39ede4bb9af592cc93016789b7ac6b6a1a))
* Set release please to only run template files for template repos ([#793](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/793)) ([dc6adf5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/dc6adf588e37d425e4624694dd5584ee8528d84d))


### Bug Fixes

* Remove prompt-toolkit pin ([#789](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/789)) ([6b34f1c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6b34f1cbace44cd88dea1c788bb7271736a55568))


### Miscellaneous

* **deps:** Update actions/upload-pages-artifact action to v4 ([#787](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/787)) ([1ec6c48](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1ec6c4816588f898af8aa743366384fd6e5782e8))
* **deps:** Update dependency astral-sh/uv to v0.8.15 ([#778](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/778)) ([b40ca0e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b40ca0ed15dc3984b3f1215deacd6f138f8721ee))
* **deps:** Update dependency commit-and-tag-version to v12.6.0 ([#784](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/784)) ([55db6d6](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/55db6d671c1f97adad3187ecd7b2c650b9e38b2f))
* **deps:** Update dependency copier to v9.10.1 ([#785](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/785)) ([ddf36fc](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ddf36fce718c03249b28a88563ffb8e32d364e4e))
* **deps:** Update dependency githubkit to v0.13.2 ([#779](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/779)) ([1a3827b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1a3827b0c3d7215b9fffa88a5ec0d7dc0442a8bf))
* **deps:** Update dependency mkdocs-material to v9.6.19 ([#792](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/792)) ([2003c2a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2003c2a475bb0341d3e7c1869fbda812166e3a3a))
* **deps:** Update dependency pipx:copier to v9.10.1 ([#780](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/780)) ([668ad0e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/668ad0e7ff3f1c87a5e4d9d795f9d8cf0473ae42))
* **deps:** Update dependency python to v3.13.7 ([#781](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/781)) ([ab8cedb](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ab8cedba8bda75ecb8c9908c199b7c148c0c6787))
* **deps:** Update dependency requests to v2.32.5 ([#782](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/782)) ([484809f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/484809f9b28cbc3001881e8cd98a148af9a0b69d))
* **deps:** Update dependency uv to v0.8.15 ([#783](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/783)) ([4e25f00](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4e25f009c98641220ad0f38cfee6bd14455dd985))
* **deps:** Update jdx/mise-action action to v3 ([#788](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/788)) ([f41fef8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f41fef8bbbb1df1f8865bbb60cc7fe08e9e5f0af))
* **deps:** Update node.js to v22.19.0 ([#786](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/786)) ([119313c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/119313cdaf570cdbfd51adafdccd8ed86e9a18bc))

## 0.5.17 (2025-09-03)


### Bug Fixes

* Fix computed question azdo_project_encoded ([#771](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/771)) ([3124582](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/312458277d3e9024f51c9a9354293d82f81381cf))

## 0.5.16 (2025-09-03)


### Bug Fixes

* Fix support for azure devops projects with spaces ([#769](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/769)) ([3bb001d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3bb001d578831607396a25c59ff022c8780864e4))

## 0.5.15 (2025-08-27)


### Bug Fixes

* Adjust copier dependencies ([#764](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/764)) ([27e5e66](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/27e5e6605ba816b1b4032d8e2713c105763e4e56))

## 0.5.14 (2025-08-27)


### Bug Fixes

* Fix doc building attempt 1 ([2162c9f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2162c9f21b8ec3522642c4fc981dff9b6532903a))
* Fix doc building attempt 2 ([4fbc8d0](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4fbc8d0d7647254428bd04cefb479012a27c6c28))
* Fix docs building ([#763](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/763)) ([73cd9d3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/73cd9d32dc634d837a17bb48fad5c33e23613925))


### Miscellaneous

* Apply template v0.5.13 ([#760](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/760)) ([26cec3e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/26cec3e5d768cc481d2546a95f7bc31c7dcea86d))

## 0.5.13 (2025-08-26)


### Bug Fixes

* Adjust question structure to unbreak updating ([#758](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/758)) ([bf4ad0a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/bf4ad0a488058aebc14a493a8d4b749755e99fc7))

## 0.5.12 (2025-08-23)


### Features

* Apply template v0.5.11 ([#755](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/755)) ([eeab295](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/eeab295fb9541616eb7af64c43157b38d1461bd9))
* Switch to using mise for ghpages mkdocs workflow ([#757](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/757)) ([f9c0801](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f9c0801e180c10a11d9aa0abe0bbd408595b21a8))

## 0.5.11 (2025-08-23)


### Bug Fixes

* Adjust conditions for setup-mkdocs-ghpages ([#752](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/752)) ([848ff3e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/848ff3e55f33784e6dcd66f55aed0be222f2b5ea))

## 0.5.10 (2025-08-23)


### Bug Fixes

* Fix azdo_token question ([#750](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/750)) ([1a2f424](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1a2f42452d70a62ebff4cffdbb4a7e687c3ca4b9))

## 0.5.9 (2025-08-23)


### Bug Fixes

* Fix bad token criteria ([#748](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/748)) ([3bf92df](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3bf92df1e930edaf8905f3d008abe77e8a69bf8f))

## 0.5.8 (2025-08-23)


### Bug Fixes

* Fix token criteria ([#746](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/746)) ([4ecba7d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4ecba7da256ce6cd26643446d5ec8c902c3fbc89))

## 0.5.7 (2025-08-23)


### Bug Fixes

* Restore the None option for repo_setup_actions ([#744](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/744)) ([042edef](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/042edef78c1170179d510b5bc5da7d16493c7833))

## 0.5.6 (2025-08-22)


### Bug Fixes

* Fix azdo update check ([#742](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/742)) ([535ff77](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/535ff7749079ac222b4f5a2c64af4f6794d6ac24))

## 0.5.5 (2025-08-22)


### Features

* Refactor license question ([#740](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/740)) ([5895839](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5895839b424f9c8012ae96d7eb0a66fbf5ca5d0a))

## 0.5.4 (2025-08-22)


### Features

* Refactor github_repo_description to project_description ([#738](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/738)) ([ff8a9f3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ff8a9f3195d0bf88de57fdd28786cd07bfcc59b7))

## 0.5.3 (2025-08-22)


### Features

* Ask setup questions once ([#736](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/736)) ([1f93115](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1f93115fd1c9cede407c058f067a0fd12aecbfeb))
* Implement copyright_year computed value ([#732](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/732)) ([c08a7ab](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c08a7ab7d824be48e90167fb5071871c44a909a2))
* Remove context.py in favor of _copier_operation ([#734](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/734)) ([4d02a22](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4d02a22aed21b5093de56b45b93567358782ed1b))

## 0.5.2 (2025-08-15)


### Bug Fixes

* Properly make vcs_ref optional for copy_template_files ([#730](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/730)) ([6dcfcf4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6dcfcf4c57585a7d61a5f621ae5b67240f4484c5))

## 0.5.1 (2025-08-15)


### Features

* Add checks for secret existence to all workflows ([#727](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/727)) ([a89cddb](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a89cddb31bc900f5088acb4bd07d57f3ee13d99e))


### Bug Fixes

* Fix copier-update mise task ([#724](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/724)) ([65c61da](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/65c61da528de566f602a06471e4744414408a68d))
* Fix template update github workflow ([#726](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/726)) ([b2c233a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b2c233a3d557a70d5634de771a3c5bf578259816))
* Fix template-update-check azdo pipeline ([#728](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/728)) ([dbc7d9a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/dbc7d9ad706d4fdf462de66baf00af68aa81fab8))
* Rename to copier-update-check ([#729](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/729)) ([4a066ef](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4a066ef9ef1feb7ced6f33f27ab1c5a82289b872))

## 0.5.0 (2025-08-14)


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

## 0.4.4 (2025-06-24)


### Bug Fixes

* Wrap custom manager code in raw tags ([#640](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/640)) ([5f6cd4b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5f6cd4b89ce36e573b829f600351847bdd3824e8))

## 0.4.3 (2025-06-24)


### Bug Fixes

* Backport config changes into template ([#638](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/638)) ([fc64a6b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/fc64a6b45781de02c628ad3a389c6132ed263078))

## 0.4.2 (2025-06-24)


### Bug Fixes

* Wrap double brackets in raw tag ([#636](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/636)) ([f563902](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f56390247b5fc48f1410a258121df8323029dc19))

## 0.4.1 (2025-06-20)


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

## 0.4.0 (2025-06-18)


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

## 0.3.47 (2025-06-02)


### Bug Fixes

* Set fetch-depth to 0 to support hk ([#561](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/561)) ([1dd03c2](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1dd03c294a8d061d627d6e4a64a27262c78a75ce))

## 0.3.46 (2025-06-02)


### Bug Fixes

* Don't lint azure pipelines yaml files ([def2560](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/def256020899a6eeea6d9d280da8b85096ab9e43))
* Fix azdo copier update pipeline ([200d952](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/200d95240c11b2994418a1a23514624a308bd397))
* Fix azdo copier updating pipeline ([12471b0](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/12471b05ca5aa5cc8f82fc67c9246fcad4a875d6))
* Fix hk to properly run on PRs ([#559](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/559)) ([6c581a6](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6c581a659ae56f2c747d2906147cf3f2cee24705))

## 0.3.45 (2025-06-02)


### Features

* Improve logging for mise postinstall hooks ([fe2eed3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/fe2eed344153fab4319b41ab5b6be465852662d2))
* Improve logging for mise postinstall hooks ([9a8f4ac](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9a8f4ac6f7e55d64c5f99e1b99c19aa5023fcf8c))

## 0.3.44 (2025-06-02)


### Bug Fixes

* Change to always use token for first git push ([b2f575b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b2f575b8b2c172721798b885582e47ada77ba71e))
* Change to always use token for first git push ([a7cb007](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a7cb007063a28b9e54e8c3f4c85924328e3488af))
* Clean up git credentials settings ([5b5220d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5b5220d7899120ca4820ce8d0d20d0d7d09425ee))
* Clean up git credentials settings ([5d4cab0](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5d4cab02405b940ea4ff6bd7218e9f427e265996))

## 0.3.43 (2025-06-02)


### Features

* Copier update to parent template v0.3.42 ([dea71ff](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/dea71ffb6a05f053d663cd0a46141d0d9b03eda9))
* Copier update to parent template v0.3.42 ([7b328f6](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7b328f675d6f42d1c694f394cb54eb79c252f6ad))
* Replace phase_extension.py with _copier_operation ([73519d8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/73519d8c0d58a9d0548b5ced708d9c642189b316))
* Replace phase_extension.py with _copier_operation ([f26646d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f26646d4654fd46e0ed6874de7542cc5e39927c6))

## 0.3.42 (2025-06-02)


### Bug Fixes

* Fix template structure issues ([beae721](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/beae72174637cd8207f81927bdbe350e73f599c5))
* Fix template structure issues ([609a61b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/609a61b28e9dbbdd91e0b092e8768cb85a2c31e9))

## 0.3.41 (2025-06-02)


### Bug Fixes

* Activate venvs as needed ([26fd914](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/26fd914dba1f348de682b4e93093623d951c230a))
* Add necessary invoke dependency for copier ([7099a1a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7099a1a6f280dd4880d70253d2b2f2d819130e4d))
* Switch copier workflows to pure bash ([3a81c49](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3a81c498c95563d2fa34c4188d234910713ac52a))
* Switch copier workflows to pure bash ([81b4b15](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/81b4b1502d271d4bdfc045c10b142aeef455025d))

## 0.3.40 (2025-06-02)


### Features

* Copier update to parent template v0.3.39 ([c9b34cc](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c9b34cc63a2e9e1c6c453f6408c78f857ac05453))
* Copier update to parent template v0.3.39 ([f9e24af](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f9e24afee6c79c97770fec2f62ed93385d22ea98))
* Update copier update workflows to use mise ([e19976d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e19976db2f01c7abc043c548f3b70d512af12936))
* Update copier update workflows to use mise ([aa2fa33](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/aa2fa33a597398c3301638d27a572c6e57da2b88))


### Bug Fixes

* Fix errors in template ([90479ad](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/90479ad0c57d1432d5da25a673f5cc855f1c50f6))
* Fix errors in template ([335d910](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/335d910e1fd26a1dadca9169bfbc7a4b1c298f97))

## 0.3.39 (2025-06-02)


### Bug Fixes

* Fix jinja errors in template ([52060a6](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/52060a646a3ad303b8e3cfcb7995a862a4bfbf7b))
* Fix jinja errors in template ([5916961](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5916961b04c0f84897f4a755d3124d901c2a71e3))

## 0.3.38 (2025-06-02)


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

## 0.3.37 (2025-01-09)


### Features

* Improve logging for azure pipeline creation ([f6244c4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f6244c4d893dbb97059fa40cac2730c54bcfc02e))
* Overhaul trunk linters ([4d4f485](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4d4f4852d55c100a9f14e013db4e20304c002507))
* Update cspell words ([6129917](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/61299171d516c1214f618969455434ee9c2a7c8e))

## 0.3.36 (2025-01-09)


### Features

* Improve repo_actions help ([1e7f854](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1e7f8541acc1962b1e3c845c633fb478b5563957))


### Bug Fixes

* Fix azdo_org question ([7887895](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7887895d9dd069d3ba5d96c0db2b3f71596849b7))

## 0.3.35 (2025-01-09)


### Features

* Add repo_actions validators ([1736b3f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1736b3f7f97ec13617c8eadc17213aca9338a661))

## 0.3.34 (2025-01-09)


### Features

* Copier update to parent template v0.3.33 ([ed5ed64](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ed5ed6402ed11e35816657f9c9f7b6faf96f46cc))


### Bug Fixes

* Fix credential file creation ([0bbd0f3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0bbd0f33aeaebe529a4e221311af5a8780f55752))

## 0.3.33 (2025-01-09)


### Features

* Improve question help ([4fc9be2](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4fc9be2ad612a4e1cf6a11be780f47adfb0555a2))

## 0.3.32 (2025-01-09)


### Bug Fixes

* Fix other yaml validity issue ([3dd58f8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3dd58f8a3371756aee49e8eede3f6a25f3e96e99))
* Fix yaml validity issue ([d6f8ed4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d6f8ed4803f88bab35843c22205d8cf913858ea2))

## 0.3.31 (2025-01-09)


### Features

* Improve structure of questions ([a40f7ab](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a40f7abd1db3f860708daafd52a2b29eaf74117b))

## 0.3.30 (2025-01-09)


### Bug Fixes

* Fix path extension copies ([db5ba3c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/db5ba3c2e992623b45d1d177e7ec6795c8fbee5a))

## 0.3.29 (2025-01-09)


### Bug Fixes

* Refactor cwd_name function ([008cb79](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/008cb79e34cc2428b404f7419cf75ebc52be0b72))

## 0.3.28 (2025-01-09)


### Bug Fixes

* Fix bad extensions definition ([7f06478](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7f06478bdf62b056ece2ee856f056060312b90cc))

## 0.3.27 (2025-01-09)


### Bug Fixes

* Fix cwd_name ([e69bf2f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e69bf2f995a2d2c901e214fd106eacf9c8919912))

## 0.3.26 (2025-01-09)


### Features

* Move repo name question first ([d19a289](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d19a289ed4a19429810b315074a8ee8916e2b36b))

## 0.3.25 (2025-01-09)


### Bug Fixes

* Fix cwd_name function ([84c5215](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/84c521524a91352cb9da1bd06fd15a83895a9167))

## 0.3.24 (2025-01-09)


### Features

* Copier update to parent template v0.3.23 ([5d5c0ee](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5d5c0eebb0c5278d6cc3bb602eb24e3124538ddb))


### Miscellaneous

* **deps:** Update ghcr.io/natescherer/postmodern-tools-container:latest docker digest to f56e2b1 ([18587e1](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/18587e19870503b0b7174b9734b78af413e1c559))

## 0.3.23 (2025-01-09)


### Features

* Add default for repo_name question ([29dbfa9](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/29dbfa940396d167cb8570690c8703050131b84a))
* Copier update to parent template v0.3.22 ([e70de2c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e70de2cb0aa47b232a04daf336a46f37f6994e3e))

## 0.3.22 (2025-01-09)


### Bug Fixes

* Fix template devcontainer.json ([0ac2f81](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0ac2f8143148c2d2efdb769d802f9395090a7f69))

## 0.3.21 (2025-01-09)


### Bug Fixes

* Disable pinning for devcontainer features ([6825179](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/68251792e2050c95be6ff20a5a53df30618e55fd))
* Fix copier update workflow ([#462](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/462)) ([e3fe6f6](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e3fe6f6a55859eb8afbd4ec15b0fdab488ff1365))
* Make release please config a template ([9e0b7e2](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9e0b7e259dfbf5605afded37e81e8f7037581522))

## 0.3.20 (2025-01-08)


### Features

* Copier update to parent template v0.3.19 ([2e20189](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2e201894737590759b186f5c978ad76a953ef2a4))
* Update release please config to include chores ([f48a6d5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f48a6d5066f9c464b6511a9e6543c772eba3c091))
* Use postmodern-tools-container ([1afe85b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1afe85bc9d8191d89cb6c34153d2999056ac35e2))


### Miscellaneous

* **deps:** Pin dependencies ([63c51a4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/63c51a400648dcc3b779f2ddb4b32afe58392274))
* Fix merge conflict ([44d0d09](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/44d0d099e9dfa3b838009ceb1040738cc77ea024))

## 0.3.19 (2024-12-31)


### Features

* Have release please run with pat ([4a65522](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4a655228a5ad797c794fc65416af34a67e02c892))

## 0.3.18 (2024-12-31)


### Features

* Copier update to parent template v0.3.17 ([9e43de8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9e43de88470df98e33c6058f2937c7929cef28b2))

## 0.3.17 (2024-12-31)


### Features

* Add infisical to cspell dictionary ([c9686ab](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c9686ab0e1be97d1eb80360eba0cac1b08c102e9))
* Switch to using REPO_MAINTENANCE_PAT secret ([dedc2f7](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/dedc2f758432c8a69d68580ea064e313a032c9a6))

## 0.3.16 (2024-12-31)


### Features

* Copier update to parent template v0.3.15 ([e6e1e32](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e6e1e32e4d8cf2ff2d51980562b37d933b2ce332))
* Update cron schedules for workflows ([8c6fffc](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8c6fffceadbf54bd5a52c5e4a4577814877bd02b))

## 0.3.15 (2024-12-31)


### Features

* Copier update to parent template v0.3.14 ([fbd41ba](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/fbd41baa94238dedea701e0e5ae415953e14c2ac))


### Bug Fixes

* Fix os.getenv ([2a6f711](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2a6f7115fb3297a1c4da7e64ab2a634510e4ed82))

## 0.3.14 (2024-12-31)


### Features

* Add workflow for upgrading trunk ([b64ca97](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b64ca9774d35f9e9da9f9a568cb7f93fa2018f31))


### Bug Fixes

* Fix naming of trunk upgrade prs ([531e451](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/531e45130369a879aef06fae6f5d3ea2ea120023))
* Fix repo creation credential setting ([21eae37](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/21eae37023af83ad1bd53c24ccc7e645f8477d2b))
* Fix trunk testing for prs ([91cc9bb](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/91cc9bb57e8fd354cce082cf8243ea745645c7f0))
* Fix trunk workflows ([4ece49e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4ece49e693841c3a694b0faf3021b065603661a4))
* Force pr tests to save trunk annotations ([217e1bb](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/217e1bb20dd5c6be11057deb7065446f3bbb9acb))
* Update trunk check workflows ([f585c7d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f585c7d8b0cbcb3817f267452b7273e91a07ccb6))

## 0.3.13 (2024-12-31)


### Bug Fixes

* Actually fix trunk for prs ([d768c98](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d768c9877dcc557911fad61fedc69bdc0a50f3b4))
* Fix checkout action version ([65e2300](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/65e23004a70df2f83ddd5e136976ad587bc3cc57))
* Fix trunk testing on PRs ([75abbfb](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/75abbfb27a4ec0a80d83c758fc8014e8e3a4ebc3))

## 0.3.12 (2024-12-31)


### Bug Fixes

* Disable renovate dependency dashboard ([51c941f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/51c941f5ae5efc3265e5038dae6575857b02d42b))
* Fix bad jinja syntax ([5517bbb](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5517bbbf917e6c4714e629fa063198635bf8303e))

## 0.3.11 (2024-12-31)


### Features

* Add renovate config to downstream templates ([2eef993](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2eef9932ab471b84ba71f2039dbdd9e5fc572c32))

## 0.3.10 (2024-12-31)


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

## 0.3.9 (2024-11-04)


### Bug Fixes

* Don't use encoded git tokens ([4451416](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4451416fc31245e9ac285cc1362b99252b4ba219))

## 0.3.8 (2024-11-04)


### Bug Fixes

* Fix git cred file path ([bc3f06a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/bc3f06a518e5fdaf64a6b23b41fdcb60004eaa1b))

## 0.3.7 (2024-11-04)


### Bug Fixes

* Fix open mode for credential file ([1994441](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/19944413cfc84c78863dec33a83ad7ea2109b451))

## 0.3.6 (2024-11-04)


### Features

* Add cred handling for docker ([f03b4fd](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f03b4fd3ed2cbe27ea3ecd11c6a89ce2b82e8d9c))
* Apply parent template v0.3.5 ([6dcc9eb](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6dcc9eb7f314deeb11ad91d290f5476f0d332a8c))


### Bug Fixes

* Fix yaml formatting on azdo cron schedule ([414a245](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/414a2455afd11a87187d1ba6176f1ba0f3b04521))

## 0.3.5 (2024-11-01)


### Features

* Add copier update workflow for Azure DevOps ([b448721](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b448721e261fd165ccb09f0dec016b42e05ac928))

## 0.3.4 (2024-11-01)


### Bug Fixes

* Fix payload for azdo pipeline creation ([ee2ddf7](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ee2ddf7212ab62b420bf7579086d28b15d183352))

## 0.3.3 (2024-11-01)


### Bug Fixes

* Fix pipeline naming for azdo ([9a00ce8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9a00ce8ff7a0738b766c6c4465724b891af664a2))

## 0.3.2 (2024-11-01)


### Features

* Add vscode associations for azure pipelines ([5162a29](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5162a29a93cdba7d4d4c769e5b8095135696b5bd))
* Allow create_pipelines_azdo task to dynamically register multiple pipelines ([0ab6b1d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0ab6b1d3904939f611a03bb23838e1e5bac71d17))
* Copier update to parent template v0.3.1 ([0c85845](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0c8584504f07a095b7da969dfe9c98fe183d0143))

## 0.3.1 (2024-11-01)


### Features

* Apply parent template v0.3.0 ([f0fcc6f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f0fcc6f4089f30257266dd1bb4531e3c9fa9b050))
* Improve azdo release pipeline ([4c75e72](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4c75e7206ad82238e46bcd162db656ad614f6817))


### Bug Fixes

* Port azdo workflow improvements from test repo ([983558d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/983558d35c163d2a841c79eb6b82ab46327c23af))

## 0.3.0 (2024-10-23)


### ⚠ BREAKING CHANGES

* all-contributors and dependabot PRs will no longer automatically merge

### Features

* Remove automerge workflow on PRs ([653d9dc](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/653d9dcb31ad566651a65b49ae061b0764df04b5))


### Bug Fixes

* Fix formatting issues in template ([2cf9df2](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2cf9df23ef6f243f6df539a30b54d3d9475bfe74))

## 0.2.47 (2024-10-23)


### Features

* Copier update to parent template v0.2.46 ([34f31fe](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/34f31fe6bf1c5ff9242ad2debfba58304ec8cc63))


### Bug Fixes

* Don't create public workflows for private gh repos ([c4279da](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/c4279da97e8804e33567b7bdaf016690ea985f08))
* Fix trunk check prs (closes [#316](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/316)) ([0191943](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0191943b9e2bad400a22d83ab240c77d42c2bfe9))

## 0.2.46 (2024-10-23)


### Features

* Copier update to parent template v0.2.45 ([9b169fe](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9b169fe08a7830c5b623843f5d6a1fab690e4e4a))


### Bug Fixes

* Fix extension recs in template ([7fe3770](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/7fe3770f597a695a5ee6188f742134241091632d))

## 0.2.45 (2024-10-18)


### Bug Fixes

* Add extension definition ([1fc1b1e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1fc1b1e1530b2ee15320c92295fa45e67e05cb68))

## 0.2.44 (2024-10-18)


### Bug Fixes

* Add missing extension file ([f1ec90c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f1ec90c17517917d0de274783a73c1e17b016353))

## 0.2.43 (2024-10-18)


### Features

* Copier update to parent template v0.2.42 ([83bca46](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/83bca468e57852fd5678b1df5d30de4feb61cf26))


### Bug Fixes

* Make parent_template_name question input-safe ([a32c6b3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a32c6b3fe6fcfdebc51d268100132a36b77c2ebb))

## 0.2.42 (2024-10-18)


### Features

* Add scherer back into cspell words ([8e8d625](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8e8d62581bc83b9c6a2db646a7a3f8433a9c8c45))
* Apply linting updates from trunk ([0ed8a98](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0ed8a9807320dd29f19d91967438e5709a75eb47))
* Copier update to parent template v0.2.41 ([9d15582](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9d15582b0514802a2542dfbefb6607e9bfb7fb71))
* Improve spell checking ([5942041](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/59420419134ee9a24a93ed0ca35572c95d5af012))
* Update trunk, cspell, and ruff ([500e594](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/500e59419306ec93d0cc358700456a908231c9a1))

## 0.2.41 (2024-10-18)


### Bug Fixes

* Ensure CHANGELOG.md exists for created projects so trunk doesn't error out ([b5e3048](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b5e304881a81cdfad3bd4be6064d3157727b3afd))
* Fix yamllint config for templates ([4a472e8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4a472e83fe0ba0c3a0d69386ad24cd4bd7369662))

## 0.2.40 (2024-10-13)


### Features

* Replace bash dict with shell dict in cspell config ([f6bb0a2](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f6bb0a2c1b6ebf7ae86caef6bdfb1caf09aa3961))


### Bug Fixes

* Clean up template to not deploy template-only settings for regular projects ([b696349](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b696349e1526e256a44d674a93ec004b17692b87))

## 0.2.39 (2024-10-12)


### Features

* Copier update to parent template v0.2.38 ([204dfdd](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/204dfdd22ee9d66b1e7ebfaab66d57ebfa58553c))


### Bug Fixes

* Only use actionlint on github projects ([37dce71](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/37dce71701ce3a862d6065bdefb3cf3628c79a8d))

## 0.2.38 (2024-10-12)


### Features

* Copier update to parent template v0.2.37 ([b71857c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b71857cc0f65d399a3776955480888b5c503bdcf))
* Remove unneeded node feature ([5937100](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/59371005dc9315ed3c5c2a3fc45f3426e48bb9c8))

## 0.2.37 (2024-10-12)


### Bug Fixes

* Fix dynamic plugin logic ([4c9e37c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4c9e37c7ff60d05aed6eca2aa9bc507021708454))

## 0.2.36 (2024-10-12)


### Features

* Copier update to parent template v0.2.35 ([910e011](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/910e011a8ab6dfe1ac75eba0d7b4f04625206cce))
* Make plugins dynamic ([70d2070](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/70d2070500ea4e5df45963f7e7cca91e5677a9c3))


### Bug Fixes

* Add natescherer back to cspell ([fd466ba](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/fd466ba060f73add8fdc1b9ebf63c33e23b3ad9a))

## 0.2.35 (2024-10-12)


### Features

* Update cspell settings ([49c2825](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/49c282580bf5a5395652e59bf2881e54d92f4432))
* Update trunk ([792b08e](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/792b08eb800cb01406a41c15b8919440f50f7b25))


### Bug Fixes

* Fix devcontainer home mount ([1e58765](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/1e58765afd7eae8a1d1525c342551a44a414f722))

## 0.2.34 (2024-10-12)


### Features

* Add built-in slugify extension (closes [#300](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/300)) ([9feadb5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9feadb5b1f1463b7c0f3c0a0f89c8449bc935d4d))
* Copier update to parent template v0.2.33 ([b03ee51](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/b03ee51865cde019b0af3cf615f8f523535d9e6b))

## 0.2.33 (2024-10-12)


### Bug Fixes

* Fix copier update workflow formatting ([eab7839](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/eab78391cf3fadf12d1e753a6c350707aef28129))

## 0.2.32 (2024-10-12)


### Bug Fixes

* Fix NEW_VERSION calculation in copier update workflow ([5ee3e2d](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5ee3e2d37932ffedd5a94787a8fccd289e5bbfd1))

## 0.2.31 (2024-10-12)


### Bug Fixes

* Fix branch name ([064f75a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/064f75a568121a7ced480054948ce08a85c9d9f1))

## 0.2.30 (2024-10-12)


### Features

* Fix mount permission issues on windows hosts ([0d12cc9](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0d12cc901cbc7e7240fec8039f281cc819b2dc63))
* Improve template update workflow ([0a497ff](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/0a497ff28abded831b80a81fe9b52d982db7434e))

## 0.2.29 (2024-10-12)


### Bug Fixes

* Update base image in template ([e75ca21](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e75ca2103b98cb074d30b20d5ff875cf9c9bbabb))

## 0.2.28 (2024-10-12)


### Features

* Bump devcontainer base image ([9ff6950](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9ff695093c16b44517bc68b2b5127e4e772dc049))

## 0.2.27 (2024-09-25)


### Features

* Add more cSpell dictionaries ([a3e81c5](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/a3e81c5aebe17468e480f08db1c50b06249a8852))

## 0.2.26 (2024-09-25)


### Bug Fixes

* Fix readme format ([d2a84c1](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/d2a84c1ed0b1785c615a3080ba71a8c18c1e15c5))

## 0.2.25 (2024-09-25)


### Bug Fixes

* Fix formatting issues from downstream ([e6d899a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e6d899aecba8ab0afe8bd751d759028196382766))

## 0.2.24 (2024-09-25)


### Bug Fixes

* Fix versionrc formatting ([e20724c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e20724c9200fbacaad6bb1da2e572ea0fa3cfcfd))

## 0.2.23 (2024-09-25)


### Bug Fixes

* Fix readme formatting ([69a1bbd](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/69a1bbdd0e6fac30c4dd86765481b135072ef76f))

## 0.2.22 (2024-09-25)


### Bug Fixes

* Fix formatting issues found downstream ([838a5db](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/838a5db116de3f4b85423711c75f3a0bdfa37c7a))

## 0.2.21 (2024-09-25)


### Bug Fixes

* Dynamic trunk ignores ([4e01eb9](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/4e01eb9a6fd53a58fc818bcbcd696486db5c93f3))

## 0.2.20 (2024-09-25)


### Features

* Apply parent template v0.2.19 ([199bef3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/199bef320336cc67d2ca20d7ffbe305cbf5b01b5))

## 0.2.19 (2024-09-25)


### Bug Fixes

* Bump minimum copier version ([2d0bd03](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/2d0bd030c337f10bf66a584df55d1cd19c7bb4e5))

## 0.2.18 (2024-09-25)


### Features

* Skip linting/formatting on release please manifest ([8eae6f3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8eae6f34b2c30fa6b5f9a51fc768b372714f6dc6))

## 0.2.17 (2024-09-25)


### Bug Fixes

* Fix release please formatting ([32b0c7a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/32b0c7af654dde897639b2b343d46a11a76cb5d1))

## 0.2.16 (2024-09-25)


### Features

* Add pscore to dictionary ([ec0d937](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ec0d937d3cf22e7306546dae6238144772d63e02))

## 0.2.15 (2024-09-25)


### Bug Fixes

* Fix link format ([f98121a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f98121aec0c2dff73e300af21de57df6404fe133))

## 0.2.14 (2024-09-25)


### Features

* Apply v0.2.13 ([f81b0b9](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f81b0b929d71fb48cebfff1efa9498bc636ca600))
* Improve formatting ([f3cf8f3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f3cf8f3875334edf342ca8eaf305f08b8bd474a1))

## 0.2.13 (2024-09-25)


### Bug Fixes

* Fix readme formatting ([e6fdd30](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e6fdd30d86a9b6df82cc3d585e59a4911997c271))

## 0.2.12 (2024-09-25)


### Bug Fixes

* Fix doc templates ([f3227c3](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f3227c3ce605cf37665346240f335ee596fbee1c))

## 0.2.11 (2024-09-25)


### Bug Fixes

* Remove unneeded ignore ([5425d18](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5425d18c8db7d9a3a69342ad77e554aa2f8e774c))

## 0.2.10 (2024-09-25)


### Bug Fixes

* Fix bad formatting on dependabot template ([e00510c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e00510c21d3e3c6f21dbddc1b350ff973804d782))

## 0.2.9 (2024-09-25)


### Features

* Add dependabot grouping (closes [#6](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/6)) ([6dee4bb](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6dee4bb415f7c52e6d5b937fcb223541165215e1))
* Add devcontainers to dependabot (closes [#8](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/8)) ([298ffe7](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/298ffe717e0812062b5a332efe7e55a70f26a8aa))


### Bug Fixes

* Add commitlint config to template ([3f2684b](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/3f2684be64b974f11ba100955efb517cafe75d83))
* Fix yaml format ([9cb2bb8](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/9cb2bb87cbcd04938e45769f8d9955f5597c9358))

## 0.2.8 (2024-09-25)


### Features

* Add toml vscode plugin ([ed3c986](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/ed3c986e4949c52e886e3a884186025a0c7a91fa))

## 0.2.7 (2024-09-25)


### Features

* Apply parent template v0.2.6 ([30796a4](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/30796a4ef1ff154cebd409ff3b540f8b697daefd))


### Bug Fixes

* Fix trunk nits ([49f36bc](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/49f36bc981cd1d1aa6b516cee7c869ad956a94eb))

## 0.2.6 (2024-09-25)


### Bug Fixes

* Fix jinja conditionals ([8144c49](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/8144c498beb7826f2be9e283767ce322760c55b8))

## 0.2.5 (2024-09-25)


### Features

* Remove unneeded workflows ([17a5a4a](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/17a5a4ac6e8675eb5992c13cf2f28d8d4a50333e))


### Bug Fixes

* Fix task conditionals in root copier.yml ([cdc3d4c](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/cdc3d4c89e9653da714c8767f4d2147a5e17dab4))

## 0.2.4 (2024-09-25)


### Bug Fixes

* Fix conditionals on copier tasks ([5d7baad](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5d7baad1154b7ad2ce532503c7ea7e8a055fbc21))

## 0.2.3 (2024-09-25)


### Features

* Apply trunk quality and formatting ([cb66c16](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/cb66c165720a4f6e5cc9f2942c7f3a4f4a3112a0))
* Change devcontainer mount (closes [#211](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/211)) ([78e3353](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/78e335346322ba10d9df5202122287c4ee808154))
* Implement trunk ([e711206](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e711206352ae9fdc9f792a3cb6eb88a117ee6366))

## 0.2.2 (2024-09-24)


### Features

* Ensure devcontainer folder is made for all projects ([e5ae1c7](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/e5ae1c7dd6014bc8f78c371735fd0c78eb7eb5b9))

## 0.2.1 (2024-09-24)


### Features

* Update vscode extensions ([5e46c4f](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/5e46c4f186f7c580c4562e8821edb8f483e51b90))


### Bug Fixes

* Fix license file ([6fc1d10](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/6fc1d10c628cc1843abd7e55ac0dc31dbf8847fe))
* Fix pull request ruleset settings (closes [#221](https://github.com/natescherer/postmodern-repo-copiertemplate/issues/221)) ([f882058](https://github.com/natescherer/postmodern-repo-copiertemplate/commit/f882058927b4b73c437857fd1f2814bd23aab3cf))

## 0.2.0 (2024-09-23)


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
