from setuptools import setup, find_packages

version = "0.3.0"

setup(
    name="validate-it",
    packages=find_packages(),
    version=version,
    description="Yet another schema validator",
    long_description="Yet another schema validator",
    author="Ruslan Roskoshnyj",
    author_email="i.am.yarger@gmail.com",
    url="https://github.com/ruslux/validate_it",
    download_url="https://github.com/ruslux/validate_it/archive/{}.tar.gz".format(version),
    keywords=["schema", "validator", "json"],
    classifiers=[],
    python_requires=">3.7.0",
    platforms=["OS Independent"],
    license="LICENSE.txt",
    install_requires=[],
    extras_require={
        "tests": [
            "pytest (==3.4.0)",
            "coverage (==4.5)",
            "pytest-cov (==2.5.1)",
            "python-box (==3.2.0)",
        ],
        "docs": [
            "sphinx >= 1.4",
            "aiohttp_theme"
        ]
    }
)
