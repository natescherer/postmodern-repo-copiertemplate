# Applying to Existing Projects

To apply this template to an existing project, follow these steps:

1. Review the prerequisites from [Getting Started](getting_started.md) and decide which method you are using
1. Ensure your project is already using Git, and the all of the following are true:
   1. Project is cloned to your local computer
   1. All changes are committed
   1. Default branch (usually `main` or `master`) is checked out
1. Create a new branch (`copier-template-apply`, for example) from your default branch
1. Make sure your shell is in the project root, then run the appropriate command below based on the method you are using for prerequisites:

    *Docker*

    ```shell
    docker run -v .:/mnt/${PWD##*/} -w /mnt/${PWD##*/} -v ~/.gitconfig:/root/.gitconfig:ro -e USE_TOKEN_FOR_GIT_AUTH=true -it --pull always --rm ghcr.io/natescherer/postmodern-tools-container:latest copier copy --trust --overwrite gh:natescherer/postmodern-repo-copiertemplate .
    ```

    *Devcontainer/Manual*

    ```shell
    copier copy --trust --overwrite gh:natescherer/postmodern-repo-copiertemplate .
    ```

1. If you are using GitHub, Make sure to choose `Set Repo Rules` in the first question
1. Set all other settings as appropriate for your project
1. Once the template is applied, review files that have been changed using git, and stage, discard, or modify as appropriate
1. Commit and push the changes, then merge them via a Pull Request
1. You are done, and your project will now operate the same as one that was generated from this template.
