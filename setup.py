import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="functiondefextractor",
    version="0.0.1",
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