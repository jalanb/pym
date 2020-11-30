"""Set up the pym project"""


from setuptools import setup, find_packages


import pym


setup(
    packages=find_packages(),
    download_url=f"https://github.com/jalanb/pym/tarball/v{pym.__version__}",
    test_suite="pytest.collector",
    install_requires=[
        "pprintpp",
        "pysyte>=0.7.41",
        "rich",
        "stemming",
        "tatsu",
    ],
    tests_require=[
        "codecov",
        "coverage",
        "pym==0.3.3",
        "pysyte>=0.7.41",
        "pytest",
        "pytest-cov",
        "tox",
    ],
    extras_require={
        "test": [
            "pytest",
            "pysyte",
        ],
        "development": ["ipython", "pudb3"],
        "devops": [
            "bumpversion",
        ],
        "lint": ["black", "flake8", "mypy"],
    },
)
