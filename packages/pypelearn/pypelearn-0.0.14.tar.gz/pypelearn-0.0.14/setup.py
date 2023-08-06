import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pypelearn",
    version="0.0.14",
    author="Alex Harston",
    author_email="alex@harston.io",
    description="A pipeline library for testing and validating time series data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alexharston/pypelearn",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)