"""Boundary answer combinations shared by every test module in this directory.

Edit this file when you add, remove, or rename a Copier question in copier.yml; each
entry should be a real, reachable combination (respecting copier.yml's
`when:`/`validator:` constraints, e.g. `Public` + `MIT` isn't valid on Azure DevOps)
that exercises a distinct rendering path. This file is repo-specific by design; the
test modules that consume it (conftest.py, test_render.py, test_content.py, ...) are
not.
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

# Combinations copier.yml.jinja's `validator:` blocks are supposed to reject, used by
# test_validators.py to confirm those guardrails actually work, not just that valid
# combinations render. Each entry's `expected_error` is the substring Copier's
# "Invalid choice for '<question>': <validator message>" is expected to contain.
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
        "expected_error": "Not Supported on Azure DevOps",
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
        "expected_error": "Not Supported on Private repos",
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
        "expected_error": "Not Supported on Azure DevOps",
    },
]

# Questions test_answer_matrix_coverage.py's choices-completeness check should skip,
# with the reason it's a deliberate gap rather than an oversight.
COVERAGE_EXEMPT_QUESTIONS = {
    # "Create Repo"/"Set Repo Rules" only gate which _tasks run (real GitHub/Azure
    # DevOps API calls via should_create_repo/should_set_repo_settings); they never
    # affect rendered file content, and this suite always renders with --skip-tasks.
    # COMMON pins this to "None" everywhere specifically to keep tests offline.
    "repo_setup_actions",
}
