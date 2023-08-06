import setuptools
from subprocess import check_output


def __extract_long_description():
    """Extract the long description from the Markdown README.md file."""

    with open("README.md") as readme_file:
        return readme_file.read()


def __extract_version():
    """Extract the version of GLICA from the git tag. Should be even with a tag otherwise will overwite."""

    return check_output(["git", "describe", "--tags"]).strip().decode("utf-8").split("-")[0]


setuptools.setup(
    name="glica",
    version=__extract_version(),
    scripts=["glica.py"],
    author="Tian Hao Wang",
    author_email="dev@paced.me",
    description="GitLab Instant Changelog Assurance (GLICA) for ensuring up-to-date CHANGELOG.md files!",
    long_description=__extract_long_description(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/halfbakedstudio/tools/glica",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Version Control :: Git",
        "Operating System :: OS Independent",
    ],
)
