# This file is designed to be run once from a local machine where the gh cli is authenticated as the user

echo "Setting Repo Settings..."
gh api '/repos/{owner}/{repo}' --silent --method PATCH -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" -f description='Here is a short description.' -f homepage='{{cookiecutter.project_website}}' -F allow_auto_merge=true -F delete_branch_on_merge=true

echo "Creating labels..."
gh label create "awaiting pr" -d "Awaiting completion of a PR from a contributor" -c 668F04 -f
gh label create blocked -d "Blocked by an external dependency" -c B60205 -f

echo "Setting up default branch protection ruleset..."
echo '{"bypass_actors":[],"conditions":{"ref_name":{"exclude":[],"include":["~DEFAULT_BRANCH"]}},"enforcement":"active","name":"default-branch-protection","rules":[{"type":"deletion"},{"type":"non_fast_forward"},{"dismiss_stale_reviews_on_push":false,"require_code_owner_review":false,"require_last_push_approval":false,"required_approving_review_count":0,"required_review_thread_resolution":false,"type":"pull_request"}],"target":"branch"}' | gh api '/repos/{owner}/{repo}/rulesets' --silent --method POST -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" --input -
echo "If you got a HTTP 422 error, that means a ruleset called 'default-branch-protection' already exists. If you've run this script before, this error can be ignored."