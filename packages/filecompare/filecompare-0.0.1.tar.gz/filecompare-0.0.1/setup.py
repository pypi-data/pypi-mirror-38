
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="filecompare",
    version="0.0.1",
    author="rascoro1",
    author_email="andcope1995@gmail.com",
    description="commnad line utility for comparing files in directories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rascoro1/filecompare",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)