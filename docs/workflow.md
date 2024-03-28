# Workflow for Using Template

## Creating New Project

## Applying to Existing Project

To apply this template to an existing project, follow these steps:

1. Ensure your project is already using Git, and the all of the following are true:
    1. Project is checked out to your local computer
    1. All changes are committed
    1. Default branch is checked out
1. Run the following in order to apply the template to your local project, changing that path as appropriate:

    ``` shell
    copier copy --trust --overwrite gh:natescherer/postmodern-repo-template /path/to/project
    ```

1. Make sure to choose `Set Repo Rules` in the first question
1. Set all other settings as appropriate for your project