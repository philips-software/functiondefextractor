import setuptools
from versiontag import get_version


def get_description(file_name):
    """ replace the license content while creating the package"""
    with open(file_name, "r", encoding="utf8") as fh:
        description = fh.read()
        return description


with open("README.md", "r") as fh:
    long_description = fh.read()
    long_description = long_description.replace(
        "[MAINTAINERS.md](MAINTAINERS.md)",
        str(get_description("MAINTAINERS.md"))).replace(
        "[INSTALL.md](INSTALL.md)", str(get_description("INSTALL.md"))).replace(
        "[License.md](LICENSE.md)", str(get_description("LICENSE.md")))

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="functiondefextractor",
    version=get_version(pypi=True),
    author="Brijesh",
    author_email="brijesh.krishnank@philips.com",
    description="Function Definition Extractor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/philips-software/functiondefextractor",
    packages=setuptools.find_packages(include=['functiondefextractor'], exclude=['test', '*.test', '*.test.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
    python_requires='>=3.7',
)
