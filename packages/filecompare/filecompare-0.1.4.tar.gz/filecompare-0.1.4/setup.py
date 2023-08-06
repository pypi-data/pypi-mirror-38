
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name = 'filecompare',
    version = '0.1.4',
    author="rascoro1",
    author_email="andcope1995@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rascoro1/filecompare",
    packages = ['filecompare'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': [
            'filecompare = filecompare.__main__:main'
        ]
    })