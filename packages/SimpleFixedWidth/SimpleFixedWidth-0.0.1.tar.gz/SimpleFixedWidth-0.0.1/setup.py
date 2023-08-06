import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="SimpleFixedWidth",
    version="0.0.1",
    author="John Glasgow",
    author_email="jglasgow@northampton.edu",
    description="A simple python library for quickly parsing records in a fixed width format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/N-C-C/simplefixedwidth.git",
    packages=['fixedwidth'],
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
)