from setuptools import setup, find_packages

version = "0.0.1"

setup(
    name="botarang",
    packages=find_packages(),
    version=version,
    description="Ui elements for building telegram bot",
    long_description="Ui elements for building telegram bot",
    author="Ruslan Roskoshnyj",
    author_email="i.am.yarger@gmail.com",
    url="https://github.com/newmediatech/botarang",
    download_url="https://github.com/ruslux/newmediatech/archive/{}.tar.gz".format(version),
    keywords=["telegram", "bot", "ui", "framework"],
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
        ]
    }
)
