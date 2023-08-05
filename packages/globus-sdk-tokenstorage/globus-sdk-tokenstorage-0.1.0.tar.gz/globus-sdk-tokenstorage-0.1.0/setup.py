import os.path

from setuptools import find_packages, setup

# single source of truth for package version
version_ns = {}
with open(os.path.join("globus_sdk_tokenstorage", "version.py")) as f:
    exec(f.read(), version_ns)

setup(
    name="globus-sdk-tokenstorage",
    version=version_ns["__version__"],
    description="Globus SDK TokenStorage Extension",
    long_description=open("README.rst").read(),
    author="Stpehen Rosen",
    author_email="sirosen@globus.org",
    url="https://github.com/globus/globus-sdk-python-tokenstorage",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=["globus-sdk>=1.6.1,<2"],
    extras_require={
        "development": [
            # drive testing with tox
            "tox>=3.5.3,<4.0",
            # linting
            "flake8>=3.0,<4.0",
            "isort>=4.3,<5.0",
            # black requires py3.6+
            'black==18.9b0;python_version>="3.6"',
            # flake-bugbear requires py3.5+
            'flake8-bugbear==18.8.0;python_version>="3.5"',
            # testing
            "pytest>=3.7.4,<4.0",
            "pytest-cov>=2.5.1,<3.0",
            "pytest-xdist>=1.22.5,<2.0",
            # mock on py2, py3.4 and py3.5
            # not just py2: py3 versions of mock don't all have the same
            # interface!
            'mock==2.0.0;python_version<"3.6"',
            # builds + uploads to pypi
            "twine==1.12.1",
            "wheel==0.32.2",
            # docs
            "sphinx==1.8.1",
        ]
    },
    include_package_data=True,
    keywords=["globus", "sdk", "contrib"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
