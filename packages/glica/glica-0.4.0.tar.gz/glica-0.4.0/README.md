# GitLab Issues Changelog Assurance

Ensures changelogs are created/updated for each release.

## Assumptions

1. Each tag must contain a corresponding, level-2 Markdown header (i.e.: starting with `##`) in the CHANGELOG.md.
2. Each tag must be a SemVer version. It can have as many levels as you like (using `.`, `+`, and `-` delimiters) but should be proper SemVer syntax without any other special character.
3. Each CHANGELOG.md entry should be in order. Remember that `0.9.0` \< `0.10.0` in SemVer!

## Algorithm

When `glica` is called, an the CHANGELOG.md file is scanned with a regular expression for headers. All of the `git` tags are stored.

CHANGELOG.md must exist and have a header in the CHANGELOG.md file for each tag version. If either isn't true, `glica` will exit with an error message.

## Requirements

- Python 2.7/3.5

## Usage

Artifacts are deployed to `pypi`. This is an example of the simplest configuration of GLICA (gets the latest version of GLICA each time):

```yaml
glica:
  image: "python:3.5"
  stage: test
  script:
  - pip install glica
  - python -m glica
```

Note that the version above can be any released version.

## Development

This `.gitlab-ci.yml` file will run the script on each commit. This is excessive. You can run it on each tag for a software project.
