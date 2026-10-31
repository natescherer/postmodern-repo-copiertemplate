"""Boundary answer combinations shared by every test module in this directory.

Edit this file when you add, remove, or rename a Copier question in copier.yml. Each
entry should be a reachable combination that respects copier.yml's `when:` and
`validator:` constraints (`Public` with `MIT` isn't valid on Azure DevOps, for example)
and exercises a distinct rendering path. An entry using a value the last release doesn't
accept also needs `_old_tag_overrides` (see test_update_from_last_tag). This file is
repo-specific by design; the test modules that use it (conftest.py, test_render.py,
test_content.py, ...) aren't.
"""

COMMON = {
    # Never touch a real repo/API during a render test.
    "repo_setup_actions": "None",
    "project_name": "Render Test",
    "repo_name": "render-test",
    "author_name": "Test Author",
    "project_description": "Rendering test project",
}

ANSWER_MATRIX = [
    {
        "id": "github-template-public-mit-ghpages-prealpha",
        **COMMON,
        "developer_platform": "GitHub",
        "github_username": "octocat",
        "project_type": "Template",
        "extensible_template": True,
        "project_visibility": "Public",
        "license": "MIT",
        "zensical_target": "GitHub Pages",
        "lifecycle": "Pre-Alpha",
        "code_coverage": True,
    },
    {
        "id": "github-standard-private-none-docs-site-stable",
        **COMMON,
        "developer_platform": "GitHub",
        "github_username": "octocat",
        "project_type": "Standard",
        "project_visibility": "Private",
        "license": "None",
        "zensical_target": "docs-site Directory in Repo",
        "lifecycle": "Stable",
        "code_coverage": True,
    },
    {
        # The only GitHub Template that builds docs into the repo (docs_base()'s
        # blob/main/docs/ branch), the only entry with a GitHub organization, and the
        # only leaf template. On update, extensible_template isn't asked and defaults to
        # true for an existing project, so _old_tag_overrides passes false back in.
        "id": "github-template-public-mit-docs-site-beta",
        **COMMON,
        "developer_platform": "GitHub",
        "github_username": "octocat",
        "github_org": "test-org",
        "project_type": "Template",
        "extensible_template": False,
        "_old_tag_overrides": {"extensible_template": False},
        "project_visibility": "Public",
        "license": "MIT",
        "zensical_target": "docs-site Directory in Repo",
        "lifecycle": "Beta",
    },
    {
        "id": "github-standard-public-none-ghpages-inactive",
        **COMMON,
        "developer_platform": "GitHub",
        "github_username": "octocat",
        "project_type": "Standard",
        "project_visibility": "Public",
        "license": "None",
        "zensical_target": "GitHub Pages",
        "lifecycle": "Inactive",
        "agent_instructions": False,
    },
    {
        "id": "azdo-template-private-docs-site-beta",
        **COMMON,
        "developer_platform": "Azure DevOps",
        "azdo_org": "test-org",
        "azdo_project": "Test Project",
        "project_type": "Template",
        "extensible_template": True,
        "project_visibility": "Private",
        "license": "None",
        "zensical_target": "docs-site Directory in Repo",
        "lifecycle": "Beta",
        "code_coverage": True,
    },
    {
        "id": "azdo-standard-private-docs-site-alpha",
        **COMMON,
        "developer_platform": "Azure DevOps",
        "azdo_org": "test-org",
        "azdo_project": "Test Project",
        "project_type": "Standard",
        "project_visibility": "Private",
        "license": "None",
        "zensical_target": "docs-site Directory in Repo",
        "lifecycle": "Alpha",
    },
]

# Combinations copier.yml.jinja's `validator:` blocks should reject; test_validators.py
# checks that they do. Each entry's `expected_error` is a substring of Copier's
# "Invalid choice for '<question>': <validator message>".
INVALID_ANSWER_MATRIX = [
    {
        "id": "azdo-public-visibility-rejected",
        **COMMON,
        "developer_platform": "Azure DevOps",
        "azdo_org": "test-org",
        "azdo_project": "Test Project",
        "project_visibility": "Public",
        "license": "None",
        "zensical_target": "docs-site Directory in Repo",
        "lifecycle": "Pre-Alpha",
        "expected_error": "Not Supported on Azure DevOps: choose Private",
    },
    {
        "id": "private-mit-license-rejected",
        **COMMON,
        "developer_platform": "GitHub",
        "github_username": "octocat",
        "project_visibility": "Private",
        "license": "MIT",
        "zensical_target": "GitHub Pages",
        "lifecycle": "Pre-Alpha",
        "expected_error": "Not Supported on Private repos: choose None",
    },
    {
        "id": "azdo-ghpages-target-rejected",
        **COMMON,
        "developer_platform": "Azure DevOps",
        "azdo_org": "test-org",
        "azdo_project": "Test Project",
        "project_visibility": "Private",
        "license": "None",
        "zensical_target": "GitHub Pages",
        "lifecycle": "Pre-Alpha",
        "expected_error": (
            "Not Supported on Azure DevOps: choose docs-site Directory in Repo"
        ),
    },
    {
        # repo_name lands unquoted in shell-string tasks (gh repo create, git remote
        # add, az pipelines create), so anything outside this set would break them.
        "id": "repo-name-with-space-rejected",
        **COMMON,
        "repo_name": "render test",
        "developer_platform": "GitHub",
        "github_username": "octocat",
        "project_visibility": "Public",
        "license": "MIT",
        "zensical_target": "GitHub Pages",
        "lifecycle": "Pre-Alpha",
        "expected_error": "Repo names may only contain letters, digits",
    },
    {
        "id": "project-name-with-quote-rejected",
        **COMMON,
        "project_name": 'Render "Test"',
        "developer_platform": "GitHub",
        "github_username": "octocat",
        "project_visibility": "Public",
        "license": "MIT",
        "zensical_target": "GitHub Pages",
        "lifecycle": "Pre-Alpha",
        "expected_error": "The project name can't contain",
    },
    {
        "id": "project-description-with-backslash-rejected",
        **COMMON,
        "project_description": "Renders C:\\path docs",
        "developer_platform": "GitHub",
        "github_username": "octocat",
        "project_visibility": "Public",
        "license": "MIT",
        "zensical_target": "GitHub Pages",
        "lifecycle": "Pre-Alpha",
        "expected_error": "The project description can't contain",
    },
    {
        "id": "azdo-set-repo-rules-rejected",
        **COMMON,
        "repo_setup_actions": "Set Repo Rules",
        "developer_platform": "Azure DevOps",
        "azdo_org": "test-org",
        "azdo_project": "Test Project",
        "project_visibility": "Private",
        "license": "None",
        "zensical_target": "docs-site Directory in Repo",
        "lifecycle": "Pre-Alpha",
        "expected_error": "Not Supported on Azure DevOps: choose None",
    },
]

# Questions test_answer_matrix_coverage.py's choices-completeness check should skip,
# with the reason it's a deliberate gap rather than an oversight.
COVERAGE_EXEMPT_QUESTIONS = {
    # "Create Repo" and "Set Repo Rules" only decide which _tasks run (real GitHub or
    # Azure DevOps API calls); they don't change rendered files, and this suite skips
    # tasks. COMMON sets "None" everywhere to keep the tests offline.
    "repo_setup_actions",
}
