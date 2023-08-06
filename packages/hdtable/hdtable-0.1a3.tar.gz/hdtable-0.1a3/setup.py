from codecs import open
from os import path
from setuptools import find_packages
from setuptools import setup


here = path.abspath(path.dirname(__file__))


with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()


with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    requirements = f.readlines()


setup(
    name="hdtable",
    version="0.1a3",
    description="Generate reStructuredText grid tables from hierarchical data",
    url="https://gitlab.com/yagehu/hdtable",
    long_description=long_description,
    author="Yage Hu",
    author_email="yagejhu@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    python_requires=">=3.6",
    entry_points={
        "console_scripts": []
    },
)
