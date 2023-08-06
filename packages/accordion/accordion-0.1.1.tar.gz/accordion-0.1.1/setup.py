from setuptools import setup, find_packages

version = "0.1.1"

setup(
    name="accordion",
    packages=find_packages(),
    version=version,
    description="Make flat dict and back from dict",
    long_description="Make flat dict and back from dict",
    author="Ruslan Roskoshnyj",
    author_email="i.am.yarger@gmail.com",
    url="https://github.com/newmediatech/accordion",
    download_url="https://github.com/newmediatech/accordion/archive/{}.tar.gz".format(version),
    keywords=["flat", "dict"],
    classifiers=[],
    python_requires=">3.6.0",
    platforms=["OS Independent"],
    license="LICENSE.txt",
    install_requires=[],
    extras_require={
        "tests": [
            "pytest (==3.4.0)",
            "coverage (==4.5)",
            "pytest-cov (==2.5.1)",
        ]
    }
)
