import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

VERSION_NUMBER_BASE="0.0.1"

build_number = "TESTING"

try:
    build_number = open("BUILD_NUMBER","r").read().strip()
except Exception:
    print("WARNING: There is no BUILD_NUMBER file")

if build_number == "RELEASE":
    VERSION = VERSION_NUMBER_BASE
else:
    VERSION = "{}.{}".format(VERSION_NUMBER_BASE,build_number)

PACKAGE_EXCLUDE = [
    "tests",
    "project",
    "*pytest*"
    "test"
    "Jenkinsfile"
]

SETUP_REQS = [
    "setuptools >= 40.5.0",
    "wheel >= 0.32.2"
]

TEST_REQS = [
    "pytest >= 3.7.2",
    "pep8 >= 1.7.1"
]


setuptools.setup(
    name="elasticsearch-python-client",
    version=VERSION,
    author="koebane82",
    author_email="jeff@koebane.net",
    description="An Alternative ElasticSearch Python Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/koebane82/elasticsearchpy",
    packages=setuptools.find_packages(exclude=PACKAGE_EXCLUDE),
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    setup_requires=SETUP_REQS,
    tests_require=TEST_REQS
)
