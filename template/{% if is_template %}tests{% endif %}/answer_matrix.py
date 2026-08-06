"""Boundary answer combinations used by test_template_render.py.

Edit this file when you add, remove, or rename a Copier question in copier.yml -- each
entry should be a real, reachable combination (respecting copier.yml's
`when:`/`validator:` constraints, e.g. `Public` + `MIT` isn't valid on Azure DevOps)
that exercises a distinct rendering path. This file is repo-specific by design;
test_template_render.py itself is not.
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
    },
    {
        "id": "github-standard-private-none-docs_site-stable",
        **COMMON,
        "developer_platform": "GitHub",
        "github_username": "octocat",
        "project_type": "Standard",
        "project_visibility": "Private",
        "license": "None",
        "zensical_target": "docs_site Directory in Repo",
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
    },
    {
        "id": "azdo-template-private-docs_site-beta",
        **COMMON,
        "developer_platform": "Azure DevOps",
        "azdo_org": "test-org",
        "azdo_project": "Test Project",
        "project_type": "Template",
        "project_visibility": "Private",
        "license": "None",
        "zensical_target": "docs_site Directory in Repo",
        "lifecycle": "Beta",
    },
    {
        "id": "azdo-standard-private-docs_site-alpha",
        **COMMON,
        "developer_platform": "Azure DevOps",
        "azdo_org": "test-org",
        "azdo_project": "Test Project",
        "project_type": "Standard",
        "project_visibility": "Private",
        "license": "None",
        "zensical_target": "docs_site Directory in Repo",
        "lifecycle": "Alpha",
    },
]
