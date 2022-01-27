import io
from setuptools import setup, find_packages

requirements = [
    "logzero",
    "requests",
    "jikanpy",
    "backoff",
    "click",
    "pygsheets",
    "google-auth",
    "cachecontrol[filecache]",
    "appdirs",
]

# Use the README.md content for the long description:
with io.open("README.md", encoding="utf-8") as fo:
    long_description = fo.read()

setup(
    name="mnu_gsheets",
    version="0.1.0",
    url="https://github.com/seanbreckenridge/mnu_gsheets",
    author="Sean Breckenridge",
    author_email="seanbrecke@gmail.com",
    description=("""tracking obscure anime music videos"""),
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    packages=find_packages(include=["mnu_gsheets"]),
    install_requires=requirements,
    keywords="anime",
    entry_points={"console_scripts": ["mnu_gsheets = mnu_gsheets.__main__:main"]},
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
