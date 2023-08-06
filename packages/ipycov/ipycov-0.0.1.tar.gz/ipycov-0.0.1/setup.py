from io import open
import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.md"), encoding="utf-8").read()


version = "0.0.1"


setup(
    author="Santiago Balestrini-Robinson",
    author_email="sanbales@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    description="Coverage access via IPython",
    include_package_data=True,
    install_requires=[
        "coverage>=4",
        "ipython>=1.0",
    ],
    keywords="testing coverage ipython",
    license="MIT",
    long_description=README,
    name="ipycov",
    packages=find_packages(exclude=("tests",)),
    test_suite="tests",
    url="https://pypi.python.org/pypi/ipython-coverage",
    version=version,
    zip_safe=False,
)
