from setuptools import find_packages, setup

setup(
    name="tinyprompt",
    version="0.1.0",
    description="Tiny Handy Prompting Lib",
    long_description=open("README.rst").read(),
    author="Stephen Rosen",
    author_email="sirosen@globus.org",
    url="https://github.com/sirosen/tinyprompt",
    packages=find_packages(exclude=["tests", "tests.*"]),
    install_requires=[],
    extras_require={
        # the development extra is for maintainers only
        "development": [
            # linting
            "flake8>=3.0,<4.0",
            "flake8-bugbear==18.8.0",
            "isort>=4.3,<5.0",
            'black==18.9b0;python_version>="3.6"',
            # testing
            "pytest>=3.7.4,<4.0",
            "pytest-cov>=2.5.1,<3.0",
            # uploads to pypi
            "twine==1.11.0",
        ]
    },
    include_package_data=True,
    keywords=["cli", "prompt", "utility"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
