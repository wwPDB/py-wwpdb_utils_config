# File: setup.py
# Date: 3-Oct-2018
#
# Update:
#
import re

from setuptools import find_packages
from setuptools import setup

packages = []
thisPackage = "wwpdb.utils.config"

# Load packages from requirements*.txt
with open("requirements.txt", "r") as ifh:
    packagesRequired = [ln.strip() for ln in ifh.readlines()]

with open("requirements-test.txt", "r") as ifh:
    packagesTest = [ln.strip() for ln in ifh.readlines()]

with open("README.md", "r") as ifh:
    longDescription = ifh.read()

with open("wwpdb/utils/config/__init__.py", "r") as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError("Cannot find version information")

setup(
    name=thisPackage,
    version=version,
    description="wwPDB Python Configuration Parsing",
    long_description=longDescription,
    long_description_content_type="text/markdown",
    author="Ezra Peisach",
    author_email="ezra.peisach@rcsb.org",
    url="https://github.com/rcsb/py-wwpdb_utils_config",
    #
    license="Apache 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        # 'Development Status :: 5 - Production/Stable',
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    entry_points={
        "console_scripts": [
            "ConfigInfoFileExec=wwpdb.utils.config.ConfigInfoFileExec:main",
            "ConfigInfoDataSetExec=wwpdb.utils.config.ConfigInfoDataSetExec:main",
        ]
    },
    #
    install_requires=packagesRequired,
    tests_require=packagesTest,
    packages=find_packages(exclude=["wwpdb.utils.tests-config", "mock-data", "tests.*"]),
    package_data={
        # If any package contains *.md or *.rst ...  files, include them:
        "": ["*.md", "*.rst", "*.txt", "*.cfg"],
    },
    #
    test_suite="wwpdb.utils.tests-config",
    #
    extras_require={"all": packagesRequired + packagesTest, "test": packagesTest, "dev": ["check-manifest"]},
    # Added for
    command_options={
        "build_sphinx": {
            "project": ("setup.py", thisPackage),
            "version": ("setup.py", version),
            "release": ("setup.py", version),
        }
    },
    # This setting for namespace package support -
    zip_safe=False,
)
