"""Scan a CHANGELOG.md file for versions to ensure matching of second-level headers and version tags."""

from subprocess import check_output
import re
import sys


def __extract_sortable_tuple(semver_string):
    """Extract a tuple that can be sorted from a valid semver string (including those with + or - annotations)."""

    components = semver_string.replace("-", ".").replace("+", ".").split(".")

    return tuple([int(i) if i.isdigit() else i for i in components])


def __extract_tags():
    """Extract tags from git using command line."""

    raw_tags = check_output(["git", "tag"], universal_newlines=True).strip()
    tags = raw_tags.split('\n')

    # Sort based on SemVer.

    return sorted(tags, key=__extract_sortable_tuple)


def __extract_versions():
    """Get the versions from the CHANGELOG."""

    regex = re.compile("##.*")  # Match level 2 headers.
    versions = list()

    with open("CHANGELOG.md") as changelog_file:
        for line in changelog_file:
            result = regex.search(line)

            if result:
                versions.append(line[2:].strip())

    return versions


if __name__ == "__main__":
    try:
        found_versions = __extract_versions()
        required_versions = __extract_tags()

        missing_versions = set(required_versions) - set(found_versions)

        if missing_versions:
            sys.exit("FIXME: CHANGELOG.md versions need to contain: " +
                     str(missing_versions))

        for i in range(len(required_versions)):
            if required_versions[i] != found_versions[::-1][i]:
                sys.exit("FIXME: CHANGELOG.md and tags are out of order.")
    except FileNotFoundError:
        sys.exit("FIXME: Cannot find CHANGELOG.md.")
