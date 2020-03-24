import setuptools


def get_license():
    """ replace the license content while creating the package"""
    with open("LICENSE.md", "r", encoding="utf8") as fh:
        license_description = fh.read()
        return license_description


def get_install():
    """ replace the install content while creating the package"""
    with open("INSTALL.md", "r", encoding="utf8") as fh:
        install_description = fh.read()
        return install_description


def get_maintainers():
    """ replace the maintainers content while creating the package"""
    with open("MAINTAINERS.md", "r", encoding="utf8") as fh:
        maintainers_description = fh.read()
        return maintainers_description


with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()
    if "[INSTALL.md](INSTALL.md)" in long_description:
        long_description = long_description.replace("[INSTALL.md](INSTALL.md)", str(get_install()))
    if "[MAINTAINERS.md](MAINTAINERS.md)"  in long_description:
        long_description = long_description.replace("[MAINTAINERS.md](MAINTAINERS.md)", str(get_maintainers()))
    if "[License.md](License.md)" in long_description:
        long_description = long_description.replace("[License.md](License.md)", str(get_license()))

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="functiondefextractor",
    version="0.0.2",
    author="Brijesh",
    author_email="brijesh.krishnank@philips.com",
    description="Function Definition Extractor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bkk003/FunctionDefExtractor",
    packages=setuptools.find_packages(include=['functiondefextractor'], exclude=['test', '*.test', '*.test.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
    python_requires='>=3.6',
)
