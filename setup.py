"""Set up the pym project"""


from setuptools import setup, find_packages


import pym


setup(
    packages=find_packages()
    download_url="https://github.com/jalanb/pym/tarball/v%s" % pym.__version__,
    test_suite="pytest.collector",
    install_requires=["pysyte", "sh"],
    tests_require=[
        "coverage<5",
        "mock",
        "pytest",
        "pysyte",
        "pytest-cov",
        "tox",
    ],
    extras_require={
        "test": ["pytest", "pysyte", ],
        "development": ["ipython", "pudb3"],
        "devops": ["bumpversion",],
        "lint": ["black", "flake8", "mypy"]
    }
)
