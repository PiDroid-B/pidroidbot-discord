.. _dev_gitmanagement:

=================
git management
=================

Branches
-----------

There are several type of branch :

- main : contains all releases (latest included) about this project. Never push on it.
- rc : (if exist) contains the release candidate (will be the next release). Never push on it.
- dev / test : only for special test (ci), output will be create on dev-output|test-output.

For each new development, create a dedicated branch and create pull request to rc when the dev is done.