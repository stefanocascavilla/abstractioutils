import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
# noinspection PyInterpreter
setup(
    name="abstractioutils",
    version="1.0.0",
    description="Common packages used in Abstractio",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/stefanocascavilla/abstractioutils",
    author="Stefano Cascavilla",
    author_email="cascavilla1@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    install_requires=["boto3==1.16.63", "pydantic==1.8.1", "oauth2client==4.1.3", "google-api-python-client==1.8.0", "google-auth==1.28.1"],
)
